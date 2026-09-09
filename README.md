# Evia

A small, dependency-free animated character: a glowing yellow orb on a white background, with big solid white eyes and a range of human-like expressions — blinking, winking, smiling, laughing, being surprised, going sleepy, looking around, rolling her eyes, and raising a skeptical eyebrow — played subtly and infrequently, with long calm rests in between, while she gently floats and breathes.

When the page first loads, a yellow puddle-drop ripple bursts from directly behind her before settling, like a raindrop hitting water.

Click the orb and it floats up to the top-left corner, shrinks, settles into a "thinking" pose, and a speech bubble pops in to her right asking "Which of the jobs below are you working on today?" — the text reveals letter by letter and keeps a gentle talking bob while it's shown. Click again and everything returns to full size in the center.

It's also installable as an app (see **Installing it as an app** below).

## Run it

Open `index.html` in a browser — no build step, no dependencies. For the installable-app behavior to work, it needs to be served over HTTPS (or `localhost`) rather than opened as a bare `file://` page — see below.

## How it works

**Opening flash (`.flash-ring`):**
Sits directly behind the orb at the same center point (lower `z-index`). A small bright core (`.flash-core`) flashes and fades fast, while three ring outlines (`.ripple`, staggered with `animation-delay`) expand outward and fade — like ripples from a drop hitting a puddle — using the orb's own yellow (`--orb-b`). Runs once automatically when the page loads.

**Eyes:**
Big solid white circles. Expressions reshape them:
- `.eye.normal` — round and open
- `.eye.closed` — squashed flat (blink/wink)
- `.eye.happy` — a smiling dome/crescent
- `.eye.wide` — bigger and taller (surprised/excited)
- `.eye.sleepy` — a thin, heavy-lidded bar

**Eyebrows (`.brow`):**
Small bars above each eye, invisible by default. `.brow.raise` lifts one or both for surprise; `.brow.furrow` angles one down for a skeptical/annoyed look. Steps can set both eyebrows (`brow`) or just one (`browL` / `browR`) for asymmetric expressions.

**Speech bubble (`#bubble`):**
Appears to the right of the docked orb, stretching from just past her to near the right edge of the screen (`left` + `right`, no fixed width), timed to pop in just after she finishes moving into the corner (~650ms delay). Built from a white rounded rectangle with a grey border and a small triangular tail (`::before`/`::after`) pointing back at her. `buildBubbleText()` in the script splits the message into words, wraps each word's letters in a `.bubble-word` span (`white-space: nowrap`) so the browser only ever wraps between words — never mid-word — and gives each letter its own `<span class="talk-letter">` with a staggered delay. Each letter animates in with a little hop (`letter-talk`: fade + bounce), then settles and stays still — so the whole line animates in like she's talking, without wobbling forever. Hides immediately when undocked.

**Always-on ambient animation (CSS keyframes):**
- `float` — the orb bobs gently up and down
- `breathe` — the orb gently scales in and out
- `glow` — the outer glow softly brightens and dims
- `shadow-pulse` — the ground shadow shrinks and fades as the orb rises

**Expression sequence (small JS state machine):**
The `sequence` array in the `<script>` tag lists short beats — how long to hold an expression, which eye/brow shapes to use, and whether the orb or face itself should flourish. Beats are spaced with long rests (3–4.5s) so expressions read as occasional personality rather than constant fidgeting:
- `pop` / `tilt` / `shake` / `nod` — small flourishes on the whole orb
- `look-left` / `look-right` — gaze shifts sideways
- `roll` — a playful circular eye-roll (`eye-roll` keyframe)

The loop plays through the sequence forever, until interrupted by a click.

**Click to dock:**
Clicking the orb (`#dock`) toggles a docked state — moves to the top-left corner, scales to 55%, pauses the expression loop, resets eyes/brows to neutral, and sways gently in a "thinking" pose. Clicking again reverses it and resumes the loop.

## Options drawer (discreet bottom sheet)

Rather than a visible button, access to the options is a small grey grip-handle (`#sheetHandle`) that only appears once Evia is docked in the top-left corner — it fades in flush against the bottom edge of the screen, easy to miss unless you're looking for it.

**Opening it:**
- Tap the handle, or
- Swipe up on the handle (real touch gesture, not just a tap target — see `addSwipe()` in the script)

Either one slides a bottom sheet (`#sheet`) up from the edge and blurs everything behind it (`#sheetBlur`), the same blur treatment as before. The sheet lists the three options as full-width rows, in this order top to bottom:

- **Chat**
- **QR Code**
- **Options** (closest to the bottom edge/handle)

**Closing it:** tap the handle again, swipe down on the sheet, tap the blurred background, tap any row, or press <kbd>Esc</kbd> — all call the same `setSheetOpen(false)`.

The three rows (`#rowChat`, `#rowQr`, `#rowOptions`) currently just close the sheet on click — wire up real behavior for each inside the `.sheet-row` click handler in the script.

## Installing it as an app

This is a Progressive Web App (PWA): `manifest.json` plus `sw.js` (a minimal service worker) make it installable to a home screen or desktop, with the "Evia" / "Apprentice" icon in `icons/`.

**Requirement:** browsers only offer the install prompt over HTTPS (GitHub Pages qualifies) or on `localhost` — not for a file opened directly from disk.

- **Desktop Chrome/Edge:** open the hosted URL, click the install icon in the address bar (or menu → "Install Evia…").
- **Android Chrome:** open the URL, tap the menu → "Add to Home screen" / "Install app".
- **iOS Safari:** open the URL, tap Share → "Add to Home Screen" (iOS uses the `apple-touch-icon` and meta tags rather than the manifest, which are already wired up in `index.html`).

### Icon

Generated by `make_icons.py` (requires Pillow: `pip install pillow`) — a yellow gradient square with rounded corners, "Evia" in large white text and "Apprentice" in smaller white text below. It writes:
- `icons/icon-192.png`, `icons/icon-512.png` — standard manifest icons
- `icons/icon-512-maskable.png` — edge-to-edge version for adaptive icon masks (Android)
- `icons/apple-touch-icon.png` — 180×180 for iOS
- `icons/favicon-32.png` — browser tab favicon

Re-run the script after editing colors or text, and re-zip/redeploy.

## Customize

- Colors: `--bg`, `--orb-a`, `--orb-b`, `--eye` custom properties at the top of the `<style>` block
- Eye shapes: `.eye`, `.eye.normal`, `.eye.closed`, `.eye.happy`, `.eye.wide`, `.eye.sleepy`
- Eyebrow shapes: `.brow.raise`, `.brow.furrow`
- Orb flourishes: `pop`, `tilt`, `shake`, `nod` keyframes
- Opening flash: `.flash-ring`, `.ripple`, `.flash-core`, `.reveal`, and the `ripple-out` / `flash-core-out` / `orb-in` keyframes
- Speech bubble message/position/timing: `BUBBLE_MESSAGE` in the script, and `#bubble` (position/size) plus the `revealDelay` timeout
- Expression timing/order: edit the `sequence` array in the script
- Docked position/size: `#dock.docked`
- App name/icon/colors: `manifest.json` and `make_icons.py`
- Options drawer: sizing/position in `#sheetHandle` and `#sheet`; swipe sensitivity in the `addSwipe()` thresholds (currently 24px); row labels/icons/actions in the sheet's markup and the `.sheet-row` click handler in the script

`prefers-reduced-motion` is respected: the opening flash, ambient animations, expression flourishes, and letter-bounce are all disabled for users who request it — the bubble still appears (instantly, no pop-in) with plain, fully visible text. The JS expression loop doesn't start either way (clicking to dock/undock still works).

## Deploy on GitHub Pages

1. Push this repo to GitHub (include `index.html`, `manifest.json`, `sw.js`, and the `icons/` folder).
2. In the repo settings, go to **Pages**.
3. Set the source to the `main` branch, root folder.
4. Your page will be live at `https://<username>.github.io/<repo-name>/` — and installable from there.
