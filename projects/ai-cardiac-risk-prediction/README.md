# Cardiac Risk Explorer — ML Methodology Prototype

This is an **educational ML methodology demonstration** for classification, evaluation, stratified data splits, and permutation feature importance. The included code deliberately uses scikit-learn's **breast cancer benchmark**, **not** heart disease records. It therefore **does not estimate cardiac risk**. The cardiovascular application in the name is a future research direction, not an implemented clinical claim.

## Run
```bash
pip install -r requirements.txt
python main.py
```

## Next research steps
- Select a properly licensed cardiovascular dataset and document cohort composition.
- Create a separate cardiac task with valid clinical endpoints and leakage checks.
- Report calibration, confidence intervals, subgroup analysis and external validation.

**Not for medical decisions.**
