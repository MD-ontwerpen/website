/* Landing-page stage: the building turns once, then holds still.

   Loaded only here, and only after first paint, so the other pages stay at a
   few KB and this one shows its header, links and footer before the 210KB of
   library and model arrives.

   The four labels are real links in the markup, positioned over the canvas
   rather than drawn inside it. Text rendered into WebGL is invisible to search
   engines, to screen readers and to keyboard users; these are ordinary anchors
   that happen to be arranged in a circle.

   Nothing here is required for the page to work. If WebGL is missing, the
   import fails, or the model does not arrive, the links stay exactly where CSS
   put them and remain clickable.
*/

import * as THREE from "./vendor/three.module.min.js";
import { GLTFLoader } from "./vendor/GLTFLoader.js";

const TURN_MS = 1000;

function start() {
  const stage = document.querySelector(".stage");
  const canvas = document.querySelector(".stage-canvas");
  if (!stage || !canvas) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true,
    });
  } catch (e) {
    // no WebGL: the links are already in place, so there is nothing to undo
    return;
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(stage.clientWidth, stage.clientHeight, false);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    35,
    stage.clientWidth / stage.clientHeight,
    0.1,
    1000
  );

  scene.add(new THREE.HemisphereLight(0xffffff, 0xbfbfbf, 2.2));
  const key = new THREE.DirectionalLight(0xffffff, 1.4);
  key.position.set(4, 6, 3);
  scene.add(key);

  const pivot = new THREE.Group();
  scene.add(pivot);

  function frame(object) {
    // centre the model on the pivot and pull the camera back far enough to
    // hold it whatever the window shape
    const box = new THREE.Box3().setFromObject(object);
    const size = box.getSize(new THREE.Vector3());
    const centre = box.getCenter(new THREE.Vector3());
    object.position.sub(centre);

    const radius = Math.max(size.x, size.y, size.z) * 0.5;
    const fov = (camera.fov * Math.PI) / 180;
    let distance = radius / Math.sin(fov / 2);
    if (camera.aspect < 1) distance /= camera.aspect; // portrait needs more room
    camera.position.set(0, radius * 0.55, distance * 1.15);
    camera.lookAt(0, 0, 0);
  }

  function resize() {
    const w = stage.clientWidth;
    const h = stage.clientHeight;
    if (!w || !h) return;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
    if (pivot.children.length) frame(pivot.children[0]);
    renderer.render(scene, camera);
  }

  new GLTFLoader().load(
    stage.dataset.model,
    (gltf) => {
      pivot.add(gltf.scene);
      frame(gltf.scene);
      stage.dataset.ready = "true";

      const end = pivot.rotation.y;
      if (reduced) {
        renderer.render(scene, camera);
        return;
      }

      // one turn, anticlockwise, matching the labels; then it stops and the
      // loop is torn down rather than idling against the battery
      const from = end + Math.PI * 2;
      const t0 = performance.now();
      const ease = (t) => 1 - Math.pow(1 - t, 3);

      (function turn(now) {
        const t = Math.min((now - t0) / TURN_MS, 1);
        pivot.rotation.y = from + (end - from) * ease(t);
        renderer.render(scene, camera);
        if (t < 1) requestAnimationFrame(turn);
      })(t0);
    },
    undefined,
    () => {
      /* model missing: leave the links as they are */
    }
  );

  window.addEventListener("resize", resize);
  resize();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", start);
} else {
  start();
}
