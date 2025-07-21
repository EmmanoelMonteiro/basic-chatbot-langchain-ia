import os
import sys
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
def testar_conexao_llm(llm=None):
    """
    Tenta se comunicar com o LLM rodando no LM Studio para verificar a conexão.
    """
    print("\n--- Testando conexão com o LLM no LM Studio ---")
    try:
        # Se não receber um LLM externo, cria um padrão
        if llm is None:
            if not LM_STUDIO_BASE_URL:
                print("Erro: Variável LM_STUDIO_BASE_URL não configurada")
                return False
                
            llm = criar_llm_padrao(temperature=0.01)
        
        response = llm.invoke("Qual é o seu nome?")
        print(f"Resposta do LLM (teste): {response.strip()}")
        print("Conexão com o LM Studio bem-sucedida! O LLM respondeu.")
        return True
    
    except Exception as e:
        print(f"Erro ao conectar ou interagir com o LLM: {e}")
        return False

# --- Função para criar LLM ---
def criar_llm_padrao(temperature=0.7):
    """Cria uma instância padrão do LLM para uso normal"""
    return OpenAI(
        base_url=LM_STUDIO_BASE_URL,
        api_key="lm-studio",
        temperature=temperature,
    )

# --- Configuração do Chatbot ---
def configurar_chatbot(llm=None):
    """
    Configura e retorna a cadeia LangChain para o chatbot.
    """
    print("\n--- Configurando Chatbot ---")
    try:
        # Usa LLM fornecido ou cria um padrão
        if llm is None:
            llm = criar_llm_padrao(temperature=0.7)

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
def iniciar_chatbot(llm=None):
    """
    Inicia o loop de conversação do chatbot.
    """
    # Teste de conexão com LLM opcional
    if not testar_conexao_llm(llm):
        print("\nNão foi possível iniciar o chatbot devido a problemas de conexão com o LLM.")
        return

    # Passa o LLM para a configuração
    chatbot_chain = configurar_chatbot(llm)
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

def executar_teste_ci():
    """Executa testes básicos para validar a pipeline de CI"""
    print("\n--- Executando Testes de CI ---")
    
    # Mock do LLM para testes
    class MockLLM:
        def invoke(self, prompt):
            return "Mock Response: " + prompt
    
    # Teste de conexão
    print("Testando conexão com mock LLM...")
    if testar_conexao_llm(MockLLM()):
        print("✅ Teste de conexão bem-sucedido")
    else:
        print("❌ Falha no teste de conexão")
        return False
    
    # Teste de configuração do chatbot
    print("Testando configuração do chatbot...")
    try:
        configurar_chatbot(MockLLM())
        print("✅ Chatbot configurado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro na configuração do chatbot: {e}")
        return False
    
if __name__ == "__main__":
    # Modo especial para CI
    if "--ci-test" in sys.argv:
        if executar_teste_ci():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        iniciar_chatbot()