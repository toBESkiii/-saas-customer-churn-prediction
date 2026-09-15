import json

from fastapi.testclient import TestClient

from api.main import (
    app,
    customer_health_data,
    feature_columns
)


client = TestClient(app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "SaaS Customer Churn Prediction API is running."
    )


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


def test_prediction_endpoint():

    sample_customer = (
        customer_health_data[
            feature_columns
        ]
        .dropna()
        .iloc[0]
    )

    prediction_payload = {
        "features": json.loads(
            sample_customer.to_json()
        )
    }

    response = client.post(
        "/predict",
        json=prediction_payload
    )

    assert response.status_code == 200

    prediction = response.json()

    assert (
        0
        <= prediction["churn_probability"]
        <= 1
    )

    assert prediction["risk_level"] in [
        "Low",
        "Medium",
        "High"
    ]