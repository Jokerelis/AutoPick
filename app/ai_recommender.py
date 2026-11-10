import os
import json
import logging

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)


def recommend_alternatives(
    alternatives,
    preferred_body_type=None,
    client=None
):
    # Atsarginis variantas - pigiausias automobilis
    ranked = sorted(
        alternatives,
        key=lambda car: car["total_price"]
    )

    if not ranked:
        return [], "Fallback"

    # Jei AI isjungtas arba nera API rakto
    if client is None:
        enabled = os.getenv(
            "AUTOPICK_AI_ENABLED", "false"
        ).lower() == "true"

        if not enabled or not os.getenv("OPENAI_API_KEY"):
            return ranked, "Fallback"

    try:
        if client is None:
            client = OpenAI(
                timeout=2.0,
                max_retries=0
            )

        prompt = {
            "preferred_body_type": preferred_body_type,
            "available_cars": ranked
        }

        response = client.responses.create(
            model=os.getenv(
                "OPENAI_MODEL", "gpt-4.1-mini"
            ),
            instructions=(
                "You recommend rental cars. "
                "Choose the most suitable car based on "
                "the customer's preferred body type and price. "
                "You must choose ONLY from the provided cars. "
                "Return ONLY the chosen numeric car_id. "
                "Do not include explanations."
            ),
            input=json.dumps(
                prompt, ensure_ascii=False
            ),
            max_output_tokens=30
        )

        # AI turi grazinti tik automobilio ID
        selected_id = int(response.output_text.strip())

        # Tikriname ar AI pasirinko tikrai egzistuojancia alternatyva
        selected = next(
            (
                car for car in ranked
                if car["car_id"] == selected_id
            ),
            None
        )

        if selected is None:
            return ranked, "Fallback"

        # AI pasirinktas automobilis bus pirmas
        result = [selected] + [
            car for car in ranked
            if car["car_id"] != selected_id
        ]

        return result, "AI"

    except Exception as error:
        logger.warning(
            "AI recommendation failed: %s",
            type(error).__name__
        )

        return ranked, "Fallback"