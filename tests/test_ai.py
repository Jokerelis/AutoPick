
from types import SimpleNamespace

from app.ai_recommender import recommend_alternatives


cars = [
    {
        "car_id": 7,
        "brand": "Subaru",
        "model": "Forester",
        "body_type": "SUV",
        "total_price": 135.0
    },
    {
        "car_id": 9,
        "brand": "VW",
        "model": "Polo",
        "body_type": "Hatchback",
        "total_price": 90.0
    }
]


def fake_client(answer):
    return SimpleNamespace(
        responses=SimpleNamespace(
            create=lambda **kwargs: SimpleNamespace(
                output_text=answer
            )
        )
    )


def test_ai_valid_recommendation():
    result, source = recommend_alternatives(
        cars,
        preferred_body_type="SUV",
        client=fake_client("7")
    )

    assert source == "AI"
    assert result[0]["car_id"] == 7


def test_ai_invalid_recommendation():
    result, source = recommend_alternatives(
        cars,
        client=fake_client("9999")
    )

    assert source == "Fallback"
    assert result[0]["car_id"] == 9


def test_ai_service_error():
    def fail(**kwargs):
        raise RuntimeError("AI service unavailable")

    client = SimpleNamespace(
        responses=SimpleNamespace(create=fail)
    )

    result, source = recommend_alternatives(
        cars,
        client=client
    )

    assert source == "Fallback"
    assert result[0]["car_id"] == 9
