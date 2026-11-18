---
title: VR Protein Analysis Lab (Senior Design)
meta: August 2026 - Present | Product Manager
summary: A protein analysis lab that works in VR with WebXR, built for an outside sponsor, with an LLM voice assistant for accessibility.
tags: WebXR, Docker, AWS, Agile Scrum, LangChain, STT, VR
---
> **Note:** This is an ongoing project that I am working on for a class (Senior Design). This project will be worked on for the duration of the Fall 2026 and Spring 2027 semesters.

The product is **Protein Language Space in VR**, a web app built with A-Frame and WebXR that shows a 3D visualization of protein language model data. Users can explore it in a VR headset or on a laptop, and they can join the same session with a room code as a **host**, a **collaborator**, or a **livestream follower**.

## The course
This course is built to give us experience as real software engineers. This project includes sponsors requesting a product, weekly sponsor meetings, release meetings, and live demos. We are constantly receiving feedback and adjusting accordingly, and we deliver in Agile Scrum sprints for tasks and releases.

## My role: Product Manager
For this project, I am a Product Manager on my team. I work to keep the project in scope, reach out to the sponsor, and assign tasks to groupmates. This means writing user stories in ZenHub and splitting the work between our frontend and backend groups so both sides can work at the same time. This role has really given me valuable experience in leadership and planning.

## How the voice assistant works
As for the project itself, we are adding an LLM voice assistant for accessibility, so users can move around the room by speaking instead of using controls.

1. First, the user says "Hey Husker," and the wake word and speech-to-text (STT) models pick up the command right in their browser.
2. Then, the browser sends that command, along with the user's position, direction, and the room bounds, to our backend.
3. We are working with two AWS servers, one hosting the frontend and a second running a Django backend that uses LangChain to turn the command into movement.
4. Finally, the frontend moves the user and shows a short caption of what the assistant did.

## What I built
On top of the PM role, I also work on the code.

- I brought the wake word and STT pipeline into the app (openWakeWord with a custom "Hey Husker" model, and Moonshine for STT), and I wired the voice commands through to the backend so the user actually moves.
- I have also fixed bugs from VR buttons lagging on the Apple Vision Pro to the menu layout breaking for collaborators.
- Refined prompting for the LLM to keep movement within bounds of the room. 
- Various other small fixes/bugs. Primarily on the first server (Frontend Server).

---

**Next up:** Going forward, I plan to add avatars for every user (with hands for VR users). In the process of making experimental/optional features, I am constantly contacting the Sponsor to ensure they are satisfied with the direction I am going. 
