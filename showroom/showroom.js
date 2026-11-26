// The entrance to the showroom: the door from the front page fills the
// window, the head over it weeps blood, its mouth opens and pours, the door
// splits open and the view goes in. It runs only with script and only for a
// visitor who has not asked for less motion, and only on arriving at the
// place itself, not at one of its rooms. Without it the showroom is as it is.
// A press, a key or a turn of the wheel ends it at once.

(() => {
  "use strict";

  const SVG = "http://www.w3.org/2000/svg";

  if (matchMedia("(prefers-reduced-motion: reduce)").matches || location.hash) {
    return;
  }

  // The place is held back from the first moment, so that it is not seen
  // before the door, and let go the moment anything fails.
  const root = document.documentElement;
  root.classList.add("entrance-waits");
  const release = () => root.classList.remove("entrance-waits");
  setTimeout(release, 3000);

  // What the door's picture is and where its parts lie, written beside it
  // by the script that draws it.
  const ready = new Promise((resolve) => {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", resolve, { once: true });
    } else {
      resolve();
    }
  });
  // The door's picture is made ready before anything is shown of it.
  const picture = new Image();
  picture.src = "door.svg";
  Promise.all([
    fetch("door.json").then((answer) => (answer.ok ? answer.json() : Promise.reject(answer))),
    picture.decode(),
    ready,
  ])
    .then(([door]) => enter(door))
    .catch(() => {})
    .finally(release);

  function made(name, attributes, parent) {
    const element = document.createElementNS(SVG, name);
    for (const [key, value] of Object.entries(attributes)) {
      element.setAttribute(key, value);
    }
    if (parent) parent.append(element);
    return element;
  }

  function token(name) {
    return getComputedStyle(document.body).getPropertyValue(`--cruor-${name}`).trim();
  }

  function enter(door) {
    const { width, height, middle, half, spring, apex, foot, eyes, mouth } = door;
    const radius = 2 * half;
    const left = middle - half;
    const right = middle + half;

    const veil = document.createElement("div");
    veil.className = "entrance";
    veil.setAttribute("aria-hidden", "true");
    veil.style.background = token("page");

    const svg = made("svg", { viewBox: `0 0 ${width} ${height}`, class: "entrance-door" });
    const defs = made("defs", {}, svg);
    const arch =
      `M${left} ${foot}V${spring}A${radius} ${radius} 0 0 1 ${middle} ${apex}` +
      `A${radius} ${radius} 0 0 1 ${right} ${spring}V${foot}Z`;
    const leftLeaf = `M${left} ${foot}V${spring}A${radius} ${radius} 0 0 1 ${middle} ${apex}V${foot}Z`;
    const rightLeaf = `M${middle} ${apex}A${radius} ${radius} 0 0 1 ${right} ${spring}V${foot}H${middle}Z`;
    made("path", { d: leftLeaf }, made("clipPath", { id: "entrance-left" }, defs));
    made("path", { d: rightLeaf }, made("clipPath", { id: "entrance-right" }, defs));
    const light = made("radialGradient", { id: "entrance-light" }, defs);
    made("stop", { offset: "0", "stop-color": token("chip-top") }, light);
    made("stop", { offset: "0.6", "stop-color": token("heading-top") }, light);
    made("stop", { offset: "1", "stop-color": token("blood") }, light);

    // The door as it stands, and behind its leaves the light within.
    made("image", { href: "door.svg", width, height }, svg);
    made("path", { d: arch, fill: "url(#entrance-light)" }, svg);
    const leaves = ["entrance-left", "entrance-right"].map((clip) => {
      const leaf = made("g", { "clip-path": `url(#${clip})` }, svg);
      made("image", { href: "door.svg", width, height }, leaf);
      return made("g", {}, svg).appendChild(leaf).parentNode;
    });

    // Blood from the eyes, and the mouth that opens and pours.
    const blood = token("blood-edge");
    const streams = eyes.map(([x, y]) =>
      made("rect", { x: x - 1.5, y, width: 3, height: 64, fill: blood, class: "entrance-grows" }, svg),
    );
    const gape = made(
      "ellipse",
      { cx: mouth[0], cy: mouth[1], rx: 9, ry: 7, fill: token("shadow"), class: "entrance-opens" },
      svg,
    );
    const pour = made(
      "rect",
      {
        x: mouth[0] - 4,
        y: mouth[1],
        width: 8,
        height: foot - mouth[1],
        fill: blood,
        class: "entrance-grows",
      },
      svg,
    );

    veil.append(svg);
    document.body.append(veil);

    const at = (start, length, easing = "ease-in") => ({
      delay: start,
      duration: length,
      easing,
      fill: "both",
    });
    const running = [
      ...streams.map((stream, index) =>
        stream.animate({ transform: ["scaleY(0)", "scaleY(1)"] }, at(300 + index * 150, 1500)),
      ),
      gape.animate({ transform: ["scale(0)", "scale(1)"] }, at(1500, 700, "ease-out")),
      pour.animate({ transform: ["scaleY(0)", "scaleY(1)"] }, at(2100, 1100)),
      leaves[0].animate(
        { transform: ["translateX(0)", `translateX(${-half}px)`] },
        at(3200, 1200, "ease-in-out"),
      ),
      leaves[1].animate(
        { transform: ["translateX(0)", `translateX(${half}px)`] },
        at(3200, 1200, "ease-in-out"),
      ),
      svg.animate(
        { transform: ["scale(1)", "scale(9)"] },
        at(4200, 1400, "ease-in"),
      ),
      veil.animate({ opacity: [1, 0] }, at(5000, 600, "linear")),
    ];
    svg.style.transformOrigin = `${(middle / width) * 100}% ${(((spring + foot) / 2) / height) * 100}%`;

    const end = () => {
      for (const animation of running) animation.finish();
    };
    for (const kind of ["pointerdown", "keydown", "wheel"]) {
      addEventListener(kind, end, { once: true, passive: true });
    }
    Promise.all(running.map((animation) => animation.finished)).then(() => {
      veil.remove();
      for (const kind of ["pointerdown", "keydown", "wheel"]) {
        removeEventListener(kind, end);
      }
    });
  }
})();
