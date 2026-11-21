# VANTA ZONE 1.0: art direction + polish

## Art direction: "sun-baked tactical"
These rules are written at the top of the code, so anything added later stays consistent.

1. **Value first.** The world is light, warm and muted (sand concrete, terracotta, dry olive). Enemies are **dark**, with one hostile red-orange accent, so they stand out at a glance. *Why:* in shooters, readability comes from value contrast more than from hue. This is the same idea behind Valorant's muted maps.
2. **Colour = meaning, never reused.** Mint = you and the UI; red-orange = enemy; violet = storm (it was red, which clashed with "enemy"); amber = armour; green = health.
3. **Hard vs soft.** Man-made things (concrete, crates, metal, rocks) keep crisp bevels and flat facets. Bodies, foliage and clouds are now **smooth-shaded**. That's the "smoother" look, and the contrast between the two makes both read better.
4. **Warm sun, cool shadows, everything grounded.** There's baked ambient occlusion: objects darken where they meet the floor, and the floor darkens softly near walls. The horizon has warm haze, and the sky glows toward the sun. It's all computed once at load, so it costs nothing per frame.
5. **Detail where you look.** Cover, enemies and your gun carry the detail; the background stays simple.

## Feedback ("juice")
- **Screen shake.** Small on every shot, big when you're hit. It uses "trauma squared", so small bumps barely move and big hits really do. There's an option to turn it off (an accessibility best practice).
- **Hits.** Each hit plays a sound, throws sparks, shows the marker, jolts the enemy's body and knocks him back slightly.
- **Kills.** The marker turns red to confirm a kill. Kills within 4 s of each other show a banner (DOUBLE KILL / TRIPLE KILL / RAMPAGE) with its own sound.
- **Low health.** Below 35 HP the screen edges pulse red and you hear a heartbeat.
- **Low ammo.** At 5 rounds or fewer the ammo counter turns red.
- **Look.** A subtle cinematic vignette darkens the screen edges.

## Gameplay gaps filled
- **Armour plates.** Armour could never be refilled before. Plates now spawn and drop, giving +50 each (one HUD bar).
- **Smarter drops.** Eliminations drop whatever you're short of: health, ammo or armour.
- **Loot beacons.** A soft coloured light beam over every pickup lets you spot it across the arena.
- **Storm warnings** at 25%, 50% and 75% closed.
- **Match flow.** The match fades in with a "DROP IN" banner. The end screen shows your placement (#N of 7), kills, headshots, accuracy and time.
- **Pause button** on screen, as well as auto-pause when you leave the app.
- **New options.** LOOK speed (LOW / MED / HIGH) and SHAKE (ON / OFF). Both are saved on the phone.
- **Live menu.** The menu shows the arena with the camera slowly circling it, drawn at about 15 FPS to save battery. The HUD is hidden on menus.

## Testing (headless, software preview)
| Check | Result |
|---|---|
| Script errors | 0 |
| Logic steps / frames per second | 60 / 30 |
| Draw calls in Training | 59 (was 53; +1 per pickup beacon) |
| Armour pickup | 40 → 90 ✓ |
| Kill streak | "DOUBLE KILL" ✓ |
| Low-health edge and heartbeat | ✓ |
| Shake on damage | 0.45 trauma ✓ |
| Storm warning at 30% | "STORM CLOSING" ✓ |
| End screen | "#4 of 7 · Kills · Headshots · Accuracy · time" ✓ |

**Bug the tests caught:** an inline comment cut off the line that hides the menu, so pressing DEPLOY started the match behind the menu. Fixed.

**Not tested here:** real GPU speed, and how it feels in your hands. Check the FPS counter on the phone.
