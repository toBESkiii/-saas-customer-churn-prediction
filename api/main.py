from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# --------------------------------------------------
# Application setup
# --------------------------------------------------
app = FastAPI(
    title="SaaS Customer Churn Prediction API",
    description="API for customer churn risk prediction and health scoring.",
    version="1.0"
)


# --------------------------------------------------
# Project paths
# --------------------------------------------------
project_root = Path(__file__).resolve().parent.parent

model_path = (
    project_root
    / "models"
    / "balanced_logistic_churn_pipeline.joblib"
)

customer_health_path = (
    project_root
    / "data"
    / "processed"
    / "customer_health_scores.csv"
)


# --------------------------------------------------
# Load model and existing customer results
# --------------------------------------------------
churn_model = joblib.load(model_path)

customer_health_data = pd.read_csv(
    customer_health_path
)


# --------------------------------------------------
# Model feature names
# --------------------------------------------------
feature_columns = [
    "industry",
    "country",
    "referral_source",
    "initial_plan_tier",
    "customer_tenure_days",
    "subscription_count",
    "ever_upgraded",
    "ever_downgraded",
    "latest_plan_tier",
    "latest_seats",
    "seat_change",
    "latest_mrr",
    "latest_is_trial",
    "latest_billing_frequency",
    "latest_auto_renew",
    "plan_changed",
    "usage_event_count",
    "total_usage_count",
    "unique_features_used",
    "active_usage_days",
    "beta_usage_events",
    "errors_per_100_usage",
    "average_duration_per_event",
    "average_usage_per_event",
    "days_since_last_usage",
    "ticket_count",
    "has_support_tickets",
    "average_first_response_minutes",
    "average_resolution_hours",
    "average_satisfaction_score",
    "has_satisfaction_score",
    "escalation_count",
    "days_since_last_support_ticket"
]


# --------------------------------------------------
# Request format
# --------------------------------------------------
class PredictionRequest(BaseModel):
    features: dict[str, Any]


# --------------------------------------------------
# Basic API health check
# --------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "SaaS Customer Churn Prediction API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True
    }


# --------------------------------------------------
# Existing customer lookup
# --------------------------------------------------
@app.get("/customers/{account_id}")
def get_customer(account_id: str):

    customer = customer_health_data[
        customer_health_data["account_id"] == account_id
    ]

    if customer.empty:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer.iloc[0].to_dict()


# --------------------------------------------------
# Churn prediction endpoint
# --------------------------------------------------
@app.post("/predict")
def predict_churn(request: PredictionRequest):

    missing_features = [
        feature
        for feature in feature_columns
        if feature not in request.features
    ]

    if missing_features:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Missing required features",
                "missing_features": missing_features
            }
        )

    input_data = pd.DataFrame(
        [
            {
                feature: request.features[feature]
                for feature in feature_columns
            }
        ]
    )

    churn_probability = (
        churn_model.predict_proba(input_data)[0][1]
    )

    churn_probability_percent = round(
        churn_probability * 100,
        1
    )

    health_score = round(
        100 - churn_probability_percent,
        1
    )

    if churn_probability >= 0.60:
        risk_level = "High"

    elif churn_probability >= 0.40:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return {
        "churn_probability": round(
            float(churn_probability),
            4
        ),
        "churn_probability_percent":
            churn_probability_percent,
        "health_score": health_score,
        "risk_level": risk_level
    }