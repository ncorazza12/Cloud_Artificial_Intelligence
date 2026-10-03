import json, urllib.request, urllib.error
from getpass import getpass

KEY = getpass("Cole a chave (nao aparece na tela): ").strip()
BASE = "https://generativelanguage.googleapis.com/v1beta"

def chamar(url, corpo=None):
    dados = json.dumps(corpo).encode() if corpo else None
    req = urllib.request.Request(url, data=dados, headers={
        "Content-Type": "application/json", "X-goog-api-key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]

status, dados = chamar(f"{BASE}/models?pageSize=200")
print("Listagem de modelos:", status)
if status == 200:
    for m in dados.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []) and "flash" in m["name"]:
            print(" -", m["name"])

status, dados = chamar(f"{BASE}/models/gemini-flash-latest:generateContent",
    {"contents": [{"parts": [{"text": "Responda apenas: ok"}]}]})
print("Teste de geracao:", status)
print(json.dumps(dados, ensure_ascii=False)[:600])