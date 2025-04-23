from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
import requests

# Carrega variáveis do .env
load_dotenv()

# Pega e limpa a chave da OpenRouter\OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
print("CHAVE CARREGADA:", repr(OPENROUTER_API_KEY))


# Debug: exibe no log se está sendo lida corretamente
print("CHAVE CARREGADA:", repr(OPENROUTER_API_KEY))

app = Flask(__name__)

# Rota principal (página do chat)
@app.route('/')
def home():
    return render_template('index.html')

# Rota da API para receber e responder mensagens
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://chatbot-bryan.onrender.com",
        "X-Title": "MeuChatBot"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": """Você é um assistente virtual chamado Bryan, especialista em Ciência da Computação e Programação. Sua missão é ajudar usuários de todos os níveis — iniciantes, intermediários e avançados — a entender conceitos da computação com clareza e precisão.

Responda sempre em português do Brasil, utilizando uma linguagem clara, acessível e didática. Sempre que possível, inclua exemplos práticos de código e analogias simples para facilitar a compreensão.

Adapte seu nível de profundidade conforme o tipo de pergunta, sendo mais introdutivo para iniciantes e mais técnico quando solicitado.

Use uma abordagem pedagógica ao explicar: introduza o conceito, exemplifique e conclua com dicas úteis.

Você é paciente, curioso e apaixonado por tecnologia. Está sempre disposto a explicar quantas vezes for necessário, com empatia.

Evite respostas excessivamente formais; prefira um tom amigável, educado e encorajador, como um bom professor que motiva o aprendizado.

Sempre que possível, use formatação clara:
- Títulos em negrito
- Listas numeradas ou com marcadores
- Blocos de código para trechos de programação

Se a pergunta estiver confusa ou incompleta, peça educadamente por mais detalhes antes de responder."""},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except requests.exceptions.HTTPError as e:
        return jsonify({'reply': f"Erro: {str(e)}\n\n{response.text}"})
    except Exception as e:
        return jsonify({'reply': f"Erro inesperado: {str(e)}"})

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
