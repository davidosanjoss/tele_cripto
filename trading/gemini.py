import os
from google import genai
from pydantic import BaseModel


class Signal(BaseModel):
    side: str
    symbol: str
    leverage: int
    entry: float
    targets: list[float]


async def parse_message(message) -> Signal:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    Você receberá uma mensagem de sinal de trade no seguinte formato:
    
    {message}
    
    Extraia as seguintes informações da mensagem e retorne um JSON com as chaves:
    
    - side: "buy" se a mensagem indicar LONG, caso seja SHORT o valor é "sell"
    - symbol: o valor após "Name:"
    - leverage: o número antes do "X" em "Margin mode"
    - entry: o valor do "Entry price"
    - targets: uma lista com os valores numéricos dos targets, ignorando o "unlimited"
    
    Se a mensagem NÃO estiver exatamente nesse padrão ou faltar algum campo, retorne apenas null.
    
    Por favor, gere apenas o texto do JSON, sem markdown.
    """

    # noinspection PyTypeChecker
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
        config={"response_mime_type": "application/json", "response_schema": Signal},
    )

    return response.parsed
