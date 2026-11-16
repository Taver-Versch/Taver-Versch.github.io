(() => {
  const DIR = "assets/sprites/";
  let SCALE = 3;
  const FRAMES = {
    taver: ["stand", "breathe", "blink", "sit", "walk1", "walk2", "run1", "run2"],
    cat: ["sit", "sit2", "walk1", "walk2"],
  };
  const WALK = 2.4, RUN = 6, CAT_GAP = 46;

  const stage = document.querySelector(".stage"), canvas = document.querySelector(".lane");
  const tabs = [...document.querySelectorAll(".stage .tab")];
  if (!stage || !canvas || !tabs.length) return;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const g = canvas.getContext("2d");

  const img = {};
  const loads = Object.entries(FRAMES).flatMap(([who, names]) => names.map((n) => new Promise((done) => {
    const i = new Image();
    i.onload = i.onerror = done;
    i.src = `${DIR}${who}/${n}.png`;
    img[`${who}/${n}`] = i;
  })));

  const center = (t) => { const r = t.getBoundingClientRect(); return r.left - stage.getBoundingClientRect().left + r.width / 2; };
  const active = tabs.findIndex((t) => t.classList.contains("active"));
  const home = () => (active >= 0 ? center(tabs[active]) : stage.offsetWidth - 34);
  const step = () => (tabs.length > 1 ? center(tabs[1]) - center(tabs[0]) : 100);

  let x, catX, target, face = 1, catFace = 1, idle = 0, tick = 0, puff = 0, running = false;
  function size() {
    SCALE = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--px")) || 3;
    canvas.width = stage.offsetWidth; canvas.height = canvas.offsetHeight;
    g.imageSmoothingEnabled = false;
  }
  function start() {
    size();
    target = home();
    const from = parseFloat(keep.get("walker-x", true));
    if (still || !(from >= 0 && from <= 1) || Math.abs(from * stage.offsetWidth - target) > step() * 3.5) {
      x = target; if (!still) puff = 18;
    } else x = from * stage.offsetWidth;
    catX = x - CAT_GAP * SCALE / 3;
    running = Math.abs(target - x) > step() * 1.5;
    requestAnimationFrame(frame);
  }
  let hovered = null;
  const spot = () => (hovered ? center(hovered) : home());
  const go = (t) => { hovered = t; target = spot(); running = Math.abs(target - x) > step() * 1.5; };
  let finger = false, leaving = null;
  const leave = () => { if (leaving) { const href = leaving.href; leaving = null; location.href = href; } };
  addEventListener("pointerdown", (e) => { finger = e.pointerType !== "mouse"; }, true);
  tabs.forEach((t) => {
    t.addEventListener("pointerenter", () => go(t));
    t.addEventListener("focus", () => go(t));
    t.addEventListener("pointerleave", (e) => { if (e.pointerType === "mouse") go(null); });
    t.addEventListener("blur", () => { if (!leaving) go(null); });
    t.addEventListener("click", (e) => {
      if (!finger || still || e.ctrlKey || e.metaKey || e.shiftKey) return;
      e.preventDefault();
      leaving = t; go(t);
      setTimeout(leave, 1500);
    });
  });
  addEventListener("pagehide", () => keep.set("walker-x", x / stage.offsetWidth, true));
  addEventListener("pageshow", (e) => { if (e.persisted && x !== undefined) go(null); });

  function realign() {
    if (x === undefined) return;
    const settled = Math.abs(x - target) < 1;
    size();
    target = spot();
    if (settled || still) { x = target; catX = x - CAT_GAP * SCALE / 3 * face; }
  }
  if ("ResizeObserver" in window) { const ro = new ResizeObserver(realign); tabs.forEach((t) => ro.observe(t)); }
  addEventListener("resize", realign);
  if (document.fonts) document.fonts.ready.then(realign);

  function draw(key, cx, flip) {
    const i = img[key];
    if (!i || !i.naturalWidth) return;
    const w = i.naturalWidth * SCALE, h = i.naturalHeight * SCALE;
    g.save();
    g.translate(Math.round(cx), canvas.height - h);
    if (flip) g.scale(-1, 1);
    g.drawImage(i, -w / 2, 0, w, h);
    g.restore();
  }
  function drawPuff(cx, r, alpha) {
    const u = SCALE, ox = Math.round(cx), cy = canvas.height - 15 * u;
    const snap = (v, from) => from + Math.round((v - from) / u) * u;
    r *= u / 3;
    for (const [color, grow] of [["oklch(70.09% 0.0186 248.1 / " + alpha + ")", u], ["oklch(100% 0 0 / " + alpha + ")", 0]]) {
      g.fillStyle = color;
      for (let a = 0; a < 10; a++) {
        const px = snap(ox + Math.cos(a * 0.628) * r, ox), py = snap(cy + Math.sin(a * 0.628) * r * 0.9, cy);
        g.fillRect(px - 3 * u - grow, py - 3 * u - grow, 6 * u + grow * 2, 6 * u + grow * 2);
      }
      g.fillRect(ox - 5 * u - grow, cy - 5 * u - grow, 10 * u + grow * 2, 10 * u + grow * 2);
    }
  }

  let last = 0;
  function frame(now) {
    requestAnimationFrame(frame);
    if (now - last < 15) return;
    last = now;
    tick++;
    const zoom = SCALE / 3;
    const d = target - x, speed = (running ? RUN : WALK) * zoom;
    let pose;
    if (Math.abs(d) > speed && !still) {
      x += Math.sign(d) * speed; face = Math.sign(d); idle = 0;
      pose = (running ? "run" : "walk") + ((tick >> (running ? 2 : 3)) % 2 + 1);
    } else {
      x = target; idle++;
      if (leaving) leave();
      if (still) pose = "stand";
      else if (idle > 60 * 8) pose = "sit";
      else if (idle % 200 > 192) pose = "blink";
      else pose = idle % 70 < 35 ? "stand" : "breathe";
    }
    const edge = 9 * SCALE;
    const spot = Math.min(canvas.width - edge, Math.max(edge, x - CAT_GAP * zoom * face));
    const cd = spot - catX, catSpeed = (Math.abs(cd) > 120 * zoom ? 5 : 2.2) * zoom;
    let catPose;
    if (Math.abs(cd) > catSpeed && !still) {
      catX += Math.sign(cd) * catSpeed; catFace = Math.sign(cd);
      catPose = "walk" + ((tick >> (catSpeed > 3 * zoom ? 2 : 3)) % 2 + 1);
    } else {
      if (still) catX = spot;
      catFace = Math.sign(x - catX) || 1;
      catPose = idle % 160 > 140 ? "sit2" : "sit";
    }

    g.clearRect(0, 0, canvas.width, canvas.height);
    draw("cat/" + catPose, catX, catFace < 0);
    if (puff > 8) drawPuff(x, (18 - puff) * 3, 1);
    else {
      draw("taver/" + pose, x, face < 0 && /walk|run/.test(pose));
      if (puff > 0) drawPuff(x, 30 + (8 - puff) * 3, puff / 8);
    }
    if (puff > 0) puff--;
  }
  Promise.all(loads).then(start);
})();
