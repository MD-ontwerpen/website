/* The landing page's media layer: a sequence of houses.

   Two visual states only, per the brief - a playing video, or a static still
   that can be clicked to play the next one. The still is the video's own last
   frame, so the cut between them should be invisible; there is deliberately no
   crossfade, because fading a picture into a copy of itself reads as a stutter
   rather than a transition.

   The media layer is full screen with the header and footer in front of it,
   which is the rule taken at checkpoint 1. The four orbiting links sit in front
   too, so a click on one of them must navigate rather than advance the
   sequence - see the guard in onStillClick.

   Nothing here is required for the page to work. If the config is missing, a
   video fails, or autoplay is refused, the still stays on screen and the links
   over it stay clickable.
*/

const CONFIG = "config/houses.json";

function ready(fn) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn);
  } else {
    fn();
  }
}

function Showcase(root, data) {
  const houses = data.houses || [];
  if (!houses.length) return;

  const loop = data.loop !== false;
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const still = root.querySelector(".showcase-still");
  // Two video elements, alternating. Loading a fresh src at click time gives a
  // buffering flash; the next clip is already decoded in the spare one.
  const players = [
    root.querySelector(".showcase-video--a"),
    root.querySelector(".showcase-video--b"),
  ];
  let active = 0;
  let index = 0;

  function nextIndex(i) {
    const n = i + 1;
    if (n < houses.length) return n;
    return loop ? 0 : -1;
  }

  function preload(i) {
    if (i < 0) return;
    const el = players[1 - active];
    const src = houses[i].video;
    if (!src || el.dataset.src === src) return;
    el.dataset.src = src;
    el.src = src;
    el.load();
  }

  function showStill(i) {
    const house = houses[i];
    still.src = house.still;
    still.alt = house.label || "";
    root.dataset.state = nextIndex(i) < 0 ? "end" : "still";
    players.forEach((p) => {
      p.hidden = true;
    });
    still.hidden = false;
    preload(nextIndex(i));
  }

  function play(i) {
    const house = houses[i];
    if (!house.video) {
      // no clip for this house: fall through to its still rather than stall
      showStill(i);
      return;
    }
    const el = players[active];
    if (el.dataset.src !== house.video) {
      el.dataset.src = house.video;
      el.src = house.video;
    }
    root.dataset.state = "playing";
    still.hidden = true;
    players.forEach((p, n) => {
      p.hidden = n !== active;
    });

    el.currentTime = 0;
    const started = el.play();
    if (started && started.catch) {
      // autoplay refused - iOS low power mode does this - so settle on the
      // still, which is a complete picture in its own right
      started.catch(() => showStill(i));
    }
  }

  players.forEach((el, n) => {
    el.addEventListener("ended", () => {
      if (n !== active) return;
      showStill(index);
      active = 1 - active; // the preloaded one becomes the next to play
    });
    el.addEventListener("error", () => {
      if (n === active) showStill(index);
    });
  });

  function advance(event) {
    // the orbiting links sit over the still; let them navigate
    if (event && event.target.closest("a")) return;
    if (root.dataset.state !== "still") return;
    const n = nextIndex(index);
    if (n < 0) return;
    index = n;
    play(index);
  }

  root.addEventListener("click", advance);
  root.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      if (e.target.closest("a")) return;
      e.preventDefault();
      advance();
    }
  });

  // First frame: autoplay unless motion is unwelcome, in which case the still
  // is the whole experience and clicking still advances it.
  if (reduced) {
    showStill(0);
  } else {
    showStill(0); // paint something immediately, then start
    play(0);
  }
}

ready(function () {
  const root = document.querySelector(".showcase");
  if (!root) return;
  fetch(root.dataset.config || CONFIG)
    .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
    .then((data) => Showcase(root, data))
    .catch(() => {
      /* no config: the markup's own first still stays on screen */
    });
});
