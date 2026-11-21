# VANTA ZONE 1.1

## Plays right on phone AND laptop
The game checks for a finger (a coarse pointer) versus a mouse, and sets itself up to match:

| | Phone | Laptop |
|---|---|---|
| Controls | touch sticks + buttons | mouse look (cursor captured; Esc pauses), WASD, left click fire, right click scope, Shift sprint, R reload |
| Quality | LOW, 30 FPS cap, no anti-aliasing | HIGH, 60 FPS cap, anti-aliasing on |
| Aim help | full aim assist + auto-fire | lighter assist, auto-fire off (a mouse is precise) |
| Other | "rotate phone" screen, fullscreen | no rotate screen, no gyro option |

**PlayStation / Xbox controller** works on both: left stick moves, right stick looks (same feel as the touch stick), R2 fires, L2 aims, L3 sprints, Square/X reloads, Options pauses.

## Graphics
- **Golden hour.** The sun is lower (35°) and warmer, so shadows are longer and more dramatic. The sky is deeper blue with a warm glow, and you can see a sun disc and halo.
- **Rim light** on enemies, guns and pickups: a faint cool backlight that outlines their edges against the background.
- **Floor detail.** Dashed lane paint, oil stains and cracks.
- **Skyline.** Floodlight poles on the outer wall, vents and AC units on the containers, and rolling hills between the trees and the mountains.
- **Movement in the scene.** The clouds drift, and dust puffs rise where bullets hit.

## More enemies
- **Training** now has 10 enemies (was 6), **Standard** 16 (was 12).
- **New marksman.** He keeps his distance, holds still to aim, and hits hard from up to 17 tiles away. He's fair because you get two warnings: a **red laser sight** shows for about 1.4 s before each shot, and a **lock-on beep** tells you which direction it's coming from.

## Phone hardware: the extra enemies cost less than before
**Line-of-sight culling.** Enemies hidden behind walls aren't drawn at all. Three rays per enemy check its centre and both edges, so half-hidden enemies don't pop in late. In testing only 3–5 of the 10 enemies were drawn at any one time. Draw calls went from 59 (with 6 enemies) to 46 (with 10).

## Tested
- 0 script errors, checked in both phone mode and laptop mode.
- 60 logic steps per second; 30 FPS on phone, 60 on laptop.
- The laser sight shows when the marksman aims at you.
- All 1.0 features re-checked: armour, kill streaks, low-health warning, shake, storm warnings, end screen.
