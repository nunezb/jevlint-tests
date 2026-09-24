# jevlint benchmark

[Open the interactive report](report.html) · [Sources and provenance](SOURCES.md) · [Data licenses](DATA-LICENSE.md)

This repository records `jevlint 1.2.0` run over 27 Jev query files drawn from a measurement program that predates the linter. The queries were not written against its rule set. The report and data cover this 27-file study only.

## Results

- The code-only pass produced 40 findings: 0 errors, 12 warnings, and 28 advice.
- The first model pass produced 16 errors, 23 warnings, and 54 advice across 143 API calls. All 27 query runs completed. Exit codes were 16×0, 10×1, and 1×3. Exit 0 means no error-severity finding; warnings and advice can still be present. Exit 3 means a check could not decide because readings straddled its trigger.
- In the second pass, 23 of 27 files had the same finding set. The four changes were all within 0.05 of a check trigger.
- `question/refers-to-sibling` fired as an error on 4 of 6 known-good MMLU files. Their instruction says “the question above,” apparently read as a sibling-question reference.
- The FOLIO and rubric files had no model findings. `query/overlapping-questions` fired on all five probability files, where the source program measured Jev agreeing with both contradictory claims on 9 of 47 items.

The known-good set is small, so these results identify candidate false positives and useful patterns; they do not establish per-check false-positive rates. See the report for per-file results, the second pass, probe results, and caveats.

## What was run

1. `jevlint check --static-only` on all 27 files: 40 findings, no API calls.
2. `jevlint check` on all 27 files: 143 calls.
3. A second full model pass: 142 calls, with three extra runs of the file that ended undecided.
4. Re-send probes on six files: 37 calls.

The archived second pass and retries are under `reports/run2/`. The probe transcripts are under `resend-tests/`. During the recorded run on 2026-09-23, no API errors or billed cost were observed. Reruns call the live API; current quota and charges may differ.

## Files

| Path | Contents |
| --- | --- |
| `report.html` | Self-contained snapshot of the visual report; the rerun script does not rebuild it |
| `queries/` | The 27 request bodies, one file each, as sent |
| `annotations/queries_with_evidence.json` | Per-query provenance summary, measured evidence, and recorded linter behaviour |
| `reports/static_reports.json` | Code-only reports |
| `reports/model_reports.json` | First-pass model reports, including per-file call counts |
| `reports/summary.json` | First-pass totals |
| `reports/run2/` | Second-pass per-file reports, exit codes, and extra runs of the undecided file |
| `resend-tests/` | Recorded probe transcripts |
| `run_experiment.py` | Reproduces the static pass, one model pass, and probes |
| `SOURCES.md` | Sampling summary, dataset sources, attribution, and known traceability gaps |
| `LICENSE`, `DATA-LICENSE.md` | Code license and data/content license notes |

## Reproduce the first pass and probes

Requires Python 3.10 or newer and `jevlint` 1.2.0:

```sh
python3 -m pip install "jevlint==1.2.0"
export TYPESAFE_API_KEY=...   # or TYPESAFE_KEY
python3 run_experiment.py
```

The static pass needs no key. The model pass and probes call the live API. Set `JEVLINT_BENCH_RESENDS=0` to skip the probes. The script writes the first-pass reports to `reports/static_reports.json` and `reports/model_reports.json`; preserve copies first if you need to keep the archived reports unchanged. It does not rerun the second pass or retries, and it does not regenerate `report.html`.

## Provenance limits

The annotations contain the measured-evidence summaries used in the report. The original source-program population, row-level records for every selected item, and analysis scripts are not included, so those population measurements cannot all be independently recomputed from this repository. `SOURCES.md` records the available source pointers and gaps.
