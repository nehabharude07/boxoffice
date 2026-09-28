# Box Office Revenue Prediction

A Flask-based machine learning application that predicts a movie's worldwide box-office revenue using an XGBoost regression model.

## Project Overview

This project uses movie information such as:

* Movie title length
* Budget
* Opening theaters
* Opening revenue
* Days in theaters
* Domestic revenue

The application predicts:

* Estimated worldwide revenue
* Lower revenue estimate
* Higher revenue estimate
* Estimated profit
* Revenue-to-budget multiple

## Tech Stack

* Python
* Flask
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* HTML/CSS/JavaScript
* Pickle

## Machine Learning Model

The project uses **XGBRegressor** for worldwide box-office revenue prediction.

The features used by the model are:

```text
title_length
budget
opening_theaters
opening_revenue
release_days
domestic_revenue
```

### Model Training

The dataset is divided into:

```text
80% Training Data
20% Testing Data
```

The test data is held out during training and is used to calculate:

* R² Score
* Mean Absolute Error
* P10 residual
* P90 residual

The final model is then trained using the complete dataset.

## Project Structure

```text
boxoffice/
│
├── app.py
├── train_model.py
├── boxoffice.csv
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   └── js/
│
├── model.pkl
├── scaler.pkl
└── metrics.json
```

> `model.pkl`, `scaler.pkl`, and `metrics.json` are generated files and are excluded from Git using `.gitignore`.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/boxoffice.git
cd boxoffice
```

Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv env
```

Activate it:

```powershell
.\env\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Train the Model

Before running the application, train the model:

```powershell
python train_model.py
```

This generates:

```text
model.pkl
scaler.pkl
metrics.json
```

## Run the Flask Application

```powershell
python app.py
```

The application will run at:

```text
http://127.0.0.1:5162
```

Open the URL in your browser.

## Prediction API

The application provides a POST endpoint:

```text
POST /predict
```

Example JSON request:

```json
{
    "title": "Example Movie",
    "budget": 100000000,
    "opening_theaters": 4000,
    "opening_revenue": 50000000,
    "release_days": 90,
    "domestic_revenue": 200000000
}
```

The API returns information including:

```json
{
    "title": "Example Movie",
    "prediction": 450000000,
    "low": 400000000,
    "high": 500000000,
    "profit": 350000000,
    "multiple": 4.5
}
```

## Input Validation

The application validates the following ranges:

| Feature          |                     Range |
| ---------------- | ------------------------: |
| Title            |     Maximum 80 characters |
| Budget           | $100,000 – $1,000,000,000 |
| Opening Theaters |                1 – 10,000 |
| Opening Revenue  |       $0 – $1,000,000,000 |
| Days in Theaters |                   1 – 365 |
| Domestic Revenue |       $0 – $2,000,000,000 |

## Model Evaluation

The training script evaluates the model on a held-out 20% test set.

The generated `metrics.json` contains:

```text
rows
r2
mae
p10
p90
median
```

The application uses the residual percentiles to provide a lower and higher prediction estimate.

## Important Files

### `app.py`

Runs the Flask web application and exposes the prediction endpoint.

### `train_model.py`

Loads the dataset, trains the XGBoost model, evaluates it, and saves the model and scaler.

### `boxoffice.csv`

Contains the movie data used for training.

### `model.pkl`

Saved trained XGBoost model.

### `scaler.pkl`

Saved StandardScaler used during model training.

### `metrics.json`

Contains model evaluation metrics and prediction-error information.

## Disclaimer

This project is intended for educational and demonstration purposes. Predictions are model estimates and should not be treated as guaranteed box-office results.
