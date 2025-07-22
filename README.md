# 🔍 Busca Wikipedia com IA via MCP

Este projeto implementa um sistema de busca na Wikipedia integrado com Inteligência Artificial usando o protocolo **Model Context Protocol (MCP)**. O sistema permite buscar informações na Wikipedia e gerar resumos inteligentes usando a API da OpenAI.

## 🎯 Objetivo do Projeto

O projeto demonstra como implementar uma arquitetura **MCP (Model Context Protocol)** para criar um sistema distribuído que:

- **Busca informações** na Wikipedia de forma inteligente
- **Processa dados** usando serviços de IA (OpenAI GPT)
- **Apresenta resultados** em uma interface web moderna
- **Modulariza responsabilidades** entre servidor e cliente
- **Facilita extensibilidade** para adicionar novas fontes de dados

### O que é MCP?

O Model Context Protocol é um padrão para comunicação entre sistemas de IA e fontes de dados externas, permitindo que modelos de linguagem acessem informações em tempo real de forma estruturada e segura.

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐    Wikipedia API    ┌─────────────────┐
│                 │  ───────────►   │                 │  ─────────────────► │                 │
│   Interface     │                 │   Servidor MCP  │                     │    Wikipedia    │
│   Streamlit     │  ◄───────────   │   (Flask)       │  ◄───────────────── │                 │
│                 │                 │                 │                     └─────────────────┘
└─────────────────┘                 └─────────────────┘
         │                                   │
         │                                   │
         ▼                                   ▼
┌─────────────────┐    OpenAI API    ┌─────────────────┐
│                 │  ───────────────► │                 │
│   Cliente MCP   │                  │     OpenAI      │
│   (aiohttp)     │  ◄─────────────── │     GPT-3.5     │
│                 │                  │                 │
└─────────────────┘                  └─────────────────┘
```

### Fluxo de Dados:

1. **Usuário** insere termo de busca na interface Streamlit
2. **Interface** chama o Cliente MCP
3. **Cliente MCP** faz requisição HTTP para o Servidor MCP
4. **Servidor MCP** busca informações na Wikipedia
5. **Cliente MCP** recebe dados e os envia para OpenAI para processamento
6. **OpenAI** gera resumo inteligente
7. **Interface** exibe resultado formatado para o usuário

## 📁 Estrutura do Projeto

```
mcp_app/
├── .env                    # Variáveis de ambiente (chave OpenAI)
├── requirements.txt        # Dependências Python
├── servidor_debug.py       # Servidor MCP (Flask)
├── cliente_debug.py        # Cliente MCP (aiohttp + OpenAI)
├── interface.py           # Interface web (Streamlit)
├── teste_env.py           # Script de teste das variáveis
├── teste_wikipedia.py     # Script de teste da Wikipedia
└── README.md              # Este arquivo
```

### Descrição dos Arquivos:

- **`servidor_debug.py`**: Servidor Flask que implementa o protocolo MCP, responsável por buscar dados na Wikipedia
- **`cliente_debug.py`**: Cliente que consome o servidor MCP e integra com OpenAI para processamento de IA
- **`interface.py`**: Interface web construída com Streamlit para interação do usuário
- **`.env`**: Arquivo de configuração com credenciais (chave OpenAI)
- **`requirements.txt`**: Lista de dependências Python necessárias

## 🚀 Configuração e Instalação

### 1. Pré-requisitos

- Python 3.9+
- Chave da API OpenAI
- Conexão com internet

### 2. Criação da Máquina Virtual

```bash
# Navegar para o diretório do projeto
cd /home/seu_usuario/

# Criar diretório do projeto
mkdir mcp_app
cd mcp_app

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalação das Dependências

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 4. Configuração do Arquivo `.env`

Crie o arquivo `.env` na raiz do projeto:

```bash
# Criar arquivo .env
touch .env
```

Adicione sua chave OpenAI:

```env
OPENAI_API_KEY=sk-proj-sua_chave_openai_aqui
```

**Como obter chave OpenAI:**
1. Acesse https://platform.openai.com/api-keys
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave e adicione no arquivo `.env`

### 5. Arquivo `requirements.txt`

```txt
flask
openai
wikipedia
python-dotenv
streamlit
aiohttp
```

## 🎮 Como Executar

### 1. Ativar Ambiente Virtual

```bash
source venv/bin/activate
```

### 2. Executar o Servidor MCP

```bash
# Terminal 1
python servidor_debug.py
```

Saída esperada:
```
🚀 Iniciando servidor Flask...
📍 URL: http://localhost:8000
🏠 Home: GET /
💚 Health: GET /health
🔍 Wikipedia: POST /tools/buscar_wikipedia
==================================================
```

### 3. Executar a Interface Streamlit

```bash
# Terminal 2
streamlit run interface.py
```

Saída esperada:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 4. Acessar a Aplicação

Abra o navegador e acesse: `http://localhost:8501`

## 🧪 Testes

### Teste das Variáveis de Ambiente

```bash
python teste_env.py
```

### Teste da Busca Wikipedia

```bash
python teste_wikipedia.py
```

### Teste do Cliente MCP

```bash
python cliente_debug.py
```

## 💡 Como Usar

1. **Acesse a interface** no navegador (`http://localhost:8501`)
2. **Digite um termo** de busca (ex: "Python", "Maradona", "Brasil")
3. **Clique em "Buscar"**
4. **Aguarde o processamento** (busca + IA)
5. **Visualize o resultado** formatado

### Exemplos de Busca:

- ✅ "Python" - linguagem de programação
- ✅ "Maradona" - jogador de futebol
- ✅ "Inteligência Artificial" - conceito tecnológico
- ✅ "Brasil" - país
- ✅ "Energia Solar" - tecnologia

## 🔧 Funcionalidades

### 🌐 Servidor MCP (Flask)
- API REST para busca na Wikipedia
- Tratamento de ambiguidades e erros
- Busca inteligente com fallback
- Logs detalhados para debug
- Suporte a múltiplas tentativas de busca

### 🤖 Cliente MCP (aiohttp + OpenAI)
- Comunicação assíncrona com servidor
- Integração com OpenAI GPT-3.5
- Processamento inteligente de respostas
- Tratamento robusto de erros
- Cache e otimização de requisições

### 🎨 Interface Web (Streamlit)
- Interface moderna e responsiva
- Feedback visual em tempo real
- Tratamento de erros amigável
- Debug info opcional
- Formatação markdown dos resultados

## 🛠️ Personalização

### Adicionar Novas Fontes de Dados

1. **No servidor** (`servidor_debug.py`):
```python
@app.route('/tools/buscar_fonte_nova', methods=['POST'])
def buscar_fonte_nova():
    # Implementar nova fonte
    pass
```

2. **No cliente** (`cliente_debug.py`):
```python
resultado = await cliente.chamar_ferramenta("buscar_fonte_nova", {"termo": busca})
```

### Modificar Prompts da IA

No arquivo `cliente_debug.py`, edite a seção:
```python
messages=[
    {
        "role": "system",
        "content": "Seu prompt personalizado aqui"
    },
    # ...
]
```

### Alterar Modelo da OpenAI

```python
response = client.chat.completions.create(
    model="gpt-4",  # ou "gpt-3.5-turbo"
    # ...
)
```

## 🐛 Solução de Problemas

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### Erro: "OpenAI API key not found"
- Verifique o arquivo `.env`
- Execute: `python teste_env.py`

### Erro: "Connection refused"
- Verifique se o servidor está rodando
- Teste: `curl http://localhost:8000/health`


## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request


