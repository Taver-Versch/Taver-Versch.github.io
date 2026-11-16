---
title: This Site
meta: November 2026 | Python, GitHub Actions
summary: My own small static site generator. Folders of Markdown files become this site, and renaming a file reorders it.
tags: Python, Markdown, GitHub Actions, CI/CD
link: https://github.com/Taver-Versch/Taver-Versch.github.io
link_text: Source on GitHub
---
> **Note:** This site is a work in progress, I keep adding to it as I finish more projects.

This site is basically my own small static site generator. Every page on here comes from a folder of Markdown files, and a Python script (`build.py`) turns them into HTML. I wanted something where I could just write a file and have it show up, without touching any code.

## How it works
- **Folders are tabs:** every numbered folder in `content/` becomes a tab, and the number sets the order. Renaming `05-posts` to `03-posts` moves the tab.
- **Files are entries:** each project or post is a Markdown file, or a folder with an `index.md` and its images. Giving it a `summary:` line gets it a row on the list and its own page.
- **Home page terminal:** the terminal on the home page is one Markdown file, each `## heading` is a command and the text under it is what it prints.
- **Deploying:** on every push, a GitHub Actions workflow builds the site and deploys it to GitHub Pages, so adding a project is pretty much just writing a file and committing it.

## The pixel art
The character and the cat in the header are pixel art. Each frame is its own image file, so I can redraw them whenever I want. Hovering a tab makes me walk (or run) over to it with the cat following behind, and clicking the sun switches the site to night mode, where the grass turns into a sidewalk with streetlights.
