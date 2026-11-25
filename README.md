# Verified AI-Assisted Workflow

A synthetic CSV shopping-cart workflow shows how fixed acceptance checks caught a rollback defect in an AI-drafted implementation. Both drafts run against the same inputs and expectations. Their JSON reports retain case-level evidence and SHA-256 digests.

## Reproduced local results

| Draft | Matched cases | Exit code | What happened |
| --- | ---: | ---: | --- |
| `v1` | 10/18 | `1` | `outer_discard` expected `{"x": 2}` and observed `{"x": 3, "y": 0}`. The incorrect state carried forward. |
| `v2` | 18/18 | `0` | Copying the cart at the start of each edit lets an outer discard restore the original state. |

[Requirements](requirements.md) · [First report](result-v1.json) · [Corrected report](result-v2.json) · [Case study](CASE-STUDY.md)

## Reproduce locally

Run from the repository root with Python 3.10 or later. The workflow reads the bundled fixtures and uses only the Python standard library. It runs offline.

```sh
python -B verify.py v1
python -B verify.py v2
python -B -m unittest -v
```

Run the commands separately. Exit code `1` from `v1` is expected and exposes the regression. The tests compare each CLI run with the bundled JSON report and verify the expected exit status. Local verification used Windows with Python 3.10.11 and 3.14.7. GitHub Actions is configured for Windows and Linux with both Python series. [Hosted GitHub Actions CI](https://github.com/ryanlupardus/verified-ai-workflow/actions/runs/45376625423) passed all four jobs on Windows and Linux with Python 3.10 and 3.14.

## Evidence and limitations

The 18 cases are fixed, visible synthetic examples. The verifier uses the bundled operation vocabulary. An unknown action can be counted as an expected `ValueError` if the expectation also matches the cart state, so arbitrary CSVs require separate schema and action validation. The results cover the demonstrated rollback, state and error-handling behavior. Concurrency, persistence and production use are outside the sample.

The portfolio founder set the acceptance and reproducibility requirements. Codex wrote both drafts and the checker. [Contributions and AI assistance](CONTRIBUTIONS.md)

## Reuse

This portfolio sample carries no open-source license grant.
