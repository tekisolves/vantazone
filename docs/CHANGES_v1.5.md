# 1.5.1: aiming and looking fixed

**The bug:** aiming and looking around didn't work properly.
- **Phone:** the AIM, FIRE, RELOAD, SPRINT and SWAP buttons sit exactly where your right thumb rests to look. A touch
  there pressed a button instead of turning the view. And holding AIM used the same thumb you look with, so you could
  scope or look, but not both.
- **Laptop:** if the game lost the mouse (Esc, alt-tab, or the browser refusing to re-capture it for about 1 s after
  Esc), it showed CLICK TO AIM, but clicking did nothing. The click landed on the invisible touch layer that sits on
  top of the game, not on the game itself. So you couldn't look around until you paused and resumed.

**Fixes**
- **Swipe look (new default on phones):** the view follows your finger 1:1, like most phone shooters. A 300 px swipe
  is about 100°. No dead zone and no ramp-up. It's slower while scoped (slower again on the LR-7), and the aim assist's
  gentle pull backs off while you swipe so it never fights you. The 1.4 camera stick is still in ⚙ as
  **LOOK STYLE: STICK**.
- **Drag from FIRE or AIM to look:** a thumb that starts on FIRE keeps shooting while you drag it to track a target.
  The same works from AIM.
- **AIM taps on and off:** tap to scope, tap again to stop, so your thumb is free to look. Holding still scopes only
  while held. Sprinting or switching guns drops the scope.
- **Laptop:** one click anywhere on the game takes the mouse back.
- **Laptop, browsers with no mouse capture at all:** hold a mouse button and drag to look.
- **The view responds a frame sooner.** Your view angle is no longer blended between logic steps, so mouse and swipe
  movement show on the very next frame. Position is still blended, so movement stays smooth.

**Other edge cases fixed**
- A new match starts with input cleared. A FIRE button held when the last match ended, a scope left on, or a stuck
  thumb no longer carry over.
- Turning the phone upright mid-match pauses the game (the ROTATE screen used to cover a match that kept running).
- Tutorial text matches your look style and the new AIM tap.

**Tested** (real WebGL, emulated phone with real touch events, and laptop):
- a 300 px swipe turns 1.74 rad and back, and turns half as far while scoped
- tapping AIM toggles the scope on and off
- dragging from FIRE turned the view while firing 9 shots
- the stick style still turns
- move + look + scope with three fingers at once
- a new match clears the scope
- portrait pauses
- laptop: the click recaptures the mouse, mouse look and right-click scope work
- the full 1.5 regression passed, with phone FPS unchanged (27.8 average)
- 0 script errors

# VANTA ZONE 1.5 "GRIT": a city you can get lost in

1.4 gave you reasons to come back. 1.5 gives you somewhere worth coming back to: a map four times bigger, with
streets, buildings and districts that each feel different, and a look that is stylised but gritty instead of clean and
toy-like. It still runs on a low-end phone (measured below).

## Art direction: "stylised grit"
Not photo-real. Games like Fortnite and Valorant simplify shapes and colours on purpose so you read the game in a
glance, and that is also what lets them run on weak hardware. 1.5 keeps that clarity and puts the **grit in the
surfaces** instead of in extra polygons:
- **One grime texture for the whole world** (256x256, generated in code at load, no download). It tiles seamlessly and
  is laid over everything by world position, so nothing needs UV maps:
  - walls get rain streaks, rust drips and blotches
  - floors get worn patches, oil stains and hairline cracks
  - close up, a fine grain
- Each surface has a **grit amount**: painted lines and lamps stay clean, containers and old plaster are filthy.
- **Half-Lambert light** (Valve's Team Fortress 2 trick, also used by Valorant). Light wraps further round each
  shape, so shadow sides stay soft and readable instead of going black.
- **Colour grade**: a gentle split-tone that cools shadows and warms lights.
- **Dust haze**: warmer and dustier, thicker on LOW quality (see Performance).
- Palette pushed toward sun-faded, dusty tones. The colour-means-something rules are unchanged: mint = you,
  red-orange = enemy, violet = storm, amber = armour, green = health, sky blue = weapon crate.

The full rules are at the top of `index.html`.

## A 40x40 city (4x the area), new every match
Five districts, each with its own ground, cover and **one tall landmark you can navigate by**:

| District | Ground | Cover | Landmark |
|---|---|---|---|
| Container Yard (NW) | concrete slabs, parking bays | rows of containers, some two deep | gantry crane over the yard |
| Old Town (NE) | paving stones | 2–3 storey buildings on a street grid, courtyards | water tower on the tallest roof |
| The Ruins (SW) | broken slabs and bare earth | broken walls, half-collapsed buildings, rubble | leaning radio mast |
| Rail Depot (SE) | dark concrete | long platform barriers, freight containers | rusty fuel tank with a ladder |
| Central Plaza | paving | corner pillars, low walls | stepped obelisk with four lamps |

- **Cross roads** (asphalt, dashed centre lines, yellow edges) link the districts. They get scattered barriers and
  crate stacks so they're never empty shooting galleries.
- **Buildings**: plaster blocks in six faded colours. Storeys read from a distance through window rows, sills, floor
  lines and a parapet. Some windows are boarded up, ruined buildings have broken tops, and some roofs have AC units.
  Windows are flat panels (2 triangles each), so a street full of them stays cheap.
- **A new city every match.** Each district's generator places its own kind of cover with random sizes and gaps.
  A flood fill then opens walls until every floor tile can be reached, so it always succeeds and needs no fallback
  map. It takes about 1 ms. 30/30 test cities were fully connected with all four spawn pads clear.
- The **firing range and the menu always use the same city** (fixed seed), so range scores stay comparable.
- You spawn at one of the **four road ends**, facing the middle. The storm starts around the whole city and closes
  toward a random spot near the plaza.
- **District name** fades in under the compass when you walk into a new one.
- More to fight over:

  | | 1.4 | 1.5 |
  |---|---|---|
  | Enemies (Training / Standard) | 10 / 16 | 14 / 22 |
  | Storm (Training / Standard) | 240 / 150 s | 300 / 240 s |
  | Pickups | 7 | 15 |
  | Weapon crates of each gun you didn't bring | 1 | 2 |

- Outside the walls: a low **skyline** of abandoned industrial blocks, chimneys and a water tower, half lost in the
  haze. It says this is part of a bigger city.

## Perks: the second half of your loadout
One extra button on the menu, **PERK**, next to GUN. Tap to cycle; the line under it explains the perk. One pick, one
clear effect, all available from the start:

| Perk | Effect |
|---|---|
| **PLATED** | Start with all 3 armour plates (everyone else now starts with 2) |
| **LIGHTFOOT** | Move 10% faster; enemies only hear you sprint from 2.5 tiles (normally 4.5) |
| **SCAVENGER** | 50% more ammo at the start and from pickups; eliminations drop loot more often |
| **STEADY HANDS** | 40% less recoil and spread (a little tighter shotgun spread too) |

Saved with your progress, like your starting gun.

## Performance
A 4x bigger map would normally cost about 4x the drawing. Five changes keep it in budget:
1. **Chunks.** Scenery is split into a 3x3 grid inside the city plus a grid outside it. The GPU skips every chunk
   that's behind you or off to the side.
2. **View distance per quality.** On LOW, the haze is thicker, and chunks, enemies and loot beams past it aren't drawn
   at all. MED sees further. HIGH (laptops) keeps the full view to the skyline and mountains.
3. **Cheaper shapes.** The outer walls are four long pieces instead of 152 segments (about 40x fewer
   triangles), rubble uses 8-triangle chunks, stains are flat discs, crates have one strap each, and container
   sides have 3 ribs instead of 5. Together that cut the city from about 61k to about 46k triangles.
4. **All shadows in one mesh**, so they're one draw call instead of one per chunk.
5. **LOW reads the grime texture once per pixel**, not twice.

Measured with the same method as 1.4: emulated phone (780x360 at 2x, touch), CPU slowed 6x, software GPU, 20 s
scripted walk-and-shoot in a Standard match, several runs each:

| | 1.4 | 1.5 |
|---|---|---|
| FPS (cap 30) | 27.8 – 29.0 | 26.9 – 28.1 |
| Average triangles drawn | ~38–39k | ~41–43k |
| Average draw calls | 25–31 | 39–56 |
| CPU time per frame (game logic / render) | 4.6 / 4.3 ms | 3.9 / 4.5 ms |

Both versions dipped to about 23 FPS at times and dropped render scale to keep up. The software GPU is harsher than a
real phone's.

## Tested
Real WebGL in headless Chrome, on an emulated phone (touch, LOW) and a laptop (HIGH):
- menu with the PERK button
- the first-run tutorial, then skipping it
- a Training match, then a Standard match with a new city
- the PLATED and LIGHTFOOT effects
- shooting and hitting an enemy
- a win screen with XP
- the firing range (same city twice, targets keep coming)
- screenshots in every district at LOW and HIGH
- 30 generated cities

**0 script errors.** Not yet tested on a real phone, a real controller or Safari.
