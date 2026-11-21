# VANTA ZONE 1.3: smarter enemies

Enemies no longer magically know where you are. Each one has a small "brain" with five states.

| State | What he does |
|---|---|
| **Patrol** | Walks (doesn't run) between random spots inside the storm. Everyone starts here. |
| **Hunt** | Heads for your **last known position**. If you're not there, he goes back to patrolling. |
| **Fight** | Can see you: strafes, holds or backs off depending on his kit, and shoots when it's his turn. |
| **Cover** | When he's hit or bullets land close: sprints to the nearest spot you can't see, waits 1–3 s, then peeks out and fights again for ~2 s before ducking back. |
| **Flank** | (Standard only) While a squadmate keeps you busy, one hunter is sent round to your side, about 100° away from the attacker. |

## How they find you
- **Sight.** Anything one enemy sees, the whole squad knows ("squad comms").
- **Hearing.**
  - Your **gunfire** gives away your position to anyone within 10 tiles.
  - **Sprinting** is heard within 4.5 tiles.
  - **Walking is quiet.**
- **Memory.** What the squad knows goes stale after 10 s without contact, and then they go back to patrolling.

## Fairness rules
- **No spawning in view.** Enemies always start somewhere you can't see.
- **Slower if he's behind you.** An enemy that spots you from behind takes 1.8× longer to react, so you have time to hear him.
- **"SPOTTED" warning.** When an enemy first sees you, a radio callout plays from his direction and "SPOTTED" flashes on the HUD.
- **The shot warnings are still there:** red visor, marksman laser and lock-on beep.

## Rushers stay rushers
They never take cover. They charge.

## Tested (scripted scenarios)
| Check | Result |
|---|---|
| Spawns inside your view | 0 of 16 |
| Quiet start, 2 s | all 16 on patrol |
| One gunshot | nearby enemies switch to fight/hunt |
| A burst near an enemy | he goes to cover out of your sight, then cover → peek → fight (~2.5 s) → cover → peek |
| Flanking | flanker assigned, sent round at 1.74 rad (≈100°) from the attacker |
| Reaction delay | 1.41 s behind you vs 0.77 s in front |
| Regression on phone, laptop and range | 0 errors; draw calls unchanged (the brain is pure logic, no graphics cost) |
