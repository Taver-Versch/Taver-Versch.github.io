import datetime
import html
import re
import shutil
import sys
from pathlib import Path

import markdown

esc = html.escape

ROOT = Path(__file__).parent
SPECIAL = ("home", "about", "contact")

TYPED = re.compile(r"\{([^{}]*\|[^{}]*)\}")
FRONT = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.S)
PREFIX = re.compile(r"^(\d+)[-_ ]*")
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
NOTE_COLORS = {"yellow": "oklch(95.88% 0.1093 102.6)", "pink": "oklch(90.32% 0.0535 2.2)", "green": "oklch(91.91% 0.0561 154.6)", "blue": "oklch(90.77% 0.0469 248.3)",
               "orange": "oklch(90.39% 0.0758 72.4)", "purple": "oklch(89.48% 0.0601 300.1)"}

ICONS = {"python": "python", "django": "django", "typescript": "typescript", "javascript": "javascript",
         "java": "openjdk", "c#": "csharp", "docker": "docker", "aws": "amazonaws", "unity": "unity",
         "cloudflare": "cloudflare", "linux": "linux", "git": "git", "github actions": "githubactions",
         "ci/cd": "githubactions", "wireshark": "wireshark", "raspberry pi": "raspberrypi",
         "blender": "blender", "bash": "gnubash", "html": "html5", "css": "css3", "markdown": "markdown",
         "sql": "mysql", "kali": "kalilinux", "networking": "cisco", "proxmox ve": "proxmox",
         "pi-hole": "pihole", "wireguard": "wireguard", "puppeteer": "puppeteer", "excel": "microsoftexcel",
         "tailscale": "tailscale", "nginx": "nginx", "home assistant": "homeassistant",
         "nextcloud": "nextcloud", "ubuntu": "ubuntu"}
EXTERNAL = re.compile(r'(<a\b[^>]*?) href="(https?://)')
PAGE_LINK = re.compile(r'href="([a-z0-9-]+)\.html([#?][^"]*)?"')
LOCAL_SRC = re.compile(r'(src|href)="(?![a-z]+:|/|#|assets/|media/)([^"]+)"')


def order(path):
    m = PREFIX.match(path.stem)
    return (int(m.group(1)) if m else float("inf"), path.stem.lower())


def caption(path):
    return PREFIX.sub("", path.stem).replace("-", " ").replace("_", " ").strip().capitalize()


def read(path, folder=None):
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    m = FRONT.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                value = value.strip()
                if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                meta[key.strip().lower()] = value
        body = m.group(2)
    meta["slug"] = re.sub(r"[^a-z0-9]+", "-", PREFIX.sub("", (folder or path).stem).lower()).strip("-") or "page"
    meta.setdefault("title", meta["slug"].replace("-", " ").title())
    meta["body"] = markdown.markdown(body, extensions=["tables", "fenced_code"])
    meta["images"] = sorted((f for f in folder.iterdir() if f.suffix.lower() in IMAGES), key=order) if folder else []
    if folder:
        media = f"media/{meta['slug']}/"
        meta["body"] = LOCAL_SRC.sub(lambda m: f'{m.group(1)}="{media}{m.group(2)}"' if (folder / html.unescape(m.group(2))).is_file()
                                     else m.group(0), meta["body"])
        used = set(re.findall(r'src="' + re.escape(media) + r'([^"]+)"', meta["body"]))
        extra = [f for f in meta["images"] if f.name not in used]
        if extra:
            meta["body"] += '<div class="gallery">' + "".join(
                f'<figure><a href="{media}{esc(f.name)}"><img src="{media}{esc(f.name)}" alt="{esc(caption(f))}"></a>'
                f"<figcaption>{esc(caption(f))}</figcaption></figure>" for f in extra) + "</div>"
        if meta["images"] and "image" not in meta:
            meta["image"] = media + meta["images"][0].name
    meta["has_body"] = bool(body.strip()) or bool(meta["images"])
    meta["dir"] = bool(folder)
    return meta


def slug(path):
    return PREFIX.sub("", path.name).lower()


def label(s):
    return s.replace("-", " ").title()


def pairs(value):
    return [(a.strip(), c.strip()) for a, _, c in (x.partition("=") for x in names(value))]


def own_page(e):
    return bool(e.get("summary")) and e["has_body"]


def entries(folder):
    if not folder.is_dir():
        return []
    items = []
    for p in sorted(folder.iterdir(), key=order):
        if p.suffix == ".md" and p.name != "index.md":
            e = read(p)
            pic = next((p.with_suffix(s) for s in sorted(IMAGES) if p.with_suffix(s).is_file()), None)
            if pic:
                e["images"] = [pic]
                e.setdefault("image", f"media/{e['slug']}/{pic.name}")
            items.append(e)
        elif p.is_dir():
            md = p / "index.md" if (p / "index.md").exists() else next(iter(sorted(p.glob("*.md"))), None)
            if md:
                items.append(read(md, folder=p))
    return items


def names(value):
    return [x.strip() for x in (value or "").split(",") if x.strip()]


def bubbles(e):
    out = []
    for tag in names(e.get("tags")):
        icon = ICONS.get(tag.lower())
        img = f'<img src="assets/icons/{icon}.svg" alt="" loading="lazy">' if icon else ""
        out.append(f'<span class="skill">{img}{esc(tag)}</span>')
    return f'<div class="tags">{"".join(out)}</div>' if out else ""


def outside_link(e, text="View on GitHub"):
    return f'<a href="{esc(e["link"])}">{esc(e.get("link_text", text))}</a>' if e.get("link") else ""


def polaroid(p, out, text, note=""):
    (out / "media" / "about").mkdir(parents=True, exist_ok=True)
    shutil.copy(p, out / "media" / "about" / p.name)
    return (f'<figure class="tile photo"><img src="media/about/{esc(p.name)}" alt="{esc(text)}">'
            f"<figcaption>{esc(text)}{f'<small>{esc(note)}</small>' if note else ''}</figcaption></figure>")


def collage(folder, out, skip=None):
    tiles = []
    for p in sorted(folder.iterdir(), key=order):
        if p.suffix == ".md" and p.name != "index.md":
            e = read(p)
            color = e.get("color", "").lower()
            if color and color not in NOTE_COLORS and not re.fullmatch(r"#[0-9a-f]{3}|#[0-9a-f]{6}|oklch\([\d.%\s/]+\)", color):
                sys.exit(f"{p}: color can be {', '.join(NOTE_COLORS)}, a hex code like #ffd1dc, or oklch(88% 0.06 0).")
            style = f' style="--paper: {NOTE_COLORS.get(color, color)}"' if color else ""
            tiles.append(f'<div class="tile note"{style}><h3>{esc(e["title"])}</h3>{e["body"]}</div>')
        elif p.suffix.lower() in IMAGES and p != skip:
            tiles.append(polaroid(p, out, caption(p)))
    return f'<div class="collage reveal">{"".join(tiles)}</div>' if tiles else ""


def yes(value):
    return str(value).strip().lower() in ("yes", "true")


def card(e, pictures=False):
    links = [outside_link(e)] if e.get("link") else []
    title = esc(e["title"])
    if e.get("summary"):
        kind, inline = "row", f"<p>{esc(e['summary'])}</p>"
        if own_page(e):
            title = f'<a class="stretch" href="{e["slug"]}.html">{title}</a>'
    else:
        kind, inline = "full", e["body"]
    shot = f'<img class="shot" src="{esc(e["image"])}" alt="" loading="lazy">' if kind == "row" and pictures and e.get("image") else ""
    return (f'<article class="card {kind} reveal" data-tags="{esc("|".join(names(e.get("tags"))))}">{shot}<h3>{title}</h3>'
            + (f'<div class="meta">{esc(e["meta"])}</div>' if e.get("meta") else "") + inline + bubbles(e)
            + (f'<p class="links">{" · ".join(links)}</p>' if links else "") + "</article>")


def badge(e):
    art = (f'<img class="badge-art" src="{esc(e["image"])}" alt="" loading="lazy">' if e.get("image")
           else '<div class="badge-art blank" aria-hidden="true"></div>')
    status = f'<span class="status-pill">{esc(e["status"])}</span>' if e.get("status") else ""
    link = f'<a class="btn view" href="{esc(e["link"])}">{esc(e.get("link_text", "View"))}</a>' if e.get("link") else ""
    pending = " pending" if e.get("status") else ""
    return (f'<article class="card badge{pending} reveal" data-tags="{esc("|".join(names(e.get("tags"))))}">{art}<h3>{esc(e["title"])}</h3>'
            + (f'<div class="meta">{esc(e["meta"])}</div>' if e.get("meta") else "") + status + link + "</article>")


def teaser(label, e, href, more_href, more_text):
    img = f'<img class="shot" src="{esc(e["image"])}" alt="">' if e.get("image") else ""
    blurb = e.get("summary") or e.get("meta", "")
    return (f'<div class="teaser reveal"><div class="label">{label}</div>{img}'
            f'<a class="title" href="{href}">{esc(e["title"])}</a><p>{esc(blurb)}</p>'
            f'<a class="more" href="{more_href}">{more_text} &rarr;</a></div>')


def listing(title, section, items, cfg):
    counts = {}
    for e in items:
        for t in names(e.get("tags")):
            counts[t] = counts.get(t, 0) + 1
    tags = names(cfg.get("filters")) or sorted(counts, key=lambda t: (-counts[t], t.lower()))[:8]
    unused = [t for t in tags if t not in counts]
    if unused:
        sys.exit(f"{section}/index.md: filters: no entry is tagged '{unused[0]}'. Tags in use: {', '.join(sorted(counts))}.")
    chips = "".join(f'<button type="button" class="chip" data-tag="{esc(t)}">{esc(t)}</button>' for t in tags)
    tools = (f'<div class="filters"><input type="search" class="search" placeholder="Search {section}" aria-label="Search {section}">'
             f'<button type="button" class="chip on" data-tag="">All</button>{chips}</div>') if len(items) > 3 else ""
    intro = f'<div class="body lead">{cfg["body"]}</div>' if cfg.get("body", "").strip() else ""
    badges = cfg.get("layout", "list") == "badges"
    if cfg.get("layout", "list") not in ("list", "badges"):
        sys.exit(f"{section}/index.md: layout can be list or badges.")
    return (f'<h1 class="page-title">{esc(title)} <span class="count">{len(items)}</span></h1>{intro}{tools}'
            f'<div class="grid{" badges" if badges else ""}">{"".join(badge(e) if badges else card(e, yes(cfg.get("pictures"))) for e in items)}</div>'
            + ('<p class="empty" hidden>Nothing matches that.</p>' if items else '<p class="empty">Nothing here yet.</p>'))


def build(content=ROOT / "content", out=ROOT / "_site", templates=ROOT / "templates", assets=ROOT / "assets"):
    page = (templates / "page.html").read_text(encoding="utf-8")
    dirs = {slug(p): p for p in sorted((p for p in content.iterdir() if p.is_dir()), key=order)}
    if not (dirs.get("about", content) / "index.md").exists():
        sys.exit("content/ needs an about folder (like 02-about/) with an index.md in it.")
    about_dir = dirs["about"]
    about = read(about_dir / "index.md")
    sections = {s: entries(p) for s, p in dirs.items() if s not in SPECIAL}
    cfgs = {s: read(dirs[s] / "index.md") if (dirs[s] / "index.md").exists() else {} for s in sections}
    for cfg in cfgs.values():
        if cfg.get("title") == "Index":
            del cfg["title"]
    label = lambda s: cfgs.get(s, {}).get("title") or s.replace("-", " ").title()
    clash = {"index", "404", "media", "assets"} & set(sections)
    if clash:
        sys.exit(f"content/: a folder can't be named '{clash.pop()}'. Rename it.")
    name = about["title"]
    tabs = [("index" if s == "home" else s, "Home" if s == "home" else cfgs.get(s, {}).get("tab") or label(s))
            for s in dirs if s != "contact"]
    out.mkdir(parents=True, exist_ok=True)
    for old in out.iterdir():
        shutil.rmtree(old) if old.is_dir() else old.unlink()

    def column(title, items):
        links = "".join(f'<a href="{esc(u)}">{n}</a>' for n, u in items if u)
        return f'<div><h2>{title}</h2>{links}</div>' if links else ""

    studio = about.get("studio")
    footer = ('<footer class="foot"><div class="wrap cols">'
              f'<div class="me"><img class="pixel" src="assets/sprites/cat/sit.png" alt="" width="54" height="39">'
              f'<strong>{esc(name)}</strong><p>{esc(about.get("tagline", ""))}</p></div>'
              + column("Pages", [(label, f"{file}.html") for file, label in tabs])
              + column("Elsewhere", [("GitHub", about.get("github")), ("LinkedIn", about.get("linkedin")),
                                     ("Amtav Games", studio)])
              + column("Contact", [("Email me", "mailto:" + about["email"] if about.get("email") else None),
                                   ("Request my resume", "contact.html")])
              + f'</div><p class="wrap fine">&copy; {datetime.date.today().year} {esc(name)}. '
              'Built from Markdown with my own Python site generator.</p></footer>')

    about_line = f'{name}. {about.get("tagline", "")}'.strip()

    console = next((f for f in sorted((assets / "fonts").glob("Monocraft.*")) if f.suffix in (".woff2", ".woff", ".ttf", ".otf")), None) \
        if (assets / "fonts").is_dir() else None
    fonts = (f'<style>@font-face {{ font-family: Monocraft; src: url(assets/fonts/{console.name}); font-display: swap; }}</style>'
             if console else "")

    def render(title, body, active, description=""):
        nav = "".join(f'<a class="tab{" active" if file == active else ""}" href="{file}.html">{label}</a>' for file, label in tabs)
        return (page.replace("{{title}}", esc(title)).replace("{{name}}", esc(name)).replace("{{nav}}", nav)
                .replace("{{description}}", esc(description or about_line)).replace("{{fonts}}", fonts)
                .replace("{{footer}}", footer).replace("{{contact_active}}", " active" if active == "contact" else "")
                .replace("{{content}}", body))

    def write(file, title, body, active=None, description=""):
        html_out = EXTERNAL.sub(r'\1 target="_blank" rel="noopener" href="\2', render(title, body, active or file, description))
        html_out = PAGE_LINK.sub(lambda m: f'href="{"./" if m.group(1) == "index" else m.group(1)}{m.group(2) or ""}"', html_out)
        (out / f"{file}.html").write_text(html_out, encoding="utf-8")

    home_md = dirs.get("home", content) / "index.md"
    if not home_md.exists():
        sys.exit("content/ needs a home folder (like 01-home/) with an index.md in it.")
    home = read(home_md)
    where = f"content/{home_md.parent.name}/index.md"
    raw = home_md.read_text(encoding="utf-8")
    parts = re.split(r"^## +(.+?) *$", FRONT.match(raw).group(2) if FRONT.match(raw) else raw, flags=re.M)
    said = {cmd: text.strip() for cmd, text in zip(parts[1::2], parts[2::2])}
    host = home.get("host", "~")
    prompt = f'<span class="prompt">{esc(host)}:~$</span> '

    def run(cmd, out):
        return f'<div class="run"><div class="cmd">{prompt}<span class="typed-cmd">{esc(cmd)}</span></div>{out}</div>'

    def ls(s):
        return '<div class="out ls">' + "".join(
            f'<a href="{e["slug"] if own_page(e) else s}.html">{esc(e["slug"])}{"/" if e["dir"] else ".md"}</a>'
            for e in sections[s]) + "</div>"

    def typed(m):
        words = [html.unescape(w.strip()) for w in m.group(1).split("|")]
        return f'<span class="typed" data-roles="{esc("|".join(words))}">{esc(words[0])}</span>'

    def output(cmd, text, tag="div"):
        if not text and cmd.startswith("ls ") and cmd[3:] in sections:
            return ls(cmd[3:])
        body = TYPED.sub(typed, markdown.markdown(text, extensions=["nl2br"]))
        if tag == "h1":
            body = re.sub(r"</?p>", "", body)
        return f'<{tag} class="out bright">{body}</{tag}>'

    first, picked = names(home.get("start")), names(home.get("buttons"))
    for field, cmds in (("start", first), ("buttons", picked)):
        unknown = [c for c in cmds if c not in said]
        if unknown:
            sys.exit(f"{where}: {field}: there's no '## {unknown[0]}' heading below. Headings: {', '.join(said)}.")
    intro = "".join(run(c, output(c, said[c], "h1" if i == 0 else "div")) for i, c in enumerate(first))
    buttons = "".join(f'<button class="cmdbtn" type="button" data-i="{i}">{esc(c)}</button>' for i, c in enumerate(picked))
    outputs = "".join(f"<template>{output(c, said[c])}</template>" for c in picked)
    hint = f'<span class="hint">{esc(home["hint"])}</span>' if home.get("hint") else ""
    terminal = (f'<section class="term" aria-label="Terminal"><div class="term-bar" aria-hidden="true"><i></i><i></i><i></i>{esc(host)}: ~</div>'
                f'<div class="screen" aria-live="polite">{intro}<div class="cmd idle" aria-hidden="true">{prompt}<span class="cursor"></span></div></div>'
                f'<div class="cmds" hidden>{hint}{buttons}</div>{outputs}</section>')
    actions = "".join(f'<a class="btn{" primary" if i == 0 else ""}" href="{esc(u)}">{esc(n)}</a>'
                      for i, (n, u) in enumerate(pairs(home.get("links"))) if u)
    hero = f'<header class="hero">{terminal}' + (f'<div class="buttons">{actions}</div>' if actions else "") + "</header>"
    teasers = []
    for top, s in pairs(home.get("cards")):
        if s not in sections:
            sys.exit(f"{where}: cards: '{s}' isn't a folder in content/. Use: {', '.join(sections)}.")
        if sections[s]:
            e = next((x for x in sections[s] if x.get("featured", "").lower() in ("yes", "true")), sections[s][0])
            href = f'{e["slug"]}.html' if own_page(e) else f"{s}.html"
            n = len(sections[s])
            teasers.append(teaser(esc(top), e, href, f"{s}.html", f"See all {n}" if n > 1 else f"See {label(s)}"))
    write("index", name, hero + (f'<div class="teasers">{"".join(teasers)}</div>' if teasers else ""))

    info_entries = entries(about_dir / "info")
    cert_entries = entries(about_dir / "certifications")
    certs = (f'<div class="stack"><div class="card full certs"><h3>Certifications</h3>'
             f'<div class="grid badges">{"".join(badge(e) for e in cert_entries)}</div></div></div>') if cert_entries else ""
    info = "".join(card(e) for e in info_entries)
    pics = sorted((f for f in about_dir.iterdir() if f.suffix.lower() in IMAGES), key=order)
    photo = about_dir / about["photo"] if about.get("photo") else (pics[0] if pics else None)
    if photo and not photo.is_file():
        sys.exit(f"content/{about_dir.name}/index.md: photo: {about['photo']} is not in that folder.")
    side = polaroid(photo, out, about.get("photo_caption") or caption(photo), about.get("photo_note", "")) if photo else ""
    blocks = {"intro": f'<div class="intro"><div class="body">{about["body"]}</div>{side}</div>',
              "notes": collage(about_dir / "notes", out) if (about_dir / "notes").is_dir() else "",
              "info": f'<div class="stack">{info}</div>' if info else "",
              "certs": certs}
    layout = names(about.get("layout", "intro, notes, info, certs"))
    if set(layout) - set(blocks):
        sys.exit(f"content/{about_dir.name}/index.md: layout can only list {', '.join(blocks)}.")
    write("about", f"About · {name}", '<h1 class="page-title">About</h1>' + "".join(blocks[b] for b in layout))
    for s, items in sections.items():
        write(s, f"{label(s)} · {name}", listing(label(s), s, items, cfgs[s]))

    contact_md = dirs.get("contact", content) / "index.md"
    contact = read(contact_md) if contact_md.exists() else {"title": "Contact", "body": ""}
    mail = esc(about.get("email", ""))
    ways = [("Email", f"mailto:{mail}", mail)] if mail else []
    links = [("GitHub", about.get("github")), ("LinkedIn", about.get("linkedin"))]
    ways += [(n, u, u.split("//")[-1].rstrip("/")) for n, u in links if u]
    rows = "".join(f'<div class="way"><div class="label">{n}</div><a href="{esc(u)}">{esc(text)}</a></div>' for n, u, text in ways)
    form = ""
    if contact.get("form_action") or mail:
        target = (f'action="{esc(contact["form_action"])}" method="post"' if contact.get("form_action") else
                  f'action="mailto:{mail}?subject=Resume%20request" method="post" enctype="text/plain" data-mailto="{mail}"')
        field = lambda label, name, kind="text", need="": (
            f'<label>{label}<input type="{kind}" name="{name}" autocomplete="{"email" if kind == "email" else "on"}"{need}></label>')
        form = (f'<form class="ask" {target}><h2>Request my resume</h2><p>{esc(contact.get("resume_note", "Sent on request."))}</p>'
                + field("Your name", "name", need=" required") + field("Your email", "email", "email", " required")
                + field("Company", "company") + field("Role you're hiring for", "role")
                + '<label>Anything else<textarea name="message" rows="3"></textarea></label>'
                '<input type="hidden" name="_subject" value="Resume request">'
                '<button class="btn primary" type="submit">Request my resume</button>'
                f'<p class="sent" hidden>Your email app should open with this filled in. If nothing happens, email me at {mail}.</p></form>')
    write("contact", f"Contact · {name}", f'<h1 class="page-title">{esc(contact["title"])}</h1><div class="contact-grid">'
          f'<div><div class="body">{contact["body"]}</div><div class="ways">{rows}</div></div>{form}</div>')

    seen = set(dirs) | {"index", "404"}
    for s, items in sections.items():
        pages = [e for e in items if own_page(e)]
        for i, e in enumerate(pages):
            if e["slug"] in seen:
                sys.exit(f"Two pages are named '{e['slug']}'. Rename one of the files or folders in content/.")
            seen.add(e["slug"])
            meta = f'<div class="meta">{esc(e["meta"])}</div>' if e.get("meta") else ""
            link = f'<p class="links">{outside_link(e)}</p>' if e.get("link") else ""
            step = "".join(f'<a class="{side}" href="{o["slug"]}.html"><span>{word}</span>{esc(o["title"])}</a>'
                           for side, word, o in (("prev", "&larr; Previous", pages[i - 1] if i else None),
                                                 ("next", "Next &rarr;", pages[i + 1] if i + 1 < len(pages) else None)) if o)
            article = (f'<article class="post"><a class="back" href="{s}.html">&larr; All {s}</a><h1>{esc(e["title"])}</h1>{meta}'
                       f'{bubbles(e)}{e["body"]}{link}<nav class="step" aria-label="More {s}">{step}</nav></article>')
            write(e["slug"], f'{e["title"]} · {name}', article, active=s, description=e.get("summary", ""))

    write("404", f"Page not found · {name}", '<div class="lost"><h1 class="page-title">This page wandered off.</h1>'
          '<p>The link is old or mistyped. The cat and I looked everywhere.</p>'
          '<a class="btn primary" href="index.html">Back to the home page</a></div>', active="none")

    for items in [*sections.values(), info_entries, cert_entries]:
        for e in items:
            for img in e["images"]:
                (out / "media" / e["slug"]).mkdir(parents=True, exist_ok=True)
                shutil.copy(img, out / "media" / e["slug"] / img.name)

    if assets.is_dir():
        shutil.copytree(assets, out / "assets")
    if (ROOT / "CNAME").exists():
        shutil.copy(ROOT / "CNAME", out / "CNAME")
    return out


if __name__ == "__main__":
    site = build()
    print("Built", site)
    if sys.argv[1:2] == ["serve"]:
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        import functools
        import http.server

        class Pages(http.server.SimpleHTTPRequestHandler):
            def send_head(self):
                path = self.path.split("?")[0]
                if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
                    self.path = path + ".html"
                return super().send_head()

        print(f"Open http://localhost:{port} (Ctrl+C stops it)")
        http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(Pages, directory=site)).serve_forever()
