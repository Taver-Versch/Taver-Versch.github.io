# Taver-Versch.github.io

My portfolio site, live at **https://taver-versch.github.io**.

It's built with my own small static site generator. Every page comes from a folder of Markdown files, and a Python script turns them into HTML. On every push, GitHub Actions builds the site and deploys it to GitHub Pages.

## How it works
```
content/          the whole site, written in Markdown
  01-home/        the home page terminal
  02-about/       about text, sticky notes, education and skills
  03-experience/  one entry per job
  04-projects/    one folder per project, with its images
  05-posts/       write-ups
  contact/        the contact page
assets/           CSS, JavaScript, and the pixel art sprites
templates/        the page layout
build.py          turns content/ into the site in _site/
```

- Every numbered folder in `content/` becomes a tab, and the number sets the order.
- Each project or post is a Markdown file or a folder with an `index.md` and its images.
- The pixel art character and cat in the header walk to whichever tab you hover, and the sun switches the site to night mode.

## Run it locally
```
pip install -r requirements.txt
python build.py serve
```
Then open http://localhost:8000.

## Built with
Python, Markdown, plain HTML/CSS/JavaScript, and GitHub Actions. The only dependency is the `markdown` package.
