import streamlit as st
import wikipedia
import os
from openai import OpenAI
import asyncio
import aiohttp

# Configuração da página
st.set_page_config(
    page_title="🔍 Busca Wikipedia + IA",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1e88e5;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .search-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
    }
    .error-container {
        background: #ffebee;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #f44336;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🔍 Busca Wikipedia com IA</h1>', unsafe_allow_html=True)

# Descrição
st.markdown("""
<div style="text-align: center; color: #666; margin-bottom: 2rem;">
    <p>🤖 Busque qualquer tema na Wikipedia e receba um resumo inteligente gerado por IA</p>
</div>
""", unsafe_allow_html=True)

def buscar_wikipedia(termo):
    """Busca inteligente na Wikipedia"""
    wikipedia.set_lang("pt")
    
    try:
        # Tentativa 1: busca direta
        resultado = wikipedia.summary(termo, sentences=4)
        return f"**{termo}**\n\n{resultado}"
        
    except wikipedia.exceptions.DisambiguationError as e:
        # Se há ambiguidade, pega a primeira opção
        primeiro_termo = e.options[0]
        resultado = wikipedia.summary(primeiro_termo, sentences=4)
        return f"**{primeiro_termo}** (termo relacionado)\n\n{resultado}"
        
    except wikipedia.exceptions.PageError:
        # Busca mais ampla
        try:
            resultados_busca = wikipedia.search(termo, results=3)
            if resultados_busca:
                primeiro_resultado = resultados_busca[0]
                resultado = wikipedia.summary(primeiro_resultado, sentences=4)
                return f"**{primeiro_resultado}** (encontrado via busca)\n\n{resultado}"
            else:
                return f"❌ Nenhum resultado encontrado para '{termo}' na Wikipedia em português."
        except Exception as e:
            return f"❌ Erro ao buscar '{termo}': {str(e)}"
            
    except Exception as e:
        return f"❌ Erro geral: {str(e)}"

def gerar_resumo_ia(texto_wikipedia, termo_busca):
    """Gera resumo usando OpenAI"""
    try:
        # Tenta pegar a chave de diferentes fontes
        openai_key = None
        
        # 1. Primeiro tenta os secrets do Streamlit Cloud
        try:
            openai_key = st.secrets["OPENAI_API_KEY"]
        except:
            pass
        
        # 2. Se não encontrar, tenta variável de ambiente local
        if not openai_key:
            openai_key = os.getenv("OPENAI_API_KEY")
        
        # 3. Se ainda não encontrar, tenta carregar do .env local
        if not openai_key:
            from dotenv import load_dotenv
            load_dotenv()
            openai_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_key:
            return f"⚠️ **Informações da Wikipedia:**\n\n{texto_wikipedia}\n\n*Nota: Configure OPENAI_API_KEY para resumo com IA*"
        
        client = OpenAI(api_key=openai_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Você é um especialista em criar resumos educativos e informativos. 
                    Sua tarefa é explicar conceitos de forma clara, didática e interessante em português.
                    Mantenha o tom profissional mas acessível."""
                },
                {
                    "role": "user",
                    "content": f"""Com base nas informações da Wikipedia sobre '{termo_busca}', 
                    crie um resumo claro e informativo que:
                    - Explique o conceito principal
                    - Destaque pontos mais interessantes
                    - Use linguagem acessível
                    - Tenha entre 150-300 palavras
                    
                    Informações da Wikipedia:
                    {texto_wikipedia}"""
                }
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        return f"🤖 **Resumo Inteligente:**\n\n{response.choices[0].message.content}"
        
    except Exception as e:
        return f"**Informações da Wikipedia:**\n\n{texto_wikipedia}\n\n*Erro na IA: {str(e)}*"

# Interface principal
with st.container():
    # Campo de busca
    termo_busca = st.text_input(
        "🔎 Digite o que você quer pesquisar:",
        placeholder="Ex: Inteligência Artificial, Maradona, Python...",
        help="Digite qualquer tema e descubra informações interessantes!"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        buscar_btn = st.button("🚀 Buscar", type="primary", use_container_width=True)

# Processamento da busca
if buscar_btn and termo_busca:
    with st.spinner("🔍 Buscando na Wikipedia..."):
        # Busca na Wikipedia
        resultado_wikipedia = buscar_wikipedia(termo_busca)
    
    if "❌" not in resultado_wikipedia:
        with st.spinner("🤖 Gerando resumo inteligente..."):
            # Gera resumo com IA
            resultado_final = gerar_resumo_ia(resultado_wikipedia, termo_busca)
        
        # Mostra resultado
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.success("✅ Resultado encontrado!")
        st.markdown(resultado_final)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Informações adicionais
        with st.expander("📚 Ver informações completas da Wikipedia"):
            st.markdown(resultado_wikipedia)
            
    else:
        # Erro na busca
        st.markdown('<div class="error-container">', unsafe_allow_html=True)
        st.error("❌ Problema na busca")
        st.markdown(resultado_wikipedia)
        st.markdown('</div>', unsafe_allow_html=True)

elif buscar_btn:
    st.warning("⚠️ Por favor, digite um termo para buscar!")

# Sidebar com informações
with st.sidebar:
    st.markdown("### 🛠️ Como funciona")
    st.markdown("""
    1. **Digite** um tema de interesse
    2. **Sistema busca** na Wikipedia
    3. **IA processa** e gera resumo
    4. **Resultado** inteligente e formatado
    """)
    
    st.markdown("### 🎯 Exemplos")
    if st.button("🐍 Python"):
        st.experimental_set_query_params(termo="Python")
    if st.button("🏆 Maradona"):
        st.experimental_set_query_params(termo="Maradona")
    if st.button("🤖 IA"):
        st.experimental_set_query_params(termo="Inteligência Artificial")
    
    st.markdown("---")
    st.markdown("### 💡 Sobre")
    st.markdown("""
    **Tecnologias:**
    - 🔍 Wikipedia API
    - 🤖 OpenAI GPT-3.5
    - ⚡ Streamlit
    
    **Criado com:** Model Context Protocol (MCP)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    🚀 Aplicação MCP | Busca + IA | Streamlit Cloud
</div>
""", unsafe_allow_html=True)