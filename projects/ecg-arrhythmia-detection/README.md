# ECG Rhythm Lab — Synthetic Time-Series CNN

A reproducible PyTorch 1-D convolutional neural network to classify **synthetic waveforms**. Includes a deterministic generator, train/holdout split, training loop, and accuracy reporting.

## Run
```bash
pip install -r requirements.txt
python main.py --epochs 5
```

**Important:** The waveforms are generated sine waves, **not physiological ECGs**. Holdout accuracy is not arrhythmia-detection performance. This is a software learning demo, not a diagnostic model.

## Research extensions
Compare against PhysioNet datasets (subject to dataset terms), use patient-level splits, assess class imbalance, evaluate sensitivity/specificity and calibration, and document ethical data handling.
