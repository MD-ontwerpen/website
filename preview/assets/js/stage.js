/* Landing-page stage: a villa turns once, then holds still.

   The building is modelled in code rather than loaded from a file. That is
   smaller than the 128KB placeholder GLB it replaces, drops the GLTF loader and
   its addon with it, and means the massing and the materials are editable here
   rather than in another program.

   Its palette comes from the practice's own renders: dark stained timber, cream
   render, deep flat-roof overhangs, pale stone paving, brick, a dark deck and a
   turquoise pool.

   What makes it read as a render rather than as a diagram is the lighting, not
   the geometry: image-based light from a procedural sky so glass and water have
   something real to reflect, one hard sun for shadows, filmic tone mapping.

   The four labels around it are anchors in the markup, not text drawn into the
   canvas. Nothing here is required for the page to work: if WebGL is missing or
   this module fails, the links stay where CSS put them and remain clickable.
*/

import * as THREE from "./vendor/three.module.min.js";

const TURN_MS = 1000;

/* ---- palette, taken from the reference renders ------------------------- */

const M = {
  render: { color: 0xf0ece4, roughness: 0.92, metalness: 0 }, // cream stucco
  timber: { color: 0x5d4835, roughness: 0.7, metalness: 0 }, // stained slats
  fascia: { color: 0x35322e, roughness: 0.55, metalness: 0.1 }, // roof edge
  glass: { color: 0x1e2a2e, roughness: 0.06, metalness: 0.55 },
  stone: { color: 0xded9d0, roughness: 0.88, metalness: 0 }, // large pavers
  brick: { color: 0xa2634a, roughness: 0.95, metalness: 0 },
  deck: { color: 0x6b4630, roughness: 0.8, metalness: 0 },
  water: { color: 0x1d7f96, roughness: 0.04, metalness: 0.35 },
  grass: { color: 0x87956d, roughness: 1 },
  hedge: { color: 0x556b45, roughness: 0.95 },
  trunk: { color: 0x4b3a2a, roughness: 0.9 },
  leaf: { color: 0x5f7d4a, roughness: 0.95 },
};

function mat(spec) {
  return new THREE.MeshStandardMaterial(spec);
}

/* ---- a sky to light the scene with ------------------------------------ */

function skyTexture() {
  const c = document.createElement("canvas");
  c.width = 16;
  c.height = 256;
  const g = c.getContext("2d");
  const grad = g.createLinearGradient(0, 0, 0, 256);
  grad.addColorStop(0.0, "#2f6fc0"); // zenith
  grad.addColorStop(0.45, "#9cc4e8");
  grad.addColorStop(0.52, "#e9eef2"); // horizon
  grad.addColorStop(1.0, "#b9b2a6"); // ground bounce
  g.fillStyle = grad;
  g.fillRect(0, 0, 16, 256);
  const t = new THREE.CanvasTexture(c);
  t.mapping = THREE.EquirectangularReflectionMapping;
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

/* ---- geometry helpers -------------------------------------------------- */

const BOX = new THREE.BoxGeometry(1, 1, 1);

function box(group, material, w, h, d, x, y, z) {
  const m = new THREE.Mesh(BOX, material);
  m.scale.set(w, h, d);
  m.position.set(x, y + h / 2, z);
  m.castShadow = true;
  m.receiveShadow = true;
  group.add(m);
  return m;
}

function slab(group, material, w, d, x, y, z, h, cast) {
  const m = box(group, material, w, h || 0.06, d, x, y, z);
  m.castShadow = !!cast; // paving lying on the ground would only self-shadow
  return m;
}

/* Vertical slat screen - the motif on the main elevation. */
function slats(group, material, count, w, h, d, x, y, z, spacing) {
  for (let i = 0; i < count; i++) {
    box(group, material, w, h, d, x + (i - (count - 1) / 2) * spacing, y, z);
  }
}

function tree(group, x, z, scale) {
  const s = scale || 1;
  box(group, mat(M.trunk), 0.18 * s, 2.2 * s, 0.18 * s, x, 0, z);
  const crown = new THREE.Mesh(
    new THREE.IcosahedronGeometry(1.05 * s, 1),
    mat(M.leaf)
  );
  crown.position.set(x, 2.6 * s, z);
  crown.scale.set(1, 0.85, 1);
  crown.castShadow = true;
  group.add(crown);
}

/* ---- the villa --------------------------------------------------------- */

function villa() {
  const g = new THREE.Group();
  // The camera frames this subgroup, not the whole scene: the ground plane is
  // deliberately far larger than the shot, and including it pushed the camera
  // so far back that the house became a speck in a green field.
  const core = new THREE.Group();
  core.name = "core";
  g.add(core);

  const grass = mat(M.grass);
  const stone = mat(M.stone);
  const render = mat(M.render);
  const timber = mat(M.timber);
  const fascia = mat(M.fascia);
  const glass = mat(M.glass);

  // ground, terrace, brick strip
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(90, 90), grass);
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  g.add(ground);

  slab(core, stone, 30, 17, 1, 0.01, 2);
  slab(core, mat(M.brick), 11, 6, -8.5, 0.02, 8.5);
  slab(core, mat(M.deck), 9, 4.6, 6.5, 0.03, 6.2);

  // main volume: two storeys, upper set back, deep roof overhang
  box(core, render, 13, 3.4, 8, -3.5, 0, -1);
  slab(core, fascia, 14.4, 9.4, -3.5, 3.4, -1, 0.22, true);
  box(core, timber, 8.5, 3.1, 6.6, -5, 3.62, -1.4);
  slab(core, fascia, 10, 8, -5, 6.72, -1.4, 0.22, true);

  // glazing to the terrace, with the slat screen in front of part of it
  box(core, glass, 12.2, 2.7, 0.12, -3.5, 0.35, 3.06);
  box(core, glass, 7.8, 2.5, 0.12, -5, 3.95, 1.96);
  slats(core, timber, 9, 0.16, 3.3, 0.16, -1.6, 0.05, 3.25, 0.62);

  // single-storey wing to the right, dark timber
  box(core, timber, 7, 2.9, 5.4, 8, 0, -2.2);
  slab(core, fascia, 8.2, 6.6, 8, 2.9, -2.2, 0.2, true);
  box(core, glass, 6.4, 2.3, 0.12, 8, 0.3, 0.56);

  // pool and its coping
  slab(core, stone, 12.4, 5.4, 0.5, 0.02, 7.6);
  const pool = box(core, mat(M.water), 11, 0.5, 4, 0.5, -0.42, 7.6);
  pool.castShadow = false;

  // low rendered garden walls and planters
  box(core, render, 26, 0.9, 0.5, 0, 0, 11.6);
  box(core, render, 0.5, 0.9, 9, -13.2, 0, 7.2);
  box(core, mat(M.hedge), 25, 0.75, 1.1, 0, 0.9, 11.4);

  // planting and trees
  box(core, mat(M.hedge), 5.5, 0.7, 1.2, -10.5, 0, 4.5);
  tree(g, -12.5, -3.5, 1.25);
  tree(g, 13.5, 4.5, 1.0);
  tree(g, 15.5, -6, 1.35);
  tree(g, -14, 9.5, 0.9);

  return g;
}

/* ---- stage ------------------------------------------------------------- */

function start() {
  const stage = document.querySelector(".stage");
  const canvas = document.querySelector(".stage-canvas");
  if (!stage || !canvas) return;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true,
    });
  } catch (e) {
    return; // no WebGL: the links are already in place
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new THREE.Scene();

  // image-based light: without it, glass and water have nothing to reflect and
  // the whole thing reads as flat shaded boxes
  const pmrem = new THREE.PMREMGenerator(renderer);
  const sky = skyTexture();
  scene.environment = pmrem.fromEquirectangular(sky).texture;
  sky.dispose();
  pmrem.dispose();

  const sun = new THREE.DirectionalLight(0xfff4e2, 3.1);
  // Side-on and slightly behind: with the sun on the same side as the camera
  // every shadow fell behind the house, where the house hid it.
  sun.position.set(15, 13, -3);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.near = 1;
  sun.shadow.camera.far = 90;
  sun.shadow.camera.left = -28;
  sun.shadow.camera.right = 28;
  sun.shadow.camera.top = 28;
  sun.shadow.camera.bottom = -28;
  sun.shadow.bias = -0.0006;
  sun.shadow.normalBias = 0.02;
  scene.add(sun);
  scene.add(new THREE.HemisphereLight(0xbcd6f0, 0x8a806f, 0.38));

  const camera = new THREE.PerspectiveCamera(32, 1, 0.5, 300);
  const pivot = new THREE.Group();
  const model = villa();
  pivot.add(model);
  scene.add(pivot);

  // frame on the building, not the plot
  const core = model.getObjectByName("core");
  const box3 = new THREE.Box3().setFromObject(core);
  const size = box3.getSize(new THREE.Vector3());
  const centre = box3.getCenter(new THREE.Vector3());
  model.position.sub(centre);
  const radius = Math.max(size.x, size.z) * 0.5;

  function resize() {
    const w = stage.clientWidth;
    const h = stage.clientHeight;
    if (!w || !h) return;
    camera.aspect = w / h;
    const fov = (camera.fov * Math.PI) / 180;
    // Crop into the plot rather than fitting all of it, so the house fills the
    // frame; and look down on it, which is how a building is usually presented
    // and what keeps the dark volumes from reading as one flat slab.
    let dist = (radius / Math.tan(fov / 2)) * 0.82;
    if (camera.aspect < 1) dist /= camera.aspect; // portrait needs more room
    camera.position.set(0, radius * 0.78, dist);
    camera.lookAt(0, size.y * 0.1, 0);
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
    renderer.render(scene, camera);
  }

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const end = -0.5; // three-quarter view, not square on
  pivot.rotation.y = end;
  stage.dataset.ready = "true";
  resize();

  if (!reduced) {
    // one turn anticlockwise, matching the labels, then it stops and the loop
    // is torn down rather than idling against the battery
    const from = end + Math.PI * 2;
    const t0 = performance.now();
    const ease = (t) => 1 - Math.pow(1 - t, 3);
    (function turn(now) {
      const t = Math.min((now - t0) / TURN_MS, 1);
      pivot.rotation.y = from + (end - from) * ease(t);
      renderer.render(scene, camera);
      if (t < 1) requestAnimationFrame(turn);
    })(t0);
  }

  window.addEventListener("resize", resize);

  if (location.search.indexOf("debug") !== -1) {
    window.__stage = { renderer: renderer, scene: scene, camera: camera, sun: sun };
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", start);
} else {
  start();
}
