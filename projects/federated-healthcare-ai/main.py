"""Educational federated averaging with synthetic local regression data."""
import numpy as np

def clients(count=4, samples=100, seed=12):
    rng = np.random.default_rng(seed)
    for site in range(count):
        x = rng.normal(loc=site * 0.15, size=(samples, 3))
        y = x @ np.array([1.5, -2., 0.7]) + 0.25 + rng.normal(0, 0.2, samples)
        yield np.column_stack([x, np.ones(samples)]), y

def local_steps(x, y, global_weights, steps=40, lr=0.025):
    weights = global_weights.copy()
    for _ in range(steps):
        gradient = (2.0 / len(y)) * x.T @ (x @ weights - y)
        weights -= lr * gradient
    return weights

def run(rounds=12):
    sites = list(clients())
    global_weights = np.zeros(4)
    for rnd in range(rounds):
        # Only weight updates are aggregated; clients retain their own x and y.
        updates = [local_steps(x, y, global_weights) for x, y in sites]
        sizes = np.array([len(y) for _, y in sites])
        global_weights = np.average(updates, axis=0, weights=sizes)
        mse = np.mean([np.mean((x @ global_weights - y) ** 2) for x, y in sites])
        print(f"round={rnd+1:02d} mean_client_mse={mse:.5f}")
    print("Final shared parameters:", global_weights)
    return global_weights

if __name__ == "__main__":
    run()
