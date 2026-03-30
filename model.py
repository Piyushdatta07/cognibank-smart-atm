import numpy as np
from sklearn.ensemble import IsolationForest

X = np.array([
    [10], [20], [50], [100], [150],
    [200], [300], [500], [800], [1000],
    [1200], [1500], [1800], [2000], [2500]
])

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

def predict_fraud(amount):
    pred = model.predict([[amount]])
    return True if pred[0] == -1 else False
