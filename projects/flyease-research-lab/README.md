# FlyEase Research Lab ✈️

**Data-science pipeline for mobile flight-booking UX.** Inspired by Ibrar's MSc FlyEase work (61-participant survey, SPSS, predictive model comparisons and Figma wireframes). This project **does not use the original participant data** and is **not a reproduction of the research results**.

## Features
- Deterministic **synthetic** survey generator with booking-friction features.
- Leakage-resistant numerical and categorical preprocessing with scikit-learn pipelines.
- Ridge regression compared with a baseline on a held-out test split.
- MAE, R², permutation feature importance and JSON/CSV export.
- Automated unit tests.

## Run

Install dependencies with `python -m pip install -r requirements.txt`, then run:

```bash
python analysis.py --responses 500 --out results
python -m unittest discover -v
```

Generated files appear in `results/`. Synthetic associations are intentionally embedded in the generator, and must **never** be described as empirical findings about travelers. Future work could add consented survey data, reproducible cross-validation, error intervals and usability analysis.
