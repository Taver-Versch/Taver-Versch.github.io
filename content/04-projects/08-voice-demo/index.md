---
title: Voice Demo for WebXR
meta: October 2026 | UNL SoC Yao project
summary: A browser demo for testing and comparing wake-word engines and speech-to-text models in WebXR on Apple Vision Pro and Meta Quest.
tags: JavaScript, Python, Flask, WebXR, Machine Learning
link: https://github.com/Taver-Versch/voice_demo
---
> **Note:** I made this demo to test voice options for my [senior design project](senior-design), the VR Protein Analysis Lab. It's part of the UNL School of Computing Yao project.

Before adding a voice assistant to our VR app, I needed a way to compare wake word engines and speech-to-text (STT) models side by side. This demo runs in a laptop browser and in WebXR on the Apple Vision Pro and Meta Quest, so I could test them on the actual headsets. For senior design, we ended up going with openWakeWord and Moonshine.

## What it does
- **Wake word:** TensorFlow.js Speech Commands or openWakeWord listens for when the user is talking to the app. It ships with a custom "Hey Husker" wake word model.
- **Speech to text:** Moonshine or Whisper tiny, through Transformers.js, turns the phrase into text.
- **Three modes:** wake word and STT, wake word only, or STT only.
- **Privacy:** everything runs in the browser, so audio and text are never sent to a server.

## Running it on a headset
WebXR and microphone access both need HTTPS, so I share the Flask app through a Cloudflare tunnel and open the tunnel's URL on the headset.
