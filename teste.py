from dotenv import load_dotenv
load_dotenv()

from app.services.llm import call_llm


historico = 'qual a linguagem de programação mais utilizada?'

response = call_llm(historico)
print(response)

