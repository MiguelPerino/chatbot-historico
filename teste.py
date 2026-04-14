from dotenv import load_dotenv
load_dotenv()

from app.services.llm import call_llm


historico = 'que dia é hoje?'

response = call_llm(historico)
print(response)

