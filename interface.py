import streamlit as st
import asyncio
from cliente import testar_servidor, cliente_mcp

st.set_page_config(page_title="Busca MCP", layout="centered")
st.title("🔍 Busca na Wikipédia com IA via MCP")

busca = st.text_input("Digite o termo a ser buscado:")

if st.button("Buscar"):
    if busca:
        with st.spinner("Buscando e gerando resposta..."):
            resposta = asyncio.run(testar_servidor(cliente=cliente_mcp, busca=busca))
            st.success("Resultado:")
            st.markdown(resposta)
    else:
        st.warning("Por favor, digite um termo.")
