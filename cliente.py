import asyncio
import json
from typing import Any, Dict
import aiohttp
import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis de ambiente
load_dotenv()

class ClienteMCP:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def chamar_ferramenta(self, nome_ferramenta: str, argumentos: Dict[str, Any]) -> str:
        """Chama uma ferramenta no servidor MCP"""
        if not self.session:
            raise RuntimeError("Cliente não inicializado. Use async with.")
        
        url = f"{self.base_url}/tools/{nome_ferramenta}"
        
        try:
            async with self.session.post(url, json=argumentos) as response:
                if response.status == 200:
                    resultado = await response.json()
                    return resultado.get('content', '')
                else:
                    return f"Erro na requisição: {response.status}"
        except Exception as e:
            return f"Erro ao conectar com o servidor: {str(e)}"

# Instância global do cliente
cliente_mcp = ClienteMCP()

async def testar_servidor(cliente: ClienteMCP, busca: str) -> str:
    """Testa o servidor buscando informações e gerando resposta com IA"""
    
    async with cliente:
        # Busca informações na Wikipedia via servidor MCP
        resultado_busca = await cliente.chamar_ferramenta(
            "buscar_wikipedia", 
            {"busca": busca}
        )
        
        # Se houve erro na busca, retorna o erro
        if resultado_busca.startswith("Erro"):
            return resultado_busca
        
        # Usa OpenAI para gerar uma resposta mais elaborada
        try:
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
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
            # Se falhar com OpenAI, retorna apenas o resultado da Wikipedia
            return f"**Informações da Wikipedia:**\n\n{resultado_busca}\n\n*Nota: Não foi possível gerar resumo com IA: {str(e)}*"

if __name__ == "__main__":
    # Teste básico
    async def teste():
        resultado = await testar_servidor(cliente_mcp, "Python programming")
        print(resultado)
    
    asyncio.run(teste())