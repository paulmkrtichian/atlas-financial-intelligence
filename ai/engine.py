from openai import OpenAI

# The local AI model Atlas will use
MODEL = "qwen3:4b"

# Connect to Ollama running on your Mac
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Instructions defining Atlas's behavior
SYSTEM_PROMPT = """
You are Atlas AI, a personal intelligence assistant.

Your purpose is to help the user:
1. Organize tasks and personal projects.
2. Analyze financial information.
3. Conduct research using reliable sources.
4. Automate repetitive workflows.
5. Develop AI and programming skills.

Rules:
- Be accurate and transparent.
- Never invent financial data.
- Distinguish facts from assumptions.
- Never claim to have performed an action unless
  a tool actually performed it.
- Keep explanations clear and concise.
"""


def ask_atlas(message):
    """
    Send a message to the local AI model
    and return its response.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
        extra_body={"think": False},
        timeout=120
    )

    return response.choices[0].message.content

def stream_atlas(message):
    """
    Stream responses from the local Ollama model.
    """

    from openai import OpenAI

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    stream = client.chat.completions.create(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Atlas Financial Research Intelligence. "
                    "Use supplied financial evidence accurately. "
                    "Distinguish verified facts from hypotheses. "
                    "Never invent financial information."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],
        stream=True,
        extra_body={"think": False},
        timeout=120
    )

    for chunk in stream:
        if chunk.choices:
            content = chunk.choices[0].delta.content

            if content:
                yield content