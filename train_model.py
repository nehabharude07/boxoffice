import json
import pickle

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

FEATURES = ["title_length", "budget", "opening_theaters", "opening_revenue", "release_days", "domestic_revenue"]

df = pd.read_csv("boxoffice.csv")
df["title_length"] = df["title"].apply(len)
X, y = df[FEATURES], df["world_revenue"]

# 1) Honest check: train on 80%, score on the 20% the model never saw
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
s = StandardScaler().fit(X_tr)
check = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4).fit(s.transform(X_tr), y_tr)
resid = y_te.values - check.predict(s.transform(X_te))

metrics = {
    "rows": int(len(df)),
    "r2": float(r2_score(y_te, check.predict(s.transform(X_te)))),
    "mae": float(mean_absolute_error(y_te, check.predict(s.transform(X_te)))),
    "p10": float(np.percentile(resid, 10)),
    "p90": float(np.percentile(resid, 90)),
    "median": {k: float(v) for k, v in df[FEATURES[1:]].median().items()},
}
json.dump(metrics, open("metrics.json", "w"), indent=2)

# 2) Final model on all data
scaler = StandardScaler()
model = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4)
model.fit(scaler.fit_transform(X), y)
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))
print(f"Held-out R2 {metrics['r2']:.3f} | typical error ${metrics['mae'] / 1e6:,.0f}M")
