# Federated Learning Simulator

A compact implementation of **FedAvg-style** weighted aggregation for linear regression across four simulated clients. Each client retains its synthetic training records; the coordinating process averages model updates by client sample count.

## Run
```bash
pip install -r requirements.txt
python main.py
```

This is a single-process demonstration — not a production federation, healthcare application, or formal privacy protection. **Model updates can leak information**; federated learning alone does not guarantee privacy.

Research extensions: non-IID data experiments, differential privacy, secure aggregation, client dropout and careful evaluation on authorized datasets.
