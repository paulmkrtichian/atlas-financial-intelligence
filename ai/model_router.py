import os
from openai import OpenAI


def get_ai_client(provider="local"):
    """
    Return the selected AI provider and model.
    """

    if provider == "local":
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )

        return client, "qwen3:4b"

    elif provider == "cloud":
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "Cloud AI is not configured. "
                "Set OPENAI_API_KEY before using it."
            )

        client = OpenAI(api_key=api_key)

        model = os.getenv("ATLAS_CLOUD_MODEL")

        if not model:
            raise ValueError(
                "Set ATLAS_CLOUD_MODEL to a supported model."
            )

        return client, model

    else:
        raise ValueError(
            f"Unknown AI provider: {provider}"
        )


def generate_ai_response(
    prompt,
    provider="local",
    system_prompt=None
):
    """
    Generate a response using the selected provider.
    """

    client, model = get_ai_client(provider)

    if system_prompt is None:
        system_prompt = (
            "You are Atlas Financial Intelligence. "
            "Analyze financial evidence carefully. "
            "Separate facts, calculations, assumptions, "
            "and hypotheses. Never invent financial data."
        )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False,
        timeout=120
    )

    return response.choices[0].message.content or ""