# Upgrade / maintenance backlog

Audit date: 2026-09-29 · baseline commit: `6e817a9`
Last updated: 2026-09-29 (after the local Ruby upgrade and the build-action bump)

Findings from a comparison of the local development installation, the committed
dependency manifests, and the GitHub Actions workflows. Items are ordered by
value, not by effort.

---

## Summary of the core problem

The local workstation and the CI build container disagree about which Ruby and
which Jekyll are in use. Nothing in the repo arbitrates (there is still no
`.ruby-version` or `.tool-versions`).

| Where | Ruby | Jekyll |
| --- | --- | --- |
| Local workstation | 3.4.5 | 4.4.1 |
| CI (`ruby/setup-ruby` + `bundle exec jekyll build`) | 3.4.5 (from `.ruby-version`) | 4.4.1 (from `Gemfile.lock`) |

**Resolved.** Local and CI now run the same Ruby and the same Jekyll, both driven
by files in this repository. `Gemfile.lock` governs the published site, so the
dependency pins and Dependabot alerts apply to production rather than to local
development only. Items 1-3 below record how this was reached.

---

## High value

### 1. Bump `actions/jekyll-build-pages` v1.0.9 -> v1.0.13 — DONE

The action was pinned to an exact patch, so unlike the floating `@v4`-style tags
it received nothing automatically. Upgrading moved the build container from
**Ruby 2.7.4 -> 3.3** and the gem set from **github-pages 228 -> 232**
(Jekyll **3.9.3 -> 3.10.0**).

- [x] Update the pin in `.github/workflows/build.yml`
- [x] Update the pin in `.github/workflows/jekyll-gh-pages.yml`
- [ ] Spot-check a few rendered pages on the live site after the deploy

This narrowed but did not close the local/CI gap: `github-pages` has never
shipped Jekyll 4. **Superseded by item 3**, which removes
`actions/jekyll-build-pages` from both workflows entirely; the bump is recorded
here because it was the intermediate step that shipped first.

### 2. Upgrade local Ruby and pin it — MOSTLY DONE

**The `Gemfile.lock` churn is resolved.** The old Ruby 3.0.7 could not install
`sass-embedded` 1.89.2 (needs >= 3.1), so every `bundle` invocation silently
rewrote the lockfile: `jekyll-sass-converter` 3.1.0 -> 2.2.0 (`sass-embedded`
replaced by `sassc`), the `google-protobuf` / `bigdecimal` / `rake` entries
dropped, and `BUNDLED WITH` 2.6.9 -> 2.5.23. The `check-gemfile.sh` helper was
written to chase exactly this.

Local Ruby is now **3.4.5** (Homebrew) with Bundler **2.6.9**, matching the
lockfile's `BUNDLED WITH` exactly. `bundle install` honours the committed
lockfile with zero drift, and three consecutive `bundle exec` runs leave it
byte-identical.

- [x] Install a supported Ruby locally (3.4.5)
- [x] `bundle install` and confirm `Gemfile.lock` matches HEAD afterwards
- [x] Add a `.ruby-version` file so the version is recorded in-repo rather than
      living only on one workstation (3.4.5; both workflows now read it)
- [ ] Retire `check-gemfile.sh` now that the churn is gone

### 3. Resolve the local/CI Jekyll split — DONE

Local previews rendered with **Jekyll 4.4.1** while the published site was built
with **3.10.0** (github-pages 232), with kramdown 2.5.1 vs 2.3.2 and
`sass-embedded` vs `sassc` behind it. CI emitted `github-pages can't satisfy your
Gemfile's dependencies` on every run.

**Direction chosen:** move both workflows off `actions/jekyll-build-pages` to
`ruby/setup-ruby` + `bundle exec jekyll build`. This is the only option that
makes `Gemfile.lock` govern the published site — and therefore the only one under
which the Dependabot alerts fixed in `6e817a9` mean anything for production. It
is also what GitHub's own warning now recommends.

- [x] Move `jekyll-gh-pages.yml` to a native Jekyll 4 build
- [x] Move `build.yml` to the same toolchain, so a green check predicts a green
      deploy
- [x] Resolve the `github-pages can't satisfy your Gemfile's dependencies` warning

**Regression found and fixed during the migration.** `_layouts/home.html` listed
recent news via `site.categories.news`, whose ordering Jekyll 4 does not
guarantee to match Jekyll 3. Under Jekyll 4 the homepage showed news items from
2014 instead of the current ones. Fixed with an explicit
`| sort: 'date' | reverse`, which behaves identically on both engines. The
`/news/` index was unaffected (it uses `site.posts`), as was `site.related_posts`.

**Verification.** A 24-page random sample was diffed against the live Jekyll 3
site: 21 byte-identical, 3 differing only by blank lines that Jekyll 3 emits and
Jekyll 4 does not. The homepage matches to within two blank lines inside an
excerpt.

Note the comparison must be run with `TZ=UTC` to be meaningful: `_config.yml`
sets no `timezone`, so Jekyll uses the system zone and a local build stamps
`<time datetime>` as `+01:00` where CI stamps `+00:00`. The rendered date text is
identical either way. Setting `timezone:` explicitly would make local and CI
agree, but would change the published offsets, so it is deliberately left alone.

- [ ] Optional: set `timezone:` in `_config.yml` if the `<time datetime>` offsets
      should be stable across machines

---

## Medium value

### 4. Clear the Sass deprecation warnings

Moving off Ruby 3.0.7 restored the real `sass-embedded` (dart-sass) toolchain in
place of the `sassc` (libsass) fallback. dart-sass is far stricter, so 34
deprecation warnings that were always latent are now visible on every build:

| Category | Count |
| --- | --- |
| `color-functions` (`lighten()`, `darken()`) | 10 |
| `global-builtin` | 10 |
| `import` (`@import` vs `@use`) | 9 |
| `slash-div` (`/` as division) | 5 |

These are **not** confined to the vendored `minima` theme. The site's own files
are implicated: `assets/css/main.scss`, `_sass/variables.scss`, `site.scss`,
`typography.scss`, `mixins.scss`, `page.scss`, and `forms.scss`.

Non-blocking today — they are warnings, and the build succeeds. They become hard
errors in dart-sass 3.0, so this is a "fix before it bites" item, not urgent.

Note the compiled CSS did change when the engine switched, but every difference
is an equivalent re-encoding, not a behavioural one: `#1756a9` ->
`rgb(22.948...,86.254...,168.55...)`, `#008080` -> `teal`,
`calc(800px - (30px * 2))` -> `calc(800px - 30px*2)`. No visual change. This
affects local previews only, since CI compiles with its own toolchain.

- [ ] Migrate the site's own `_sass` files off `@import` to `@use`/`@forward`
- [ ] Replace `lighten()` / `darken()` with `color.scale()` / `color.adjust()`
- [ ] Replace `/` division with `math.div()`
- [ ] Decide whether to patch or replace the vendored `minima` 2.5.2 theme,
      which is the source of the remainder

### 5. Refresh the remaining GitHub Actions pins

| Action | Pinned | Latest |
| --- | --- | --- |
| `actions/checkout` | v4 | **v7.0.1** |
| `actions/cache` | v4 | **v6.1.0** |
| `actions/configure-pages` | v4 | **v6.0.0** |
| `actions/deploy-pages` | v4 | **v5.0.1** |
| `actions/upload-pages-artifact` | v3 | **v5.0.0** |
| `lycheeverse/lychee-action` | v2 | v2.9.0 (current) |

`actions/checkout@v4` is the source of the Node 20 deprecation annotation on
every run. `configure-pages` / `upload-pages-artifact` / `deploy-pages` are a
matched set and should be bumped together and tested as a group.

`ruby/setup-ruby` (added in item 3) is pinned to the floating `@v1` major tag,
which is that action's documented convention, so it needs no bump here.

- [ ] Bump `actions/checkout` across all three workflows
- [ ] Bump the Pages action trio together, then verify a full deploy
- [ ] Bump `actions/cache` in `link-checker.yml`

### 6. Remove the vestigial minimal-mistakes theme tooling

`package.json` declares `"name": "minimal-mistakes-theme"` with
`engines.node >= 0.10.0`, but `_config.yml` sets `theme: minima`. The file and
`Gruntfile.js` are leftovers from a theme the site no longer uses. No workflow
references node, npm, or grunt, and there is no `package-lock.json`.

These files are the sole source of the phantom `grunt` Dependabot alerts. They
were pinned rather than removed in `6e817a9`; deleting them is the durable fix
and also stops the seven remaining `grunt-*` dependencies (still on open-ended
`">1.3.0"` ranges) from raising the same alerts in future.

`assets/js/scripts.min.js` is already committed, so deleting the tooling costs
no build output; the only consideration is losing the ability to regenerate it.

- [ ] Delete `package.json`, `Gruntfile.js`, and `.jshintrc`

---

## Low value / housekeeping

### 7. Branch protection is being bypassed

`master` carries a "Changes must be made through a pull request" rule, but
pushes from an account with admin rights bypass it (the remote reported
`Bypassed rule violations for refs/heads/master` on the `6e817a9` push).

- [ ] Decide whether the rule is intended; if so, route future changes through PRs

### 8. Stale Dependabot branches

Superseded by `6e817a9` and safe to prune once confirmed closed:
`dependabot/bundler/addressable-2.9.0`, `dependabot/bundler/json-2.19.9`,
`dependabot/bundler/rexml-3.4.2`, and the older `group-update` branch.

- [ ] Prune merged/superseded remote branches

---

## Already resolved

Recorded for completeness — all four open Dependabot alerts were closed by
`6e817a9` (verified: no open alerts remain).

| Alert | Package | Change |
| --- | --- | --- |
| #9 (high) | `addressable` | 2.8.7 -> 2.9.0 |
| #13 (low) | `json` | 2.12.2 -> 2.21.2 |
| #7 (high) | `grunt` | `">1.3.0"` -> `"^1.6.1"` |
| #6 (moderate) | `grunt` | same |

Caveat: because the deploy does not consume `Gemfile.lock` (see item 1), the two
gem bumps closed the alerts without changing any gem in the published build.
