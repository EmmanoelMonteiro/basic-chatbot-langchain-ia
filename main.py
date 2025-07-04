import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a URL do servidor LM Studio das variáveis de ambiente
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL")

if not LM_STUDIO_BASE_URL:
    print("Erro: A variável de ambiente LM_STUDIO_BASE_URL não está configurada no arquivo .env")
    print("Por favor, adicione LM_STUDIO_BASE_URL=http://localhost:1234/v1 ao seu arquivo .env")
    exit()

# --- Função de Teste de Conexão com o LLM ---
def testar_conexao_llm():
    """
    Tenta se comunicar com o LLM rodando no LM Studio para verificar a conexão.
    """
    print("\n--- Testando conexão com o LLM no LM Studio ---")
    try:
        llm = OpenAI(
            base_url=LM_STUDIO_BASE_URL,
            api_key="lm-studio",  # Chave API fictícia, necessária para a classe OpenAI
            temperature=0.01, # Temperatura baixa para respostas mais previsíveis no teste
        )
        response = llm.invoke("Qual é o seu nome?")
        print(f"Resposta do LLM (teste): {response.strip()}")
        if "llama" in response.lower() or "llm" in response.lower() or "linguagem" in response.lower():
            print("Conexão com o LM Studio bem-sucedida! O LLM respondeu.")
            return True
        else:
            print("Conexão com o LM Studio OK, mas a resposta do LLM não é a esperada. Verifique o modelo.")
            return True # Consideramos a conexão OK se houve resposta, mesmo que não ideal.
    except Exception as e:
        print(f"Erro ao conectar ou interagir com o LLM: {e}")
        print("Certifique-se de que o LM Studio está rodando e o servidor está ativo na porta correta.")
        print(f"Verifique se o modelo está carregado e sendo 'served' em: {LM_STUDIO_BASE_URL}")
        return False

# --- Configuração do Chatbot ---
def configurar_chatbot():
    """
    Configura e retorna a cadeia LangChain para o chatbot.
    """
    print("\n--- Configurando Chatbot ---")
    try:
        # Inicializa o modelo OpenAI compatível com LM Studio
        llm = OpenAI(
            base_url=LM_STUDIO_BASE_URL,
            api_key="lm-studio", # Chave API fictícia, necessária para a classe OpenAI
            temperature=0.7,   # Ajuste a temperatura conforme desejar (0.0 a 1.0)
                               # 0.7 geralmente é um bom ponto de partida para criatividade
            # max_tokens=256   # Opcional: limite o tamanho da resposta do LLM
        )

        # Template do prompt para dar contexto ao LLM
        prompt_template = PromptTemplate(
            input_variables=["input"],
            template="Você é um chatbot útil e amigável, capaz de conversar sobre diversos tópicos.\n\nPergunta: {input}\nResposta:"
        )

        # Cria a cadeia LangChain
        # RunnablePassthrough permite que a entrada seja passada diretamente para o próximo passo
        # StrOutputParser converte a saída do LLM em uma string simples
        chain = {"input": RunnablePassthrough()} | prompt_template | llm | StrOutputParser()

        print("Chatbot configurado com sucesso!")
        return chain

    except Exception as e:
        print(f"Erro ao configurar o chatbot: {e}")
        print("Verifique se o LM Studio está rodando e o modelo está sendo servido.")
        return None

# --- Loop Principal do Chatbot ---
def iniciar_chatbot():
    """
    Inicia o loop de conversação do chatbot.
    """
    if not testar_conexao_llm():
        print("\nNão foi possível iniciar o chatbot devido a problemas de conexão com o LLM.")
        return

    chatbot_chain = configurar_chatbot()
    if not chatbot_chain:
        return

    print("\n--- Chatbot Iniciado! ---")
    print("Digite sua mensagem e pressione Enter. Digite 'sair' para encerrar.")

    while True:
        user_input = input("\nVocê: ")
        if user_input.lower() == 'sair':
            print("Encerrando o chatbot. Até mais!")
            break
        elif not user_input.strip():
            continue

        try:
            # Invoca a cadeia LangChain com a entrada do usuário
            response = chatbot_chain.invoke({"input": user_input})
            print(f"Bot: {response.strip()}")
        except Exception as e:
            print(f"Erro ao processar a requisição: {e}")
            print("Verifique se o servidor LM Studio ainda está ativo.")

if __name__ == "__main__":
    iniciar_chatbot()