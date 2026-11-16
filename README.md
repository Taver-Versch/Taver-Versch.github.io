# Taver-Versch.github.io

My portfolio site, built by my own small static site generator. Every section of the site is a folder of
Markdown files, and a GitHub Actions workflow builds and deploys it to GitHub Pages on every push.

## How it works
```
content/                   every folder is a tab, and its number sets the tab order
  01-home/index.md         everything on the home page: every terminal command and what it prints, the buttons,
                           the links under the terminal and the cards
  02-about/
    index.md               your name, tagline, links, the About text, and the photo fields
    mila.png               the polaroid next to the About text
    notes/                 sticky notes (.md files) and extra polaroids (images) under the About text
    info/                  education, certifications, skills: full-text cards at the bottom of About
  03-experience/           one file or folder per job
  04-projects/
    02-homelab/            one folder per project
      index.md             the text
      01-network-diagram.png   drop images here, they show up on the page
  05-posts/                write-ups, a single .md file or a folder like projects (index.md: tab settings)
  contact/index.md         the Contact page text and form settings (no number, so it isn't a tab:
                           it's the Contact button in the corner)
assets/
  style.css, site.js, walker.js
  sprites/                 every pixel-art picture, one PNG each (see the README in there)
templates/page.html the page layout
build.py            turns content/ into the site in _site/
```

**Pages:** the home page is short on purpose: a small terminal that types out who you are, then lets visitors
press buttons to run `ls projects`, `ls posts`, `cat now.txt` or `contact` (no typing), plus a few cards. Each tab is its own page (About, Experience, Projects, Posts), and every project or post with
text gets its own page too. The Projects and Posts pages have a search box and tag filters, so they keep
working when there are dozens of entries.

**Small extras:** every project and post page links to the one before and after it. Lists are compact text rows,
and clicking anywhere on a row opens its page. `404.html` is the page GitHub shows for a bad link.

**Sizes:** everything on the ledge follows one number, `--px` in `assets/style.css` (how big one sprite pixel
is on screen). It's 3 normally, 4 on screens 1500px and wider, and 2 on phones.

**Footer:** every page ends with the same footer: your name and tagline, links to every page, GitHub, LinkedIn
and the studio site (`studio:` in `content/02-about/index.md`), and the contact links. It's built in `build.py`.

**Contact and resume:** there is no resume file on the site. The Contact page has a request form (name,
email, company, role, message).
- Out of the box it needs no setup: pressing the button opens the visitor's email app with everything they
  typed filled in, addressed to you.
- To get requests straight to your inbox instead, make a free form at formspree.io (or any form service
  that gives you a link), then paste the link into `content/contact/index.md` as `form_action: https://...`.

## The home page
Everything on it is in `content/01-home/index.md`. Each `## heading` is a terminal command, and the text under
it is what the command prints (Markdown works: links, **bold**, lists, and each new line shows on its own line).

```
---
host: taver@homelab                        the name in the prompt and the title bar
hint: try a command:                       the text before the buttons
start: whoami, cat status.txt, ./now       typed out by themselves when the page opens
buttons: ls projects, cat now.txt, contact the buttons visitors press, in this order
links: Get in touch = contact.html, GitHub = https://github.com/you
                                           the buttons under the terminal (the first one is highlighted)
cards: Featured project = projects, Latest post = posts
                                           the cards at the bottom: label = which tab folder
---
## whoami
Taver Versch, software engineering student

## ./now
I work on {networking | security | cloud}  words in { } separated by | type out one after another

## ls projects
                                           leave an ls command empty and it lists that tab's folder by itself
```

- Add a command: write a new `## heading` with its text, then add it to `start:` or `buttons:`.
- Hide a command: take it out of `start:` and `buttons:`. The heading can stay.
- The first `start:` command's text is the page's main heading, so keep your name in it.

## Things you change by editing one line
| What | Where | Example |
|---|---|---|
| Which project or post is on the home page | add `featured: yes` to that entry (otherwise the first one) | `featured: yes` |
| Order of the About page | `layout:` in `content/02-about/index.md` | `layout: intro, info, notes` |
| The About polaroid and its caption | `photo:`, `photo_caption:`, `photo_note:` in `content/02-about/index.md` | `photo: mila.png` |
| A sticky note's colour | `color:` in that note (yellow, pink, green, blue, orange, purple, or `#hex`) | `color: blue` |
| Footer studio link | `studio:` in `content/02-about/index.md` | |
| Tab names and order | the folder names in `content/` (`04-side-projects` becomes the tab "Side Projects") | |
| Any sprite | save a PNG over the one in `assets/sprites/` | |
| Colours, day and night (`--accent` is the secondary colour) | the two blocks at the top of `assets/style.css` | |

**Reorder anything:** the number at the start of a file name is its position. Rename
`03-audittool.md` to `01-audittool.md` and it moves to the top. Numbers don't have to be in a row, so
`05`, `10`, `20` leave room to slide things in later.

**Add a project or post:** copy an existing folder, change the number and the text in index.md, commit.
A tab with nothing in it still shows, with a count of 0 and "Nothing here yet."

**Add a whole new tab:** make a numbered folder in `content/`, like `06-volunteering/`, and put .md files
(or folders with an index.md) in it. It gets a tab, a page, a footer link and an `ls volunteering` command.
Nothing in `build.py` changes. The folder can't be named `index`, `media`, `assets` or `404`.

**Row or full text:** every entry picks its own look.
- With a `summary:` line it's a short row, and its text gets its own page (like projects).
- Without one, its whole text shows right on the list (like experience).
- Lists with more than 3 entries get a search box and tag filters.

**Tab settings:** a tab folder can have its own `index.md` (it isn't counted as an entry):
```
---
title: Posts          the tab and page name (otherwise it comes from the folder name)
pictures: yes         rows show their first image, large, on the left. Rows without one fill the width
filters: Python, Docker   the tag buttons above the list, in this order (otherwise the 8 most used tags)
---
Optional text here shows under the page title.
```
`05-posts/index.md` has `pictures: yes`. To give a post a picture, make it a folder (`05-posts/02-my-post/`)
with `index.md` and the image (`01-diagram.png`) inside.

**Add images:** drag them into the project's folder and push. That's it.
- The first image (by number, so name it `01-...`) is the picture on the home page card, if you use cards.
- Images you don't mention in the text show up in a gallery at the bottom of the page, captioned from the
  file name (`02-rack-photo.jpg` becomes "Rack photo").
- To put an image in a specific spot, write `![What it shows](02-rack-photo.jpg)` in index.md.
- Works with .png, .jpg, .jpeg, .gif, .webp, and .svg.

**Fields at the top of a file** (between the `---` lines), all optional except `title`:
`title`, `meta` (dates or role), `summary` (the row text; leave it out to show the full text instead), `tags` (comma separated), `link`,
`link_text`, `image` (to pick a card picture other than the first image). Everything under the second `---` is the page.

**Word files:** GitHub Pages can't read .docx, so write in Markdown. If you draft in Word, paste it into a
.md file, or convert it with `pandoc file.docx -o file.md`.

## The look, the character and the cat
- `assets/style.css` is a plain off-white page with mono headings and thin ink borders.
- The header is a pixel-art grass ledge that holds the tabs. You stand on the tab for the page you're on,
  and the cat sits next to you.
- Hover a tab and you walk toward it (you run if it's 2 or more tabs away), with the cat trailing behind.
  Click it and the next page picks up from where you were standing. A jump of 4 tabs or more, or the first
  page of a visit, is a teleport with a white puff. Standing still you breathe and blink, and after about
  8 seconds you sit.
- All of the art is in `assets/sprites/`, one PNG per frame, with its own README that lists every file and
  its size. Save a new PNG over an old one to change it.
- **Night mode:** click the pixel sun in the sky and it turns into a moon. The site always starts in day, and remembers the
  visitor's choice from page to page. At night the ledge becomes a sidewalk, and a streetlight stands over every other tab (Home,
  Experience, Posts) and lights up its name. The sidewalk and the streetlight are sprites too.
- People with reduced motion turned on get no animations.

## Preview on your PC (optional)
```
pip install -r requirements.txt
python build.py serve
```
Then open http://localhost:8000 (Ctrl+C stops it). Run it again after editing to see changes.
If port 8000 is busy, pick another: `python build.py serve 8001`.

Links have no `.html` (the address bar shows `/posts`, not `/posts.html`). GitHub Pages and Cloudflare
Pages handle that by themselves. Opening the files straight from `_site/` won't follow those links, so use
`serve` to preview. `python build.py` alone just builds `_site/`.

## Put it online
1. Create a public repo named exactly `Taver-Versch.github.io` and upload everything in this folder
   (including the hidden `.github` folder, so drag the whole folder or use GitHub Desktop).
2. Settings > Pages > Source: **GitHub Actions**.
3. Push or edit any file. The Actions tab shows the build, and the site goes live at
   https://taver-versch.github.io in about a minute.

## Your own domain later
**Keep GitHub Pages, add a domain** (simplest):
1. Buy the domain (Cloudflare Registrar sells at cost). In GitHub, verify it first: your profile Settings > Pages > Add a domain.
2. Repo Settings > Pages > Custom domain: type the domain and Save. (No `CNAME` file is needed: this site deploys
   with Actions, and GitHub ignores that file.)
3. In Cloudflare DNS add four A records for the bare domain (`@`): 185.199.108.153, 185.199.109.153,
   185.199.110.153, 185.199.111.153, and a CNAME record `www` pointing to `taver-versch.github.io`.
   Set them to "DNS only" (grey cloud) at first so GitHub can issue the HTTPS certificate.
4. Back in Settings > Pages, tick Enforce HTTPS once it becomes available (can take up to a day).

**Or move hosting to Cloudflare Pages** (also free):
1. Cloudflare dashboard > Workers & Pages > create a Pages project > connect this GitHub repo.
2. Build command: `pip install -r requirements.txt && python build.py`. Output directory: `_site`.
3. Add your domain under the project's Custom domains tab. Cloudflare sets up DNS and HTTPS for you.
4. Turn off GitHub Pages (Settings > Pages) so the site isn't published in two places.
