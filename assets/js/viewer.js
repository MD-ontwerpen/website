/* ==========================================================================
   MD-ontwerpen — layered building viewer

   Vanilla Three.js (no React on this site, and no build step), loaded as an ES
   module from a CDN. One GLB holds the whole building; every mesh is named
   `layer_<slug>__<part>`, so selecting a service highlights that layer and dims
   the rest — the 3D counterpart of the per-service drawings.

   Deliberate guards, following the 3d-web-experience skill's anti-patterns:
     - static SVG fallback, and 3D is never loaded when the visitor cannot or
       should not run it (no WebGL, reduced motion, save-data, low core count)
     - nothing downloads until the visitor asks for it, so the page keeps its
       sub-second load
     - explicit loading progress, because a blank canvas reads as broken
   ========================================================================== */

// Module specifiers are resolved by the import map in index.html, not written
// as URLs here: the addons import from a bare "three", so they only resolve if
// the page declares that mapping.

// Set once three.js is imported; a plain object cannot be passed to Color.lerp
let GHOST_TINT = null;

const state = {
  loaded: false,
  loading: false,
  layers: new Map(), // slug -> { meshes: [], originals: [] }
  active: null,
  renderer: null,
  scene: null,
  camera: null,
  controls: null,
  frame: null,
};

/* ---------------------------------------------------------------- capability */

function webglAvailable() {
  try {
    const c = document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (c.getContext("webgl2") || c.getContext("webgl")));
  } catch (e) {
    return false;
  }
}

function shouldOfferThreeD() {
  if (!webglAvailable()) return { ok: false, reason: "geen WebGL" };
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return { ok: false, reason: "beperkte beweging" };
  }
  const conn = navigator.connection;
  if (conn && conn.saveData) return { ok: false, reason: "databesparing" };
  if (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2) {
    return { ok: false, reason: "beperkte hardware" };
  }
  return { ok: true, reason: null };
}

/* -------------------------------------------------------------------- render */

function schedule() {
  if (state.frame !== null) return;
  state.frame = requestAnimationFrame(() => {
    state.frame = null;
    if (state.controls) state.controls.update();
    state.renderer.render(state.scene, state.camera);
  });
}

/* ------------------------------------------------------------------ layering */

const DIM = 0.16;

/*
  Layers that only make sense when chosen. The thermal shell and the model grid
  enclose the whole building, and the crane, plot boundary and tender blocks sit
  outside it - shown together they occlude the building and read as clutter, so
  the default view is the building itself and these appear on selection.
*/
const OVERLAY_ONLY = new Set([
  "bouwfysica",
  "informatiemodel",
  "vergunnen",
  "aanbesteden",
  "bouwen",
  "opleveren",
]);

function collectLayers(root, THREE) {
  root.traverse((obj) => {
    if (!obj.isMesh || !obj.name.startsWith("layer_")) return;
    const slug = obj.name.slice("layer_".length).split("__")[0];
    if (!state.layers.has(slug)) state.layers.set(slug, { meshes: [] });
    // Clone so dimming one layer cannot leak into a mesh that shares a material
    obj.material = obj.material.clone();
    obj.userData.baseColor = obj.material.color.clone();
    obj.userData.baseOpacity = obj.material.opacity;
    state.layers.get(slug).meshes.push(obj);
  });
}

function applyHighlight(slug) {
  state.active = slug;

  state.layers.forEach((layer, key) => {
    const selected = key === slug;
    const overlay = OVERLAY_ONLY.has(key);

    // Nothing chosen: the building, without the abstract layers.
    // Something chosen: that layer solid, the building ghosted behind it,
    // every other overlay out of the way.
    const visible = slug === null ? !overlay : selected || !overlay;
    const ghost = visible && !selected && slug !== null;

    layer.meshes.forEach((m) => {
      m.visible = visible;
      m.material.color.copy(m.userData.baseColor);

      if (ghost) {
        // Toward grey, not white: on a near-white page a white ghost disappears
        m.material.color.lerp(GHOST_TINT, 0.5);
        m.material.transparent = true;
        m.material.opacity = DIM;
        m.material.depthWrite = false;
      } else {
        m.material.transparent = m.userData.baseOpacity < 1;
        m.material.opacity = m.userData.baseOpacity;
        m.material.depthWrite = true;
      }
    });
  });

  schedule();
}

/* ---------------------------------------------------------------------- boot */

async function boot(mount, statusEl, buttons) {
  state.loading = true;
  statusEl.hidden = false;
  statusEl.textContent = "3D-model laden… 0%";

  const THREE = await import("three");
  GHOST_TINT = new THREE.Color(0x9aa4b2);
  const { OrbitControls } = await import("three/addons/controls/OrbitControls.js");
  const { GLTFLoader } = await import("three/addons/loaders/GLTFLoader.js");

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xfafafa);

  const camera = new THREE.PerspectiveCamera(38, 1, 0.5, 400);
  camera.position.set(26, 20, 30);

  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "low-power" });
  // Cap DPR: retina phones otherwise render 3x the pixels for no visible gain
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  mount.appendChild(renderer.domElement);

  scene.add(new THREE.HemisphereLight(0xffffff, 0xd8dee6, 2.1));
  const key = new THREE.DirectionalLight(0xffffff, 1.7);
  key.position.set(18, 26, 14);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, 0.5);
  fill.position.set(-16, 10, -12);
  scene.add(fill);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.minDistance = 14;
  controls.maxDistance = 90;
  controls.maxPolarAngle = Math.PI / 2 - 0.04; // never go below the ground plane
  controls.target.set(0, 5, 0);
  controls.addEventListener("change", schedule);

  state.renderer = renderer;
  state.scene = scene;
  state.camera = camera;
  state.controls = controls;

  const resize = () => {
    const r = mount.getBoundingClientRect();
    const w = Math.max(1, r.width);
    const h = Math.max(1, r.height);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    schedule();
  };
  if ("ResizeObserver" in window) new ResizeObserver(resize).observe(mount);
  else window.addEventListener("resize", resize);
  resize();

  await new Promise((resolve, reject) => {
    new GLTFLoader().load(
      "assets/models/gebouw-lagen.glb",
      (gltf) => {
        collectLayers(gltf.scene, THREE);
        scene.add(gltf.scene);

        // Frame to the building itself, ignoring the crane and plot markers,
        // so the default view is not zoomed out to fit scenery.
        const core = new THREE.Box3();
        gltf.scene.traverse((o) => {
          if (!o.isMesh) return;
          const slug = o.name.slice("layer_".length).split("__")[0];
          if (OVERLAY_ONLY.has(slug) || slug === "landschap") return;
          core.expandByObject(o);
        });
        // The GLB is Y-up, so this is plain framing: stand back along X and Z,
        // rise a little above the midpoint, and look at the building's centre.
        const size = core.getSize(new THREE.Vector3());
        const mid = core.getCenter(new THREE.Vector3());
        const radius = Math.max(size.x, size.y, size.z);
        camera.position.set(mid.x + radius * 1.35, mid.y + radius * 0.85, mid.z + radius * 1.55);
        controls.target.copy(mid);
        controls.minDistance = radius * 0.8;
        controls.maxDistance = radius * 5;
        controls.update();

        resolve();
      },
      (evt) => {
        if (evt.lengthComputable) {
          const pct = Math.round((evt.loaded / evt.total) * 100);
          statusEl.textContent = `3D-model laden… ${pct}%`;
        }
      },
      reject
    );
  });

  statusEl.hidden = true;
  state.loaded = true;
  state.loading = false;
  buttons.forEach((b) => (b.disabled = false));
  applyHighlight(null);
}

/* ---------------------------------------------------------------------- init */

export function initViewer() {
  const root = document.querySelector("[data-viewer]");
  if (!root) return;

  const mount = root.querySelector("[data-viewer-canvas]");
  const statusEl = root.querySelector("[data-viewer-status]");
  const startBtn = root.querySelector("[data-viewer-start]");
  const fallback = root.querySelector("[data-viewer-fallback]");
  const buttons = Array.from(root.querySelectorAll("[data-layer]"));

  const capability = shouldOfferThreeD();
  if (!capability.ok) {
    // Keep the static drawing; say why rather than silently doing nothing
    if (startBtn) {
      startBtn.hidden = true;
    }
    if (statusEl) {
      statusEl.hidden = false;
      statusEl.textContent = `Statische weergave (${capability.reason}).`;
    }
    return;
  }

  buttons.forEach((b) => (b.disabled = true));

  startBtn.addEventListener("click", async () => {
    startBtn.disabled = true;
    startBtn.hidden = true;
    if (fallback) fallback.hidden = true;
    try {
      await boot(mount, statusEl, buttons);
    } catch (err) {
      statusEl.hidden = false;
      statusEl.textContent = "Het 3D-model kon niet worden geladen.";
      if (fallback) fallback.hidden = false;
      startBtn.hidden = false;
      startBtn.disabled = false;
    }
  });

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const slug = btn.getAttribute("data-layer");
      const next = state.active === slug ? null : slug;
      buttons.forEach((b) =>
        b.setAttribute("aria-pressed", b.getAttribute("data-layer") === next ? "true" : "false")
      );
      applyHighlight(next);
    });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initViewer);
} else {
  initViewer();
}
