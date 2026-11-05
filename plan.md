# Plan: `roadmap_verona.html` — stage circles + stage icons styled after slide 5

## Context
`roadmap.html` is an SVG infographic, drawn by a script, that sets the overall layout and content you want (5 stages, linked item cards, LINK TODO badges). Its stage circles currently have thin rings, small Nunito text in the stage colour, a decorative rule, and small single-colour icons (80px). Slide 5 (`…_slide_5.pptx.png`) uses a different look: thick, shaded rings in deep navy, teal, cyan-teal, steel blue and slate grey; large bold condensed uppercase text in dark navy; and large two-tone flat icons (dark navy outlines with mid- and light-blue fills). The goal is a new file, `roadmap_verona.html`, that keeps the layout, data and item cards of `roadmap.html` but changes (1) the stage circles and (2) the icons inside them to match slide 5. `roadmap.html` stays as it is.

## Approach
Copy `roadmap.html` to `roadmap_verona.html` and change only the circle rendering and the decor icons. The `STAGES` data, the item cards (`drawItem`), the item icons (`drawIcon` types network/database/…/link), the header and the legend stay as they are.

### 1. Stage circles (render loop, ~lines 780–873)
- **Font**: add `Roboto Condensed` (400/700) to the Google Fonts `@import`. Use it only for the circle text.
- **Ring colours**: add `ring` and `ringDark` fields to each stage, so the item-card colours (`color`/`dark`) stay unchanged:
  - S1 `#1f3d66` / `#13294a` (deep navy)
  - S2 `#4f9e97` / `#357771` (teal)
  - S3 `#4c9ca2` / `#33787f` (cyan-teal)
  - S4 `#3e70a0` / `#29527c` (steel blue)
  - S5 `#5b6571` / `#3d454f` (slate grey)
- **Thickness and shading**: raise `LAYOUT.bubbleR` from 140 to 150 (outer radius). Draw the ring as a full disc with a radial gradient: lighter tone at the inner edge (offset ≈ 80%) running to `ringDark` at the outer edge, which gives the 3D tube effect. Add a drop shadow offset down and to the left (`dx -3, dy 6, blur 9`), as in the slide. Put a white inner disc on top at r ≈ `bubbleR − 27`, so the ring is about 18% of the radius. Give the disc a faint inner-shadow stroke (`rgba(0,0,0,.12)`). Check that the 4th card of Stage 2 (bottom row) still clears the larger circle, and nudge `bottomRowY` by about 10px if it doesn't.
- **Text**: all in near-black navy `#1b2838`, centred, in the upper half:
  - `STAGE N:`: Roboto Condensed 700, about 21px
  - label: 700, about 20px, uppercase, wrapped at about 16 chars with about 22px line height
  - sublabel `(WPx & WPy)`: 400, about 19px
- Remove the decorative rule under the text, which slide 5 doesn't have.

### 2. Stage icons (new `drawStageIcon(parent, type, cx, cy, w)`)
This is a separate function, so the small item icons in `drawIcon` keep their current look. The old decor branches (`cohort`, `tabletVial`, `shieldCert`, `cloudData`, `funnelChart`) move out of `drawIcon` and into it. Every stage uses one shared palette, as in the slide: `line #24384f`, `mid #5f87b0`, `light #c4d6e8`, `white`. Stroke width is about 2.2–2.8px, with round joins. Each icon is drawn about 125px wide at `cy + R·0.45`, so it fills the lower half of the white disc.
1. **cohort**: a central globe (mid fill, dark meridians and parallels). Three person badges sit around it at the top, bottom-left and bottom-right: a light-filled circle, a dark outline, and a head-and-shoulders figure in mid blue. Three curved arrows with arrowheads run on a circle between the badges.
2. **tabletVial**: on the left, a tablet with a dark rounded bezel, a white screen and a home button. The screen holds an image box at top left (mid fill), text lines, and a small line-chart squiggle at the bottom. On the right, a tall test tube with a ribbed cap and mid-blue liquid, standing in a rack with a crossbar, two legs and a base.
3. **shieldCert**: on the left, a shield with a dark outer outline, a mid-blue band, a light inner area and a bold check mark. On the right, a document with a dog-eared top-right corner and text lines. A rosette seal with two ribbon tails overlaps the document's bottom-right corner.
4. **cloudData**: at top left, a light-filled cloud with a mid-blue database cylinder in front of it. Below that, a small org tree of three square nodes. On the right, a large petri dish with a thick dark rim and an inner rim, holding mid-blue microbe blobs and dots with dark outlines.
5. **funnelChart**: at top left, five arrows: dotted origins and curved stems that end in arrowheads pointing down into a mid-blue funnel with a spout. On the right, a monitor with a dark frame and a light screen. The screen holds a bar chart (mid bars), a pie chart with one dark wedge at top right, text lines, and a stand and foot.

Then the render loop calls `drawStageIcon(svg, st.decorIcon, cx, cy + bubbleR*0.45, 125)` in place of `drawIcon(..., 80, st.color)`.

## Files
- **New**: `roadmap_verona.html`, copied from `roadmap.html` and then modified as above
- **Unchanged**: `roadmap.html`

## Verification
- Open `file://…/roadmap_verona.html` in the browser pane and take a full screenshot.
- Zoom into each of the 5 circles and compare it side by side with the same circle in slide 5. Check ring thickness and colour, text size, weight and colour, and how closely each icon matches.
- Check that circle text and icons stay inside the white disc and don't overlap. Check that no item card overlaps a circle, especially Stage 2's 4th card.
- Check that the console shows no errors and that links and hover on the item cards still work.

# Mode

ALWAYS stay within the currently assigned directory (`/Users/g.c.de.boer/projects-old/CONTAGIO/CONTAGIO_resources`). NEVER LEAVE IT!!! If you need to know settings from somewhere else, ASK ME FIRST!!

**Exception:** writing to `~/.claude/*` (e.g. plan files, memory) is allowed.

## Save location
This plan is also saved as `plan.md` in the project folder.
