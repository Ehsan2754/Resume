# Resume

![build](https://github.com/Ehsan2754/Resume/actions/workflows/build.yaml/badge.svg)
![deployment](https://github.com/Ehsan2754/Resume/actions/workflows/deployment.yaml/badge.svg)

One LaTeX source, one PDF per persona. A persona is a small overlay on a shared base, so shared text is edited once and
every persona stays consistent. This repo supersedes the Overleaf `cv/` project: Overleaf is no longer the source of truth.

## Personas

| Id | Headline | Output file | Photo |
|---|---|---|---|
| `A-edgeml` | Embedded Linux & On-Device ML Engineer -- ARM/NPU/GPU vision pipelines | `dist/Shaghaei_Ehsan_Resume_EdgeML.pdf` | no |
| `B-platformfw` (base) | Firmware & Embedded Linux Platform Engineer -- Zynq UltraScale+ / ARM SoCs, kernel, drivers, real-time Ethernet | `dist/Shaghaei_Ehsan_Resume_PlatformFW.pdf` | yes |
| `C-englead` | Engineering Lead, Embedded Linux | `dist/Shaghaei_Ehsan_Resume_EngLead.pdf` | no |
| `D-fae` | Applications Engineer -- ARM SoCs, NPUs, industrial Ethernet, camera sensors | `dist/Shaghaei_Ehsan_Resume_FAE.pdf` | yes |
| `E-lowlatency` | C++ Systems Engineer -- latency-critical pipelines on Linux/ARM (SIMD, DMA, zero-copy networking) | `dist/Shaghaei_Ehsan_Resume_LowLatencyCpp.pdf` | no |

A, D and E currently use the base `Content/` with their own headline (and, for E, Skills before Experience); C has a full overlay.

## Layout

```
resume.tex            skeleton; reads generated headline.tex + includes.tex from the staged build tree
Setting/              theme and packages -- shared, never per persona (single column, same section names: ATS rule)
Content/              BASE content (= persona B)
personas/<id>/        headline.txt, photo.txt ("none" = no photo box), order.txt (section order),
                      and optionally Content/ with only the files that differ (an overlay file replaces the base file wholesale)
archive/              old long-form content, kept for mining, never built
tools/                banned-words.txt, unreconciled.txt, banned-allowlist.txt, hidden_text_check.py
Makefile              stages base + overlay into build/<id>/, compiles with XeLaTeX, runs the checks, writes dist/
```

## Build locally

Needs TeX Live with XeLaTeX, `moderncv`, `fontawesome5`, `academicons`, German babel (`texlive-xetex texlive-latex-extra texlive-fonts-extra texlive-lang-german`), `latexmk`, `poppler-utils`, and `pip install pymupdf`.

```
make                      # all five personas -> dist/
make C-englead            # one persona      -> dist/Shaghaei_Ehsan_Resume_EngLead.pdf
make check PDF=file.pdf   # run only the honesty/ATS gate
make clean
```

## Application overlay (`APP=`)

A job-specific build is a persona plus a third layer kept outside this repo (the JD-specific text lives in a private folder):

```
make C-englead APP=/path/to/application-dir COMPANY=Amazon ROLE=SDM-Nitro
# -> dist/Shaghaei_Ehsan_Resume_Amazon_SDM-Nitro_<YYYY-MM-DD>.pdf
```

`APP` may contain `Content/*.tex` (replaces files), `headline.txt`, `photo.txt` and `order.txt`; all are optional. Application builds run locally, not in CI. Keep every dated PDF you send.

## Releases

Every push to `main` builds the five personas in parallel (GitHub Actions matrix) and publishes ONE release with all five PDFs attached:
tag `build-<YYYY-MM-DD>-<run number>`, name "Resumes <date> (#run)". Pushing a `v*` tag publishes a release under that tag.
See the [Releases page](https://github.com/Ehsan2754/Resume/releases). PDFs marked ⚠️ in the release notes still contain unreconciled placeholders and are not for sending.
The GitHub Pages deployment (`deployment.yaml`) is a cosmetic HTML rendering only.

## Honesty gate

`make` runs `make check` on every PDF, and CI is red if it fails:

- real text layer (at least 150 words), so ATS and screeners read what a person reads;
- no banned words (`tools/banned-words.txt`); the only exemption is a verbatim published paper title in `tools/banned-allowlist.txt`;
- no hidden text: font size under 6 pt, near-white fill, or glyphs outside the page (`tools/hidden_text_check.py`);
- unreconciled numbers and `⚠️` placeholders (`tools/unreconciled.txt`) produce a loud warning. Delete a pattern there once its value is reconciled.

## Credit

The initial template is from this Overleaf [template](https://www.overleaf.com/latex/templates/dhik-lebenslauf-vorlage/jscfzhxchjcw).
