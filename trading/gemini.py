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


async def generate_signal(ticker):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
Você é um gerador de sinais de trading para criptomoedas. 

**Instruções:**
1. Gere uma mensagem no formato abaixo, usando os dados do JSON fornecido.
2. **Side:** Escolha aleatoriamente entre 🟢 Long ou 🔴 Short.
3. **Margin mode:** Use "Cross" com leverage aleatório entre (10X), (15X), (25X) ou (50X).
4. **Entry price:** Use o valor de 'ask' do JSON, arredondado para 4 casas decimais.
5. **Targets:** Calcule 4 níveis usando estas regras:
   - Para LONG: entry_price × (1 + 0.5%), (1 + 1%), (1 + 1.5%), (1 + 2%)
   - Para SHORT: entry_price × (1 - 0.5%), (1 - 1%), (1 - 1.5%), (1 - 2%)
   - Mantenha 4 casas decimais
   - O 5º target sempre será "🔝 unlimited"

**Formato da mensagem:**
🟢 Long/🔴 Short
Name: [SYMBOL]
Margin mode: Cross ([LEVERAGE]X)

↪️ Entry price(USDT):
[ENTRY]

Targets(USDT):
1) [TARGET1]
2) [TARGET2]
3) [TARGET3]
4) [TARGET4]
5) 🔝 unlimited

**Exemplo com JSON:**
{
  "ask": 0.2863,
  "symbol": "SONIC/USDT:USDT"
}

**Saída correspondente:**
🟢 Long
Name: SONIC/USDT
Margin mode: Cross (50X)

↪️ Entry price(USDT):
0.2863

Targets(USDT):
1) 0.2892
2) 0.2920
3) 0.2949
4) 0.2978
5) 🔝 unlimited

**Dados atuais:**
{ticker}

Gere APENAS a mensagem formatada, sem markdown.
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
    )
    return response.text
