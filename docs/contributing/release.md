# Release process

Releases are automated by [release-please](https://github.com/googleapis/release-please)
reading Conventional Commits history on `main`, and published to PyPI via
[Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC — no
long-lived API token stored anywhere).

The **first** public tag is `v0.1.0` from the version already in
`pyproject.toml` and `.release-please-manifest.json`. Do **not** wait for
release-please to invent `0.1.1` for that cut. Later releases: squash to
`develop`, merge-commit to `main`, merge the release-please PR.

## The automated loop (after 0.1.0)

1. Feature PRs squash-merge into `develop`.
2. `develop` merge-commits into `main` (preserving individual conventional
   commits — see [development.md](development.md)).
3. `release-please.yml` (`target-branch: main`) maintains a standing PR
   titled `chore(release): x.y.z`, bumping `[project].version` and
   `CHANGELOG.md`.
4. **Merging that PR is what cuts a release** — human review gate. On merge,
   release-please tags the commit and creates a GitHub Release.
5. `publish-to-pypi.yml` triggers on `release: published`, builds the sdist
   and wheel, and publishes to PyPI via Trusted Publishing. The GitHub
   environment `pypi` requires manual approval — a second human gate.

Nothing in this loop requires hand-bumping a version, hand-writing a
changelog entry, or holding a PyPI API token anywhere.

## One-time GitHub / PyPI setup

Documented so a fork can reproduce it. Parts of this are already done for
`adammatthewsteinberger/cursorloop`.

1. **Create the GitHub repo** `adammatthewsteinberger/cursorloop`, push
   `main` and `develop`. Set **`develop` as the default branch**. Protect
   both with CI + CODEOWNER rulesets.
2. **PyPI → Account settings → Publishing → Add a new pending publisher**
   (repeat on `test.pypi.org` for TestPyPI):

   | Field | Value |
   |---|---|
   | PyPI Project Name | `cursorloop` |
   | Owner | `adammatthewsteinberger` |
   | Repository name | `cursorloop` |
   | Workflow name | `publish-to-pypi.yml` (the **filename** — load-bearing) |
   | Environment name | `pypi` (or `testpypi` on TestPyPI) |

3. **Create the GitHub environments `pypi` and `testpypi`** (Settings →
   Environments) with the maintainer as a required reviewer. URLs:
   `https://pypi.org/p/cursorloop` and
   `https://test.pypi.org/p/cursorloop`.
4. **Protect `main`**: require CI (`ci.yml`) to pass, disallow force-pushes,
   allow merge commits (gitflow).

A PyPI *pending* publisher reserves nothing — the project name isn't claimed
until the first real publish succeeds. Claim `cursorloop` promptly with a
real `0.1.0`.

## TestPyPI dry run

Before promoting `develop` → `main` (or cutting a release), validate the
OIDC + build pipeline against **TestPyPI**. The workflow **always builds
`develop`** for TestPyPI — never `main`. Real PyPI only publishes from a
GitHub Release on `main`.

1. Pending publisher registered at `test.pypi.org` (separate account /
   registry from `pypi.org`).
2. Actions → **Publish to PyPI** → Run workflow → target `testpypi`
   (branch selection in the UI is ignored; checkout is forced to
   `develop`).
3. Approve the `testpypi` environment.
4. Install and smoke:

   ```bash
   python -m venv /tmp/cursorloop-testpypi
   /tmp/cursorloop-testpypi/bin/pip install \
     -i https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple/ \
     cursorloop
   /tmp/cursorloop-testpypi/bin/cursorloop --version
   /tmp/cursorloop-testpypi/bin/cursorloop --help
   ```

   `--extra-index-url` is required so runtime deps resolve from real PyPI.

## First public 0.1.0

1. Merge feature work → `develop` (green CI + CODEOWNER).
2. `workflow_dispatch` TestPyPI (builds `develop`); approve `testpypi`;
   confirm install.
3. Merge `develop` → `main` as a **merge commit**.
4. Create the GitHub Release on `main`:

   ```bash
   gh release create v0.1.0 --target main --title "v0.1.0" --notes-file CHANGELOG.md
   ```

   That fires `release: published` → approve env `pypi` (main only).
5. Confirm `https://pypi.org/project/cursorloop/`, `pip install cursorloop`,
   and `cursorloop --help`.

Later cuts use the release-please PR instead of a hand-cut `gh release create`.

## What CI checks before any of this runs

Every gate in `ci.yml` runs on every push and PR to `main`/`develop`.
`publish-to-pypi.yml` does not re-run the test suite — it trusts that nothing
reaches `main` (protected, CI-gated) without already having passed it, and
its own `build` job runs `twine check --strict` plus a clean-venv console
script smoke as its quality gate. The publish job itself stays minimal
because it holds the OIDC token.

## Verifying a completed publish

- Attestations: `pypa/gh-action-pypi-publish` generates signed attestations
  for Trusted Publishing (PEP 740) — visible on the PyPI project page.
- `py.typed` shipped in the wheel: `unzip -l dist/*.whl | grep py.typed`.
- Metadata: `pypi.org/project/cursorloop/` should show the classifiers,
  keywords, and `[project.urls]` links from `pyproject.toml`.
