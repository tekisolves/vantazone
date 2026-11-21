# VANTA ZONE

A landscape, last-one-standing first-person shooter that runs in a phone browser — built to play smoothly on low-end Android phones. The whole game is one HTML file (three.js r128 from a CDN, no other assets: every shape, colour and sound is generated in code).

![Preview](docs/preview.png)

## Play
Open `index.html` in a browser, or enable **GitHub Pages** (Settings → Pages → deploy from `main`, root) and play from the link on your phone. Hold the phone in landscape. Live: https://tekisolves.github.io/vantazone/ (once GitHub Pages is on).

**Phone:** left thumb moves · right thumb turns/looks (push further = faster) · FIRE · AIM (scope) · SPRINT · RELOAD · II pauses.

**Laptop:** WASD · mouse look · left click fire · right click scope · Shift sprint · R reload · Esc pause.

**Controller (PlayStation/Xbox):** sticks move/look · R2 fire · L2 scope · L3 sprint · Square/X reload · Options pause.

The game detects the device and sets controls, quality and aim help to match.

**Tune your aim:** set MODE to RANGE, play 12 targets, and follow the tip on the results screen.

## Art direction — "sun-baked tactical"
Light, warm, muted world; dark enemies with one hostile red-orange accent. Colour = meaning (mint = you, red-orange = enemy, violet = storm, amber = armour, green = health). Hard surfaces crisp, organic shapes smooth, everything grounded with baked ambient occlusion. Full rules are at the top of `index.html`.

## Performance budget
All scenery is one mesh with light and shadows baked at load · each enemy is 7 meshes · no real-time shadows · 30 FPS cap with auto resolution · fixed 1/60 s game logic · nothing allocated per frame. Turn on `FPS: ON` in the options to measure.

## Changelog
- [1.2](docs/CHANGES_v1.2.md) — firing range with aim measurements and tuning tips, turn boost, tracking assist
- [1.1](docs/CHANGES_v1.1.md) — phone/laptop detection, controller support, golden-hour graphics, 10/16 enemies, laser-sight marksman, line-of-sight culling
- [1.0](docs/CHANGES_v1.0.md) — art direction, feedback/juice, armour plates, stats, live menu
- [0.6](docs/CHANGES_v0.6.md) — human enemies with natural movement, realistic low-poly shapes
- [0.5](docs/CHANGES_v0.5.md) — performance pass for low-end phones
