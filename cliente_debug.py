import asyncio
import json
from typing import Any, Dict
import aiohttp
import os
from dotenv import load_dotenv
from openai import OpenAI

import asyncio
import json
from typing import Any, Dict
import aiohttp
import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis de ambiente de forma mais robusta
def carregar_env():
    # Tenta carregar do diretório atual
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("✅ Arquivo .env carregado do diretório atual")
    elif os.path.exists('/home/paribe/mcp_app/.env'):
        load_dotenv('/home/paribe/mcp_app/.env')
        print("✅ Arquivo .env carregado do caminho completo")
    else:
        print("⚠️ Arquivo .env não encontrado")
    
    # Verifica se a chave foi carregada
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"🔑 Chave OpenAI carregada: {api_key[:10]}...")
    else:
        print("❌ Chave OpenAI não encontrada nas variáveis de ambiente")
    
    return api_key

# Carrega as variáveis de ambiente
API_KEY = carregar_env()

class ClienteMCP:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        print(f"🌐 Cliente inicializado com URL: {self.base_url}")
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        print("🔗 Sessão aiohttp criada")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            print("🔌 Sessão aiohttp fechada")
    
    async def chamar_ferramenta(self, nome_ferramenta: str, argumentos: Dict[str, Any]) -> str:
        """Chama uma ferramenta no servidor MCP"""
        if not self.session:
            raise RuntimeError("Cliente não inicializado. Use async with.")
        
        url = f"{self.base_url}/tools/{nome_ferramenta}"
        print(f"📡 Fazendo requisição para: {url}")
        print(f"📦 Com dados: {argumentos}")
        
        try:
            headers = {'Content-Type': 'application/json'}
            async with self.session.post(url, json=argumentos, headers=headers) as response:
                print(f"📊 Status da resposta: {response.status}")
                
                if response.status == 200:
                    resultado = await response.json()
                    print(f"✅ Resposta recebida: {str(resultado)[:100]}...")
                    return resultado.get('content', '')
                else:
                    texto_resposta = await response.text()
                    print(f"❌ Erro na resposta: {texto_resposta}")
                    return f"Erro na requisição: {response.status} - {texto_resposta}"
        except Exception as e:
            print(f"❌ Erro na conexão: {str(e)}")
            return f"Erro ao conectar com o servidor: {str(e)}"

# Instância global do cliente
cliente_mcp = ClienteMCP()

async def testar_servidor(cliente: ClienteMCP, busca: str) -> str:
    """Testa o servidor buscando informações e gerando resposta com IA"""
    print(f"🚀 Iniciando teste com busca: {busca}")
    
    async with cliente:
        # Busca informações na Wikipedia via servidor MCP
        resultado_busca = await cliente.chamar_ferramenta(
            "buscar_wikipedia", 
            {"busca": busca}
        )
        
        print(f"📋 Resultado da busca: {resultado_busca[:100]}...")
        
        # Se houve erro na busca, retorna o erro
        if resultado_busca.startswith("Erro"):
            return resultado_busca
        
        # Usa OpenAI para gerar uma resposta mais elaborada
        try:
            # Usa a chave carregada globalmente
            if not API_KEY:
                print("⚠️ Chave OpenAI não disponível, retornando só Wikipedia")
                return f"**Informações da Wikipedia:**\n\n{resultado_busca}"
            
            print("🤖 Gerando resposta com OpenAI...")
            client = OpenAI(api_key=API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente útil que explica conceitos de forma clara e didática em português."
                    },
                    {
                        "role": "user",
                        "content": f"Com base nas informações da Wikipedia abaixo sobre '{busca}', forneça um resumo claro e informativo:\n\n{resultado_busca}"
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️ Erro com OpenAI: {str(e)}")
            # Se falhar com OpenAI, retorna apenas o resultado da Wikipedia
            return f"**Informações da Wikipedia:**\n\n{resultado_busca}\n\n*Nota: Não foi possível gerar resumo com IA: {str(e)}*"

if __name__ == "__main__":
    # Teste básico
    async def teste():
        resultado = await testar_servidor(cliente_mcp, "Python")
        print("🎯 RESULTADO FINAL:")
        print(resultado)
    
    asyncio.run(teste())