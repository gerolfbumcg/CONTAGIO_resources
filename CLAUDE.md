# CONTAGIO_resources

## Mode

ALWAYS stay within this project directory. If settings or files from elsewhere are needed, ASK FIRST. Exceptions: writing to `~/.claude/*` (plans, memory) and to Claude's own session scratchpad directory (under `/private/tmp/claude-501/…/scratchpad`) is allowed.

## How the GitHub Pages site is published

- Live site: https://gerolfbumcg.github.io/CONTAGIO_resources/
- The Pages source is **GitHub Actions** (`build_type: workflow`), not a branch.
- The workflow is `.github/workflows/jekyll-gh-pages.yml` ("Deploy Jekyll with GitHub Pages dependencies preinstalled"). It runs on every push to `main`, and you can also run it by hand from the Actions tab (`workflow_dispatch`).
- It builds the **whole repo root** with Jekyll (`source: ./`) and deploys it. There is no `_config.yml` and no `.nojekyll`, so every file is served at its own path, e.g. `/roadmap.html` and `/roadmap_verona.html`.
- The site root (`/`) serves `index.html`. In the repo, that is the older "CONTAGIO Tools – EID Cohort Life Cycle" page.
- A deploy takes about 40 s after a push. Check with `gh run list --limit 3`.

## Choosing the home page (temporary switch)

The workflow step **"Select home page"** chooses which file is served at `/`. It only changes files in the CI checkout; the repo's `index.html` is never modified.

```yaml
      - name: Select home page
        env:
          HOME_PAGE: roadmap_verona.html
```

- **Current setting (since 2026-11-05, until further notice):** `HOME_PAGE: roadmap_verona.html`. The root shows the slide-5-style roadmap, and the original home page stays reachable at `/index_original.html`.
- **To switch back:** set `HOME_PAGE: index.html`, or delete the whole "Select home page" step. Then commit and push to `main`.
- **To show another page:** set `HOME_PAGE` to that file's name, e.g. `roadmap.html`.

## Files

- `index.html`: original home page (EID Cohort Life Cycle)
- `roadmap.html`: 5-stage roadmap, original style
- `roadmap_verona.html`: 5-stage roadmap, styled after slide 5 of the 2026-11-05 global preparedness session (thick rings, Roboto Condensed, two-tone icons)
- `contagio_resources.csv`: resource list
- `plan.md`: design plan for `roadmap_verona.html`
- `wording.json`: all roadmap texts, links, topic order and visibility (source of truth)
- `editor.html`: wording editor (slides, board, live preview); needs `wording_server.py` to save
- `main.py`: entry point, starts the wording editor
- `wording_server.py`: local server for the editor (standard library only); `--export-md` regenerates the table below

## Stage texts: slide 4 vs slide 5

Source images: `2026.11.05_CONTAGIO tools for global preparedness session_slide_4.pptx.png` (slide 4) and `…_slide_5.pptx.png` (slide 5). The texts are transcribed as they appear on the slides; typos on the slides are marked [sic].

**Background:**
- **Slide 5** is the *older* version. Its **look** is what we keep, and `roadmap_verona.html` reproduces it in SVG.
- **Slide 4** is a first attempt at a new version (made with NotebookLM, which garbled the graphics). Its stage order and texts are input for the new content.
- The final wording is chosen by the user and may differ from both slides.

**How wording updates work (one by one, over time):**
- **Single source of truth:** `wording.json`. `roadmap_verona.html` loads it at runtime and shows the `new` wording where it's filled in, otherwise the `current` text. Only the visual style per stage (colours, row/column, icon) stays in `roadmap_verona.html` (`STAGE_STYLE`).
- **Editing:** run `python3 wording_server.py` in this folder. It opens `http://127.0.0.1:8765/editor.html`, a slide-style editor:
  - **Slides view:** one slide per stage title and per topic. Navigate with PgUp/PgDn (or ←/→ outside text fields). Each slide shows the slide 4 / slide 5 / current text, the new wording fields, status (To do / Draft / Final), link, icon, stage and "Show on page".
  - **Board view:** drag cards to reorder them or move them to another stage; the eye button shows or hides a card.
  - **Adding topics:** "+ Add topic" (sidebar, stage slide or board column) creates a new topic with the next free ID in that stage (e.g. `T2.5`, match "New"). Topics added this way can be deleted again; topics from the slides can only be hidden.
  - **Live preview:** the right pane shows `roadmap_verona.html` with the unsaved wording and warns when a text is cut off. Cards are 300px wide and wrap by measured text width; a card shows at most 3 title lines and 6 description lines and grows in height to fit.
  - Every change auto-saves to `wording.json` and regenerates the table below.
- **When the user gives wording in chat instead** (e.g. "T2.3: …"): Claude edits `wording.json` (`topics.T2.3.new.title`/`new.desc`, or `stages[n].new.label`/`new.sublabel`), runs `python3 wording_server.py --export-md` to regenerate the table, checks the page via the local server, and asks before committing and pushing.
- **Publishing:** commit `wording.json` (and CLAUDE.md) and push to `main`; the live site picks it up in about 40 s.
- **Standalone copy:** "Export static HTML" in the editor, or `python3 main.py --export-static`, writes `roadmap_static.html` with the wording embedded (`<script id="wording-data">`, inserted at the `static-export` marker in `roadmap_verona.html`). It works without a server; a plain "Save Page As" copy does not. The export is not committed by default.
- `main.py` only starts the editor (`python3 main.py` = `python3 wording_server.py`). It used to hold an unrelated Posit Connect test with a hard-coded API key; that code was removed on 2026-11-06 and was never committed. Never put credentials in this repo.

### Numbering scheme
- **Row ID `T<stage>.<n>`**: one row per topic. `<stage>` follows the stage order of **slide 4**, which `roadmap_verona.html` also uses since 2026-11-05: 1 Cohort Preparedness, 2 Navigating Ethics & Governance, 3 Design Data & Sample Collection Tools, 4 Data & Sample Management & Sharing, 5 Integration & Analysis.
- **`S4-<stage>.<n>`**: item *n* of stage *stage*, as numbered on slide 4 (top to bottom).
- **`S5-<stage>.<n>`**: item *n* of stage *stage*, as numbered on **slide 5**. On slide 5, stages 2 and 3 are in the other order: S5 stage 2 = Rapid Data & Sample Collection and S5 stage 3 = Ethics & Governance. Each item is assigned to the stage whose text block it sits in on slide 5.
- **Match**: Same = identical text · Similar = same tool, different wording · Partial = only partly covered · — = no counterpart.
- **Verona**: where the topic is now in `roadmap_verona.html`: ✓ stage and card number, or – when hidden. Topic IDs never change, even when a topic moves to another stage.
- **New wording**: the user's chosen wording (**title**: description), with its status (draft/final).

<!-- wording-table:start -->
_Generated from `wording.json` by `wording_server.py` on every save. Do not edit this table by hand._

### Stage headers

| Stage | Slide 4 | Slide 5 | New wording |
|---|---|---|---|
| 1 | STAGE 1: Cohort Preparedness (WP1 & WP2) | STAGE 1: COHORT PREPAREDNESS (WP1 & WP2) |  |
| 2 | STAGE 2: Navigating Ethics & Governance (WP3 & WP4) | STAGE 3: ETHICS & GOVERNANCE (WP3) |  |
| 3 | STAGE 3: Design Data & Sample Collection Tools (WP2 & WP4) | STAGE 2: RAPID DATA & SAMPLE COLLECTION (WP2 & WP4) |  |
| 4 | STAGE 4: Data & Sample Management & Sharing (WP3, WP4 & WP2) | STAGE 4: DATA & SAMPLE MANAGEMENT AND SHARING (WP2-3-4) |  |
| 5 | STAGE 5: Integration & Analysis | STAGE 5: INTEGRATION & ANALYSIS |  |

### Item comparison

| ID | Slide 4 | Slide 5 | Match | Verona | New wording |
|---|---|---|---|---|---|
| **T1.1** | **S4-1.1** Build Consortium Platform: Connects research networks with capabilities for outbreak response. | **S5-1.1** BUILD YOUR CONSORTIUM: Establish Global Research Connections via Cohort Preparedness Platform to connect capabilities. | Similar | ✓ stage 1, #1 |  |
| **T1.2** | **S4-1.2** Existing Data Discovery: Accesses EMBL Pathogens Portal for existing data and samples. | **S5-1.2** DATA DISCOVERY: Access the EMBL Pathogens Portal to leverage existing relevant data and samples. | Similar | ✓ stage 1, #2 |  |
| **T1.3** | **S4-1.3** Standardised Population Protocols: Deploys 5x5 protocols across diverse population groups. | **S5-1.4** Standardised Population Protocols: Deploys 5x5 protocols across diverse population groups. | Same (Pasted box on slide 5.) | – (stage 1, hidden) |  |
| **T1.4** | **S4-1.4** Public Health Integration: Aligns regional priorities with public health authorities. | **S5-1.3** PUBLIC HEALTH ALIGNMENT: Integrate with Regional Authorities using the ‘Integration’ tool to define priorities and coordination. | Similar (Slide 5 names the 'Integration' tool.) | ✓ stage 1, #3 |  |
| **T2.1** | **S4-2.1** Broad Consent Guidelines: Provides guidelines and templates for broad informed consent. | **S5-3.1** ACCELERATED CONSENT PROCEDURES: Implement standardized Broad Consent Guidelines and templates. | Similar | ✓ stage 2, #1 |  |
| **T2.2** | **S4-2.2** Ethics Application Guidelines: Establishes framework to streamline ethics committee applications. | **S5-3.2** STREAMLINED ETHICAL APPROVAL: Use established guidelines and templates for Ethics Committee Applications during emergencies. | Similar | ✓ stage 2, #2 |  |
| **T2.3** | **S4-2.3** Standardised Approval Templates: Bypasses longthy [sic] legal drofting [sic] to accelerate approvals. | — | — | – (stage 2, hidden) |  |
| **T2.4** | **S4-2.4** IRB Baseline Templates: Simplifies applications for healthy baseline sample collection. | — | — | – (stage 2, hidden) |  |
| **T3.1** | **S4-3.1** Pre-Built eCRF Extensions: Deploys ISARIC-partnered eCRF extensions and cohort-specific modules. | **S5-2.1** IMMEDIATE PATIENT DATA COLLECTION: Access Pre-built eCRF Extensions developed with ISARIC for harmonized data. | Similar | ✓ stage 3, #1 |  |
| **T3.2** | **S4-3.2** Harmonised Data Dictionary: Standardises clinical data fields across research sites. | — | Partial (Only 'harmonized data' in S5-2.1.) | – (stage 3, hidden) |  |
| **T3.3** | **S4-3.3** LINK Tool Integration: Utilises Language Integration Networking Kit for multi-stle [sic] coordination. | **S5-3.3** LINK Tool Integration: Utilises Language Integration Networking Kit for multi-stle [sic] coordination. | Same (Pasted box, placed in the Ethics block on slide 5.) | ✓ stage 3, #4 |  |
| **T3.4** | **S4-3.4** Standardised Sample Templates: Provides protocols for blood and baseline sample storage. | **S5-2.2** UNIFORM SAMPLE COLLECTION TEMPLATES: Utilize pre-built templates for Standardized Specimen Storage across sites. | Similar | ✓ stage 3, #2 |  |
| **T3.5** | **S4-3.5** Legal Compliance Templates: Assists sites with local and national regulatory compliance. | **S5-2.3** ETHICAL AND LEGAL FRAMEWORKS: Access Regulatory Compliance resources and templates for local legal requirements. | Similar (Slide 5 drops 'national'.) | ✓ stage 3, #3 |  |
| **T4.1** | **S4-4.1** DAC Request Roadmap: Guides Data Access Committee request reviews and approvals. | **S5-4.1** TRANSPARENT DATA REQUEST REVIEWS: Follow Data Access Committee (DAC) Roadmap and use DTA templates. | Similar | ✓ stage 4, #1 |  |
| **T4.2** | **S4-4.2** MTA/MDTA Guidelines: Provides templates for material and data transfer agreements. | — | Partial (Only 'DTA templates' in S5-4.1.) | – (stage 4, hidden) |  |
| **T4.3** | **S4-4.3** Virtual Biorepository Cataloguing: Cataloge [sic] biological specimens in the Virtual Biorepository System. | **S5-4.2** GLOBAL SPECIMEN CATALOGING: Use the Virtual Biorepository System (VBS) for global governance framework cataloging. | Similar | ✓ stage 4, #2 |  |
| **T4.4** | **S4-4.4** 10x10 Sharing Project: Implements sample access policies, protocols, and ICF templates. | **S5-4.3** FACILITATED SAMPLE SHARING POLICIES: Apply 10x10 Sharing Project policies for flow of physical materials. | Similar (Slide 5 drops protocols and ICF templates.) | ✓ stage 4, #3 |  |
| **T5.1** | **S4-5.1** Multimodal Data Pipeline: Funnels data using Pathogens Portal Interoperability standards. | **S5-5.1** PATHOGENS PORTAL INTEGRATION: Flow multimodal data through Interoperable Data Pipeline standards for immediate use, using established interoperability standards. | Similar | ✓ stage 5, #1 |  |
| **T5.2** | **S4-5.2** Governance Framework Activation: Activates operational flow for data and physical samples. | — | — | – (stage 5, hidden) |  |
| **T5.3** | **S4-5.3** Measurement Error Guidance: Ensures high-quality research data during emerging infectious outbreaks. | **S5-5.2** HIGH-QUALITY RESEARCH STANDARDS: Address measurement errors using EID Measurement Guidance to ensure data integrity. | Similar | ✓ stage 5, #2 |  |

**Summary:** 20 topics; slide 5 has 15 of them (2 Same, 13 Similar) and 2 more partly. `roadmap_verona.html` shows 14. New wording entered for 0, of which 0 final.
<!-- wording-table:end -->
