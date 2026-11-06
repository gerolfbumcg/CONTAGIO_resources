# CONTAGIO resources

Web pages presenting the CONTAGIO tools for epidemic preparedness, including the
**5-Stage Roadmap for Rapid Epidemic Response**.

**Live site:** https://gerolfbumcg.github.io/CONTAGIO_resources/

## Pages

| Page | What it is |
|---|---|
| `roadmap_verona.html` | 5-stage roadmap in the slide style (thick stage rings, two-tone icons). **Currently the home page** of the live site. |
| `roadmap.html` | Earlier version of the roadmap, original style. |
| `index.html` | Original home page (EID Cohort Life Cycle). Online at `/index_original.html` while the roadmap is the home page. |
| `editor.html` | Wording editor for the roadmap (see below). Read-only on the live site. |

## Editing the roadmap texts

All texts, links, topic order and visibility of the roadmap live in **`wording.json`**.
`roadmap_verona.html` loads that file, so you never need to edit the HTML to change wording.

Start the editor from this folder (Python 3.9+, no packages needed):

```bash
python3 main.py
```

This opens http://127.0.0.1:8765/editor.html:

- **Slides view:** one slide per stage title and per topic (IDs `T1.1` … `T5.3`). Each shows the
  reference texts from the slides next to fields for the new wording, plus status
  (To do / Draft / Final), link, icon and "Show on page". Navigate with PgUp/PgDn.
- **Board view:** drag cards to reorder topics or move them to another stage; show/hide them;
  add new topics with "+ Add topic".
- **Live preview:** the roadmap with your changes, including a warning when text is cut off.

Changes are saved automatically to `wording.json` (and to the comparison table in `CLAUDE.md`).
Stop the editor with Ctrl+C.

Options: `python3 main.py --port 9000`, `--no-browser`, or `--export-md` to only regenerate the
table in `CLAUDE.md`.

## Standalone copy (static HTML)

`roadmap_verona.html` loads its texts from `wording.json`, so a browser "Save Page As" copy
does not work on its own. To get a single file that opens anywhere (e-mail, USB stick,
SharePoint) without a server, export it:

- in the editor: **Export static HTML** (top right) downloads `roadmap_static.html` with the
  current wording built in (also works in the read-only editor on the live site);
- or from the command line:

```bash
python3 main.py --export-static
```

This writes `roadmap_static.html` in this folder (or pass another file name). Without internet
the page falls back to system fonts; everything else works offline. To get a PDF, open the page
and use Print → Save as PDF.

## Publishing

The site is built by GitHub Actions (`.github/workflows/jekyll-gh-pages.yml`) on every push to
`main`. After editing:

```bash
git add wording.json CLAUDE.md
```

```bash
git commit -m "Update roadmap wording"
```

```bash
git push
```

The live site updates about a minute later.

### Which page is the home page

The workflow step **"Select home page"** sets `HOME_PAGE` (now `roadmap_verona.html`).
Set it to `index.html` to restore the original home page. See `CLAUDE.md` for details.

## Files

| File | Purpose |
|---|---|
| `wording.json` | Roadmap content (source of truth for `roadmap_verona.html`) |
| `editor.html` | Wording editor UI |
| `wording_server.py` | Local server for the editor (standard library only) |
| `main.py` | Starts the editor |
| `contagio_resources.csv` | Resource list |
| `CLAUDE.md` | Working notes and the slide 4 / slide 5 comparison table |
| `plan.md` | Design plan for `roadmap_verona.html` |

---

CONTAGIO is funded by the European Union's Horizon Europe programme under Grant Agreement N. 101137283.
