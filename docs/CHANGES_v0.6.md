# VANTA ZONE v6: realistic shapes, human enemies, natural movement

**Brief:** no blocky robots. Enemies should move fluidly and naturally, the game should look fun and less like Minecraft, it must still run on a low-end Motorola, and the code should stay easy to follow. Everything from v5 (frame cap, fixed-step logic, auto resolution, pause, baked sounds) is kept.

## What changed

### Enemies: human operators instead of robots
- **Three kits you can tell apart at a glance.** *Rifleman* (slate uniform, orange armband), *rusher* (tan uniform, red armband, shotgun, fast) and *heavy* (olive, bulkier armour, shoulder plates, machine gun, slow). Each has a helmet, mask, glowing visor, vest, pouches, boots and a gun held at the shoulder.
- **Natural movement**, in `animate()`:
  - **No foot sliding.** The legs cycle by the distance actually covered, and the swing angle is worked out from the stride length. Most games skip this, which is why walkers often look like they're skating.
  - **Strafing and backpedalling look right.** The legs swing in the direction he's moving, even while his body faces you.
  - **Human turning speed.** Enemies turn at a limited rate instead of snapping round instantly (the rusher turns faster).
  - **Body follow-through.** The hips dip as the legs spread, the shoulders counter-twist, and the torso leans into speed and into turns. When standing still, the chest breathes.
  - **Springy reactions.** Recoil when he fires and a jolt when you hit him (a bigger one for headshots) use a small spring, so they overshoot and settle like a real body.
  - **Death.** The knees give way with the feet staying planted, he slumps, then topples backwards with his legs straightening as he lands. The body is cleared after about 4 s.
- **Shot warning.** The visor still turns red just before he fires, and there's now a muzzle flash at his gun with the tracer starting from it.

### World: real shapes instead of cubes
- **Concrete barriers** with a sloped top, small gaps between segments and a painted hazard band. Square **pillars** with caps sit at corners.
- **Shipping containers** with corrugated ribs and top rails, one colour per container.
- **Crate stacks**: two uneven layers of wooden and army-green crates with straps.
- **Floor** of individual concrete slabs, each a slightly different shade, with visible seams.
- **Outside the walls:** pine and leafy trees, rocks, grass patches and tufts. There are also low-poly **clouds**, and the mountains are kept.
- **Bevelled edges everywhere.** The thin cut edges catch the sun, which is most of what stops a shape looking like a Minecraft block.

### Your side
- **New rifle**: receiver, rail, handguard, barrel with muzzle brake, angled magazine, grip, stock, scope and gloved hands.
- **AIM now brings the scope up to your eye** and hides the crosshair.
- **Sprinting** tilts the gun down and across; **reloading** tips it.
- **Impact sparks** show where your bullets land on walls, the floor and enemies. All the sparks together cost one draw call.
- **Pickups** are a real ammo can and a med kit.

## Things you didn't know to ask for (but matter)

| Thing | Why it matters | What v6 does |
|---|---|---|
| **Shapes must fill their grid cell** | Movement, bullets and line of sight all use the 20×20 grid. A thinner shape would mean invisible walls and bullets stopping in mid-air. | Every barrier, container and crate stack covers its full cell and is taller than eye level. |
| **Hitboxes must match the bodies** | Old robot hit spheres wouldn't line up with human shapes. Shots would hit air or miss bodies. | New spheres for head, chest and legs. Bullet magnetism (for the body only) is kept, so it isn't harder. |
| **Draw calls, not triangles, limit weak phones** | Each separate object costs the CPU one "draw call". Triangle count matters much less. | All scenery (~20k triangles) is ONE mesh with light and shadows baked in. Each enemy is 7 meshes. Training totals about 53 draw calls, about the same as v5. |
| **Readable silhouettes** | In shooters, enemies have to stand out from the background or the game feels unfair. | Dark uniforms against light concrete, plus one bright armband and a glowing visor each. |
| **Shader-compile stutter** | WebGL builds each material's shader the first time it's drawn, and on phones that freezes the first fight for a moment. | `R.compile()` builds them all when you press DEPLOY. |
| **Footsteps** | In real shooters you track enemies by sound. | Enemy footsteps (within 9 tiles) are panned left and right, so you can hear where they're coming from, even through walls. You also hear your own steps. All are pre-recorded once, like the gunshots. |
| **No garbage per frame** | Creating objects every frame makes the phone pause to clean up memory, which shows up as random hitches. | Tracers and sparks use fixed pools, and shapes are cached and shared. |
| **Same layout every load** | Random scenery would change every time and could look worse on some loads. | Scenery uses a seeded random generator. Enemy spawns stay random. |
| **One scale** | Your eye is 0.6 units up, so 1 tile ≈ 2.7 m. | Enemies are built to that human scale (~1.8 m tall), and crates and containers match. |

## Gameplay changes (small, on purpose)
- The rusher's close-range attack is now a shotgun blast instead of a robot claw. The damage and range are the same.
- Damage, speeds, AI, aim assist and auto-fire are all unchanged.
- Lighting is slightly softer (more sky fill, a bit less sun), so walls in shade aren't gloomy. Floor and wall colours are a bit darker so sunlit surfaces don't burn out to white.

## Testing
Three.js can't be downloaded in the test sandbox, so I wrote a test-only stand-in for it. It builds the same geometry and draws it with a simple software renderer, which is how the preview images were made. It shows shapes, colours, poses and animation accurately, but **not** real GPU speed or exact WebGL pixels.

| Check | Result |
|---|---|
| Script errors (play test + all preview renders) | 0 |
| Logic steps / frames drawn per second | 60 / 30 (same as v5) |
| Draw calls in Training | 53 |
| Scenery triangles (one mesh) | ~20,000 |
| Triangles per enemy | ~830–920 |
| Gunshot + footstep sounds pre-recorded | 3 + 3 |
| Death animation | falls flat, then cleared after ~4.5 s |

Problems the previews caught and that are now fixed: the floor was blowing out to plain white, the clouds looked like grey rocks, the shadows under enemies were square, the death pose sank through the floor, and your forearms looked like poles.

## Still to check on your phone
1. The FPS counter in a busy fight (Standard mode has 12 enemies, about 100 draw calls).
2. Whether the enemies' walking and turning feel natural in motion. Stills can't show that fully.
