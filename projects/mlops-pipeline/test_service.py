from service import predict, train_model

def test_baseline():
    _, accuracy = train_model()
    assert accuracy >= 0.80

def test_prediction_is_valid_class():
    assert predict([5.1, 3.5, 1.4, 0.2]) in (0, 1, 2)
