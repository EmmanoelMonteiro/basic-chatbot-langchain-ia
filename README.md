# basic-chatbot-langchain-ia
Chatbot com LLM Local (LM Studio, LangChain, Python)

## 📝 Descrição do Projeto
Este projeto apresenta um chatbot simples construído em Python utilizando a biblioteca LangChain para orquestração da conversa. A particularidade e grande vantagem deste chatbot é que ele se comunica com um Large Language Model (LLM) que roda localmente na sua máquina, sem a necessidade de uma conexão com a internet para inferência (após o download inicial do modelo).

A mágica de rodar o LLM localmente é possível graças ao LM Studio, uma ferramenta intuitiva que permite baixar e servir modelos de linguagem de código aberto (como o Gemma-2-2B-IT, que estamos utilizando aqui) diretamente no seu computador, emulando uma API compatível com a OpenAI.

O objetivo principal deste projeto é demonstrar a capacidade de:
* Configurar um ambiente de desenvolvimento para IA localmente.
* Integrar ferramentas como LM Studio e LangChain.
* Construir uma aplicação de chatbot interativa via terminal.
* Explorar o poder dos LLMs que podem ser executados em hardware comum.

## ✨ Funcionalidades
* Interação de chatbot via terminal.
* Utilização de um LLM rodando localmente (**Gemma-2-2B-IT**, configurado via LM Studio).
* Configuração de ambiente virtual Python para isolamento de dependências.
* Função de teste para verificar a comunicação com o servidor LLM do LM Studio.

## 🛠️ Tecnologias Utilizadas
* **Python 3.9+**
* **LM Studio:** Ferramenta para baixar e rodar LLMs localmente.
* **LangChain:** Framework para desenvolvimento de aplicações com LLMs.
* **langchain-openai:** Integração do LangChain com APIs compatíveis com OpenAI (usada para se conectar ao LM Studio).
* **python-dotenv:** Para gerenciar variáveis de ambiente (URL do servidor LLM).

## 🚀 Configuração do Ambiente e Execução
Siga os passos abaixo para colocar o chatbot para rodar na sua máquina Windows 11.

### 1. Instalação do LM Studio
1. Acesse o site oficial do LM Studio: https://lmstudio.ai/
2. Baixe e instale a versão para Windows.

### 2. Download e Configuração do Modelo no LM Studio
Após instalar o LM Studio:

1. Abra o **LM Studio.**
2. Na barra lateral esquerda, clique na aba **"Search"** (ícone de lupa).
3. No campo de busca, digite `gemma-2-2b-it` e pressione Enter.
4. Procure por uma versão **GGUF** do modelo (ex: `gemma-2-2b-it-q4_k_m.gguf`). Modelos com `Q4_K_M` ou `Q5_K_M` oferecem um bom equilíbrio entre desempenho e consumo de RAM.
5. Clique no botão **"Download"** ao lado da versão escolhida. Aguarde o download ser concluído (pode levar um tempo dependendo da sua conexão).

### 3. Iniciando o Servidor Local do LLM no LM Studio
Com o modelo baixado:

1. No LM Studio, vá para a aba **"Local Inference Server"** (ícone de duas setas, uma para cima e uma para baixo).
2. No painel esquerdo, certifique-se de que o modelo `gemma-2-2b-it` está selecionado no dropdown.
3. Verifique se a **porta padrão** (1234) está configurada. Anote a porta se for diferente.
4. Clique no botão **"Start Server"**.
* Você verá uma mensagem como "Serving on `http://localhost:1234"` se o servidor iniciar corretamente.
* **Deixe o LM Studio rodando em segundo plano** enquanto você configura o Python.

### 4. Configuração do Ambiente Python
1. Clone este repositório para a sua máquina:
```Bash
git clone https://github.com/SeuUsuario/NomeDoSeuRepositorio.git
cd NomeDoSeuRepositorio
```
(Substitua `SeuUsuario/NomeDoSeuRepositorio.git` pelo caminho real do seu repositório).

2. Crie um ambiente virtual (no diretório raiz do projeto):
```Bash
python -m venv .venv
```

3. Ative o ambiente virtual (no Windows):
```Bash
.venv\Scripts\activate
```
Você verá `(.venv)` no início da linha de comando, indicando que o ambiente está ativado.

5. Criação do arquivo `requirements.txt`
Crie um arquivo chamado `requirements.txt` na raiz do seu projeto com o seguinte conteúdo:

```
langchain
langchain-community
langchain-openai
python-dotenv
```

### 6. Instalação das Dependências Python
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```Bash
pip install -r requirements.txt
```

### 7. Criação do arquivo `.env`
1. Crie um arquivo chamado `.env` na raiz do seu projeto (no mesmo nível do `main.py`).
2. Adicione a seguinte linha ao arquivo `.env`, **ajustando a porta se for diferente da padrão** `1234`:
```
LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

### 8. Execução do Chatbot
Com o LM Studio servindo o modelo e o ambiente Python configurado:

1. No seu terminal, certifique-se de que você está na pasta raiz do projeto e que o ambiente virtual está ativado.
2. Execute o script principal:
```
python main.py
```

**Interação**
* O chatbot primeiro tentará conectar-se ao LLM. Se a conexão for bem-sucedida, ele iniciará o loop de conversa.
* Digite suas perguntas e pressione Enter.
* Para sair, digite sair e pressione Enter.

## 📁 Estrutura do Projeto
```shell
.
├── .env                  # Variáveis de ambiente (URL do servidor LLM)
├── main.py               # Script principal do chatbot
├── requirements.txt      # Lista de dependências Python
└── README.md             # Este arquivo
```
