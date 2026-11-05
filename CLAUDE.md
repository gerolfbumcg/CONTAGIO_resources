# CONTAGIO_resources

## Mode

ALWAYS stay within this project directory. If settings or files from elsewhere are needed, ASK FIRST. Exception: writing to `~/.claude/*` (plans, memory) is allowed.

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
