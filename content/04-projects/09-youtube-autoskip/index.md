---
title: YoutubeAutoSkip
meta: December 2025 | Python
summary: A Python desktop tool that watches a chosen part of the screen and clicks a button when the text you pick shows up there.
tags: Python, OpenCV, Tesseract OCR, Automation
link: https://github.com/Taver-Versch/YoutubeAutoSkip
---
> **Note:** This was made for a pretty specific problem I had, but it works for any button with text on it, anywhere on the screen.

I like having YouTube videos playing on my PC while I do other things, but I kept having to walk back to my desk just to skip the ads. So, I made a small Python app that skips them for me.

## How it works
First, you pick an area of the screen and the text to look for (like "Skip"). Then, the app captures that area, cleans up the image, and reads the text in it. Finally, when the text shows up, it clicks it for you.

## Libraries
- **pyautogui:** captures the screen and clicks.
- **OpenCV:** preprocesses the image so the text is easier to read.
- **Tesseract (pytesseract):** reads the text.
- **Pillow:** handles the images.
