# VANTA ZONE v5: performance pass

**Goal:** smoother play on a low-end Motorola without changing how the game looks or plays. Gameplay numbers are unchanged: speeds, damage, AI and aim assist are the same as v4.

## Changes

| # | Change | Why |
|---|---|---|
| 1 | **30 FPS cap** (60 on HIGH) | A steady 30 feels smoother than a rate that jumps between 25 and 45. It also cuts GPU work and heat roughly in half on a 60 Hz screen. |
| 2 | **Fixed-step logic (1/60 s) plus interpolation** | The game always simulates in identical ticks. The camera and robots are drawn blended between the last two ticks, so movement stays even when a frame runs late. |
| 3 | **Fake shadows; the shadow map is gone** | v4 drew its shadow map once, but every floor and wall pixel still sampled it every frame. That was the most expensive part of each frame. v5 merges each wall's shadow shape into one flat dark mesh. A stencil test darkens each pixel only once, so overlapping shadows don't stack. Robots keep their blob shadows. |
| 4 | **Starts on LOW; resolution adjusts both ways** | v4 started high and could only step down. Each quality level now starts at the low end of its range. Every 2 s it drops 0.1 if FPS falls below 85% of the cap, and rises 0.1 after 4 s at the cap. A drop also sets a ceiling, so it can't bounce between two levels. Old v4 quality saves are ignored once, so everyone starts on LOW. |
| 5 | **Baked light on static scenery; anti-aliasing off** | Walls, floor and mountains never move, so their lighting never changes. The same sum the GPU did (sky fill + sun × facing) is now computed once at load and stored as colours. They should look the same. Only moving things (robots, rifle, pickups) still use real lights. Anti-aliasing costs a lot on weak GPUs, and flat colours hide jagged edges. |
| 6 | **Mountains merged** | 28 meshes become 1, so 28 draw calls become 1. |
| 7 | **Shared materials** | All robots share one body material. The hit flash and red visor now swap to a second shared material instead of each robot recolouring its own copy. Pickups reuse one geometry and material set. |
| 8 | **Pre-recorded gunshots** | Each shot used to build about 9 audio nodes, 10 times a second. Now 3 variations of the player and enemy shots are recorded once at start and replayed as one buffer each. The live version is used as a fallback for the first few milliseconds. |
| 9 | **HUD only writes changed values** | Each DOM write can make the phone re-layout the page. The radar now redraws 10×/s instead of about 20×/s. |
| 10 | **FPS counter** (`FPS: ON` in options) | Shows the frame rate and current render scale, so we measure instead of guessing. |
| 11 | **Pause on app switch** | Leaving the app pauses the match, suspends audio and releases any held thumbs, so you don't come back running or firing. Menus and the pause screen also stop drawing the 3D view, which saves battery. |

**Skipped on purpose:** pulling the fog closer. Fog doesn't reduce drawing work, and hiding the mountains wasn't worth it once they cost 1 draw call.

## Test results (headless Chrome)

Three.js couldn't be downloaded in the test sandbox, so it was tested with a stand-in for Three.js. That covers all the game's own code, but **not the actual 3D picture or real GPU speed**.

| Measured over 4 s of walking and firing | v4 | v5 |
|---|---|---|
| Logic steps per second | 60 | 60 |
| Frames drawn per second | 60 | 30 |
| Draw calls per frame | 82 | 56 |
| HUD DOM changes per second | 105 | 9 |
| Player position after the same input | (10, 13.24) | (10, 13.24) — same feel |
| Script errors | 0 | 0 |

- Gunshots: 3 player and 3 enemy variants recorded.
- Pause: the clock freezes, held inputs are cleared and audio is suspended; resume works.
- Auto resolution: 0.6 → 0.7 → 0.8 (LOW max). It drops to 0.7 under load, then stays at 0.7 and doesn't bounce.
- Fake shadows: a top-down render shows them falling away from the sun with clean outlines.

## Still to check on the phone

- Does it look the same as v4 (baked light, fake shadows)?
- What does the FPS counter show in a busy fight?
