# Sprites

Every picture the character, the cat and the nav ledge use is a PNG in this folder. To change one, open
it in a pixel editor (Aseprite, Piskel and LibreSprite all work), draw, and save over the same file name.
Rebuild the site and it shows up. No code changes.

Sprites are drawn small and shown 3x bigger (4x on big screens, 2x on phones), so 1 pixel in the file is a 3x3 block on screen.
Keep the background transparent.

## taver/ (20 x 29 px each, feet on the bottom row)

| File | When it shows |
|---|---|
| `stand.png` | standing still, facing the visitor |
| `breathe.png` | swaps with `stand` every half second while idle |
| `blink.png` | a quick blink every few seconds |
| `sit.png` | after about 8 seconds of standing still |
| `walk1.png`, `walk2.png` | walking. Side view **facing right**. The code flips them for walking left |
| `run1.png`, `run2.png` | running, same rule: draw facing right |

## cat/ (18 x 13 px each, facing right)

| File | When it shows |
|---|---|
| `walk1.png`, `walk2.png` | following you |
| `sit.png` | waiting next to you |
| `sit2.png` | tail flick while sitting |

## world/ (18 px tall)

| File | What it is |
|---|---|
| `ground.png` | the middle of the ledge, 240 px wide. It repeats sideways, so the left and right edges should match up |
| `ground-left.png`, `ground-right.png` | the two rounded ends, 10 px wide |
| `sidewalk.png`, `sidewalk-left.png`, `sidewalk-right.png` | night mode versions of the three ground files, same sizes |
| `sun.png`, `moon.png` | the day/night switch in the sky, 14 x 14 px each. The sun shows by day, the moon at night |
| `streetlight.png` | night mode, 16 x 30 px. Stands over every other tab. Keep the bulb around 12 px from the left so the light lines up |

The tab names are real text drawn over the dirt part of `ground.png` (rows 6 to 17), so keep that area
fairly dark and plain.

## Changing sizes or adding frames

- A different sprite size works as long as every frame of the same animation is the same size, with the feet on the bottom row.
- Frame names and the walking speeds are at the top of `assets/walker.js` (`FRAMES`, `WALK`, `RUN`, `CAT_GAP`).
- The on-screen scale is `--px` at the top of `assets/style.css`.
