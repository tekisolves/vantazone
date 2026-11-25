# VANTA ZONE 1.4: a reason to play again

1.3 had a good game loop but nothing to come back for: one gun, one map, no progress saved. 1.4 fixes that,
improves the graphics, and fixes laptop controls, while still running on a low-end Android phone.

## A new arena every match
- Each match generates a **new layout** of barriers, containers and crate stacks.
- Rules keep it fair: pieces never touch each other or the outer wall (every tile can be reached), the four spawn pads stay open, and most floor tiles have cover within 2 tiles, so there are no long empty shooting galleries.
- Usually takes 1–3 tries (a few ms). If it ever fails, it falls back to the classic map.
- You spawn on a random side, facing the middle.
- The **firing range keeps the classic map**, so your aim scores stay comparable.

## A moving storm
- The storm still starts around the whole arena, but now it **shrinks and drifts toward a random final spot**.
- The centre moves less than the radius shrinks, so each new circle sits inside the last one.
- The minimap shows the ring. Leaving it puts a violet glow on the screen edges and a warning in the feed.

## Three guns
| Gun | Feel |
|---|---|
| **VX-9 Assault** | The all-rounder from 1.3: full auto, 30 rounds. |
| **KR-12 Breacher** | Pump shotgun: 8 pellets, brutal up close, weak past ~6 tiles. 6 shells. |
| **LR-7 Marksman** | Slow, accurate, hard-hitting, with a strong scope (28° view). A headshot drops anything except a heavy. 8 rounds. |

- **Weapon crates** have sky-blue beams and show on the radar. Each match has one crate for each gun you didn't bring.
- Walking over a crate fills an empty slot or adds ammo for a gun you already carry.
- With both slots full, **F / SWAP / Triangle** takes the crate's gun and drops yours (with its ammo).
- Switching: **1 / 2 / mouse wheel** on laptop, the **SWAP** button on phone, **Triangle/Y or R1** on a controller.
- Each gun has its own sound, recoil, muzzle flash, reload time and scope zoom.

## Progress that's saved (on the device)
- **XP**: +100 per elimination, +50 per headshot, +500 for a win, points for placement and survival time. Standard mode gives +50%.
- **10 ranks**, Recruit to Vanta. Rank 2 unlocks the KR-12 as a starting gun, rank 4 the LR-7, and ranks 5, 7 and 10 unlock gun finishes (amber, coral, gold).
- **Daily challenge**: one of 10, the same for everyone on a given day (e.g. "Get 3 eliminations with the KR-12"). Worth +300 XP.
- **Records**: matches, wins, total eliminations, best eliminations in one match, best placement, fastest win. The end screen says when you beat one.
- **End screen**: XP breakdown, animated rank bar, any rank-up or unlock, daily status, and a **MENU** button next to REDEPLOY.

## Simpler menu + tutorial
- The first screen is now just: rank card, **DEPLOY**, MODE, GUN, ⚙ settings, and the daily challenge.
- Everything else (auto-fire, gyro, quality, look speed, invert Y, shake, FPS, gun finish, replay tutorial) is under ⚙, along with the controls for your device.
- **First-run tutorial** (6 short steps: move, look, shoot, scope, weapon crates, storm). Enemies hold still and the storm waits until you've done each step. It can be skipped, and replayed from Settings.
- The pause screen has **QUIT TO MENU**.

## Seeing what the enemy brain is doing
The 1.3 AI was smart, but you never saw it. Now:
- Red tags appear above enemies you can see: **COVER!** when one breaks for cover, **CONTACT!** when one spots you, **RUSHING** when a rusher charges, **FLANKING** when one is sent round.
- **⚠ FLANKER — LEFT / RIGHT / BEHIND YOU** appears when a flanker is sent round and is close enough to hear (with a radio blip from that side).
- The feed tells you when **an enemy heard you sprinting** and when **the enemy lost track of you** (their memory runs out after 10 s).
- Rushers now stop at arm's length instead of walking into your camera.

## Graphics (all within the low-end budget)
- **Bullet holes** on walls and floor: 40, oldest reused first, one draw call. They sit on each block's real surface, including the sloped tops of barriers.
- **Shell casings** fly out of the gun and bounce once: brass for rifles, red hulls for the shotgun. One draw call.
- **Hit sparks are red-orange on enemies** and yellow on the world, so hits read instantly.
- The **muzzle flash** is a star of light that also lights your gun for a frame.
- **Storm wall**: scrolling violet energy streaks, bright at the ground and fading upward (it was a flat tint).
- **Ground**: soft colour variation across the field, worn into dry dirt around the walls. Sandbags and barrels outside the walls break up the edge.
- **Arena detail**: cargo doors with locking rods on container ends, hazard chevrons on free-standing pillars, painted parking bays.
- **Body landing**: a puff of dust where an eliminated enemy hits the ground.
- **New gun models**: KR-12 (pump, shell tube, red-dot sight, spare shells) and LR-7 (long barrel, big scope).

## Laptop controls
- Keys are read by **physical position**, so W A S D works on AZERTY and other layouts, and Shift doesn't break other keys while you sprint.
- **The mouse is released whenever the game pauses** (alt-tab, switching tabs), so the pause and end buttons can always be clicked. In 1.3 the mouse could stay captured and the buttons couldn't be clicked.
- If the mouse capture is lost mid-match, **"CLICK TO AIM"** shows and one click takes it back.
- **Raw mouse input** where the browser supports it (no OS acceleration), and big bogus mouse jumps are ignored.
- Scoped look is slower (slower again on the LR-7 scope).
- **5 look speeds** (was 3), plus **INVERT Y** (mouse and controller).
- **Enter** deploys / redeploys / resumes. **P** pauses too. Alt-tab pauses instead of leaving keys stuck down.
- The controller works in the menus (Cross/A starts), not only in matches.

## Phone
- **SWAP** button (shows **TAKE** when you're standing on a crate you can take).
- **Add to Home screen** now installs it as an app: full screen, locked to landscape, with its own icon (`manifest.json`).
- **Works offline after the first visit** (`sw.js`). It's network-first, so you always get the newest version when online.
- **three.js is bundled** (`vendor/three.min.js`) instead of loaded from someone else's server. The game no longer breaks if that server is slow or blocked; the CDN is only a fallback.
- Starting a match fades to black first, then builds the new arena behind the fade, instead of freezing on the menu.

## Performance (measured, same scripted walk-and-shoot in a Standard match)
Emulated low-end phone: 780×360 at 2×, CPU slowed 6×, software GPU (harsher than a real phone's GPU). Two runs each:

| | 1.3 | 1.4 |
|---|---|---|
| FPS (cap 30) | 29.3 / 24.1 | 27.5 / 26.1 |
| Average triangles drawn | ~39k | ~41k |
| Average draw calls | 26–38 | 26–58 (depends on how many enemies are in view) |

1.4 is within run-to-run noise of 1.3. The first 1.4 build was ~18k triangles heavier. Straps, container ribs, paint and door
hardware were switched to plain boxes and the ground grid was made coarser, which brought it back in line. The auto-resolution
system still adjusts render scale to hold 30 FPS.

## Tested
Scripted runs on an emulated phone (touch) and a laptop (mouse/keyboard): menu, the full tutorial, all three guns
(fire / reload / swap / take from a crate), an elimination, win screen with XP and rank-up, a second match (new layout,
storm moved, no tutorial), pause → quit to menu, settings, firing range (classic map). **0 script errors on both.**
Layout generator: 30/30 layouts valid in a row. Not tested on a real phone, a real controller or Safari.
