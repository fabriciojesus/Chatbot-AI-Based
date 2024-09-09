import openai
from openai import OpenAI
import requests
import json
from env.koibase import koibase
from dotenv import load_dotenv
import os
#client = OpenAI()
#from openai.embeddings_utils import get_embedding, cosine_similarity
load_dotenv()

# Obter a chave da API a partir da variável de ambiente
api_key = os.getenv('OPENAI_API_KEY')

# Verifica se a chave foi carregada corretamente
if not api_key:
    raise ValueError("A chave da API não foi encontrada. Verifique a variável de ambiente.")

# Configurar o cliente OpenAI com a chave da API
openai.api_key = api_key

headers = {"Authorization": f"Bearer {api_key}", "Content-Type":"application/json"}
#link = "https://api.openai.com/v1/models" link pra ver todos modelos disponiveis
link = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo-0125"

contentmessage = "qual melhor frontend para python"
body_mensagem = {
    "model":id_modelo,
    "messages":[{"role": "user", "content": contentmessage}]
}
body_mensagem = json.dumps(body_mensagem)
requisicao = requests.post(link, headers=headers, data=body_mensagem)

resposta = requisicao.json()
mensagem = resposta["choices"][0]["message"]["content"]
#print(mensagem)
#print(requisicao.text)
def get_embedding(text_to_embed):
    # Embed a line of text
    text_to_embed = "rafael nadal won golden medal for curlin at 2022 olympcs games"
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=[text_to_embed]
    )
    # Extract the AI output embedding as a list of floats
    embedding = response["data"][0]["embedding"]

    return embedding

# text copied and pasted from: https://en.wikipedia.org/wiki/Curling_at_the_2022_Winter_Olympics
# I didn't bother to format or clean the text, but GPT will still understand it
# the entire article is too long for gpt-3.5-turbo, so I only included the top few sections


query = f"""Use the below article koibase create to answer the subsequent question. If the answer cannot be found, use your own knowlodge

Article:
\"\"\"
{koibase}
\"\"\"

Question: quem é o atual CEO da KOI?"""

response = openai.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'You answer questions about Biz in portuguese.'},
        {'role': 'user', 'content': query},
    ],
    model=id_modelo,
    temperature=0,
)

print(response.choices[0].message.content)