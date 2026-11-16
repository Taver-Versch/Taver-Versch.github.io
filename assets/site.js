(() => {
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const toggle = document.querySelector(".theme");
  if (toggle) toggle.addEventListener("click", () => {
    const root = document.documentElement, next = root.dataset.mode === "dark" ? "light" : "dark";
    root.dataset.mode = next;
    root.style.colorScheme = next;
    root.style.background = "";
    keep.set("theme", next);
  });

  const ask = document.querySelector("form.ask[data-mailto]");
  if (ask) ask.addEventListener("submit", (e) => {
    e.preventDefault();
    const f = new FormData(ask), line = (label, key) => (f.get(key) ? `${label}: ${f.get(key)}\n` : "");
    const body = line("Name", "name") + line("Email", "email") + line("Company", "company") + line("Role", "role")
      + (f.get("message") ? "\n" + f.get("message") : "");
    location.href = `mailto:${ask.dataset.mailto}?subject=${encodeURIComponent("Resume request")}&body=${encodeURIComponent(body)}`;
    ask.querySelector(".sent").hidden = false;
  });

  const term = document.querySelector(".term");
  if (term) {
    const screen = term.querySelector(".screen"), idle = screen.querySelector(".idle");
    const cmds = term.querySelector(".cmds"), buttons = [...cmds.querySelectorAll(".cmdbtn")];
    const outputs = [...term.querySelectorAll("template")];
    const toBottom = () => { screen.scrollTop = screen.scrollHeight; };
    const play = (run, done) => {
      const cmd = run.querySelector(".typed-cmd"), text = cmd.textContent, out = [...run.children].slice(1);
      run.hidden = false;
      out.forEach((o) => { o.hidden = true; });
      let i = 0;
      const key = () => {
        cmd.textContent = text.slice(0, ++i);
        if (i < text.length) return setTimeout(key, 55);
        setTimeout(() => { out.forEach((o) => { o.hidden = false; }); toBottom(); setTimeout(done, 250); }, 180);
      };
      cmd.textContent = ""; key();
    };
    const intro = [...screen.querySelectorAll(".run")];
    intro.forEach((r) => { r.hidden = true; });
    const next = () => (intro.length ? play(intro.shift(), next) : (cmds.hidden = false));
    next();
    let busy = false;
    buttons.forEach((b, i) => b.addEventListener("click", () => {
      if (busy) return;
      busy = true;
      const run = document.createElement("div");
      run.className = "run";
      run.innerHTML = '<div class="cmd"></div>';
      run.firstChild.append(screen.querySelector(".prompt").cloneNode(true), " ", Object.assign(document.createElement("span"), { className: "typed-cmd", textContent: b.textContent }));
      run.append(outputs[i].content.cloneNode(true));
      screen.insertBefore(run, idle);
      play(run, () => { busy = false; });
    }));
  }

  const roles = document.querySelector("[data-roles]");
  if (roles) {
    const list = roles.dataset.roles.split("|");
    let r = 0, n = list[0].length, back = false;
    const tick = () => {
      const word = list[r];
      roles.textContent = word.slice(0, n);
      if (!back && n === word.length) { back = true; return setTimeout(tick, 1600); }
      if (back && n === 0) { back = false; r = (r + 1) % list.length; }
      n += back ? -1 : 1;
      setTimeout(tick, back ? 35 : 70);
    };
    tick();
  }

  const filters = document.querySelector(".filters");
  if (filters) {
    const search = filters.querySelector(".search"), chips = [...filters.querySelectorAll(".chip")];
    const cards = [...document.querySelectorAll(".grid .card")], empty = document.querySelector(".empty");
    let tag = "";
    const apply = () => {
      const q = search.value.trim().toLowerCase();
      let shown = 0;
      cards.forEach((c) => {
        const ok = (!tag || c.dataset.tags.split("|").includes(tag)) && (!q || c.textContent.toLowerCase().includes(q));
        c.hidden = !ok;
        if (ok) { shown++; c.classList.add("in"); }
      });
      empty.hidden = shown > 0;
    };
    search.addEventListener("input", apply);
    chips.forEach((chip) => chip.addEventListener("click", () => {
      tag = chip.dataset.tag;
      chips.forEach((c) => c.classList.toggle("on", c === chip));
      apply();
    }));
  }

  if (still) return;
  document.documentElement.classList.add("motion");
  const seen = new IntersectionObserver((items) => items.forEach((it) => {
    if (it.isIntersecting) { it.target.classList.add("in"); seen.unobserve(it.target); }
  }), { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".reveal").forEach((el) => seen.observe(el));
})();
