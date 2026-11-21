# VANTA ZONE 1.2: aim feel + firing range

## Firing range (MODE: RANGE)
A practice mode for tuning how aiming feels on your own phone or laptop.
- **12 targets, one at a time.** Each steps out somewhere in front of or beside you (sometimes off-screen, so you have to turn) and strafes. A beep from its direction tells you where. Nobody shoots back.
- **It measures what decides aim feel:**
  - **Time to first hit**: how fast you get onto a target.
  - **Time to kill.**
  - **Accuracy.**
  - **Overshoot**: how often your aim swings past the target and has to come back. It's the clearest sign the look speed is too high.
- **It tells you what to change.** For example, lots of overshoot → "try LOOK: LOW"; slow first hit → "try LOOK: HIGH"; low accuracy → shorter bursts or AUTO-FIRE.
- **Scoring.** You get a score, and the best is saved separately for phone and laptop. The FPS counter is always on in the range, with frame time in ms.

## Aiming (phone and controller)
- **Turn boost.** Hold the look stick at the very edge and turning speeds up after a moment. 180° turns are quick, while small movements near the centre stay precise.
- **Tracking assist.** When your target moves across your view, the camera follows part of that motion, the way console shooters handle thumbs and sticks. It's off for the mouse, which is precise enough without it.
- **The range uses Training-level aim help,** so tuning there matches normal play.

## Phone hardware
- The render-scale floor on LOW is now 0.45 (was 0.5), giving the auto-resolution more room on a struggling phone.
- The FPS readout shows frame time too (for example "30 FPS · 33 ms · 0.6x").

## Tested
- **Range, scripted clean shooter:** 12/12, first hit 0.30 s, accuracy 82%, overshoot 0.0 → "well tuned".
- **Range, scripted sloppy shooter:** overshoot 0.9 per target → "try LOOK: LOW".
- **Bug caught and fixed:** the overshoot counter cleared itself on the same step it detected a crossing, so it always read 0.
- **Regression on phone and laptop setups:** 0 errors; all earlier features still work.
