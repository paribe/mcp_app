import os
from dotenv import load_dotenv

print("🔍 Testando carregamento do .env...")

# Verifica se o arquivo .env existe
if os.path.exists('.env'):
    print("✅ Arquivo .env encontrado")
    
    # Mostra o conteúdo do arquivo (sem a chave completa)
    with open('.env', 'r') as f:
        content = f.read()
        print(f"📄 Conteúdo do .env:")
        print(f"📏 Tamanho do arquivo: {len(content)} caracteres")
        print("📝 Linhas:")
        for i, line in enumerate(content.split('\n'), 1):
            if line.strip():
                if 'OPENAI_API_KEY' in line:
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        key_part = parts[1][:15] + "..." if len(parts[1]) > 15 else parts[1]
                        print(f"   Linha {i}: {parts[0]}={key_part}")
                    else:
                        print(f"   Linha {i}: {line} (FORMATO INCORRETO)")
                else:
                    print(f"   Linha {i}: {line}")
            else:
                print(f"   Linha {i}: (linha vazia)")
else:
    print("❌ Arquivo .env NÃO encontrado")

print("\n" + "="*50)

# Carrega as variáveis
print("🔄 Carregando variáveis com load_dotenv()...")
load_dotenv()

# Testa se carregou
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"✅ Chave carregada: {api_key[:15]}...")
    print(f"🔢 Tamanho da chave: {len(api_key)} caracteres")
    
    # Verifica se a chave parece válida
    if api_key.startswith('sk-'):
        print("✅ Formato da chave parece correto (começa com 'sk-')")
    else:
        print("⚠️ Formato da chave pode estar incorreto (não começa com 'sk-')")
else:
    print("❌ Chave não carregada")

# Lista todas as variáveis de ambiente que contêm OPENAI
print("\n🔍 Variáveis de ambiente relacionadas ao OPENAI:")
openai_vars = {k: v for k, v in os.environ.items() if 'OPENAI' in k.upper()}
if openai_vars:
    for key, value in openai_vars.items():
        print(f"   {key}: {value[:15]}...")
else:
    print("   Nenhuma variável OPENAI encontrada")

print(f"\n📁 Diretório atual: {os.getcwd()}")
print("📋 Arquivos no diretório:")
for file in sorted(os.listdir('.')):
    if not file.startswith('.'):
        print(f"   {file}")
    else:
        print(f"   {file} (arquivo oculto)")