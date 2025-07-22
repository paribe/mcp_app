from flask import Flask, request, jsonify
import wikipedia

app = Flask(__name__)

# Logs para debug
@app.before_request
def log_request_info():
    print(f"🔍 REQUEST: {request.method} {request.url}")
    print(f"📝 Headers: {dict(request.headers)}")
    if request.is_json:
        print(f"📦 JSON Data: {request.get_json()}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'Servidor funcionando!',
        'message': 'Flask server is running',
        'port': 8000
    })

@app.route('/tools/buscar_wikipedia', methods=['POST'])
def buscar_wikipedia():
    print("🎯 Endpoint buscar_wikipedia chamado!")
    
    try:
        # Verificar se é JSON
        if not request.is_json:
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400
        
        data = request.get_json()
        print(f"📊 Dados recebidos: {data}")
        
        busca = data.get('busca', '')
        if not busca:
            return jsonify({'error': 'Parâmetro busca é obrigatório'}), 400
        
        print(f"🔎 Buscando: {busca}")
        
        # Configura Wikipedia para português
        wikipedia.set_lang("pt")
        
        try:
            resultado = wikipedia.summary(busca, sentences=2)
            print(f"✅ Resultado: {resultado[:100]}...")
            return jsonify({'content': resultado})
        except wikipedia.exceptions.DisambiguationError as e:
            resultado = wikipedia.summary(e.options[0], sentences=2)
            return jsonify({'content': resultado})
        except wikipedia.exceptions.PageError:
            return jsonify({'content': f'Página não encontrada para "{busca}"'})
        except Exception as wiki_error:
            print(f"❌ Erro Wikipedia: {wiki_error}")
            return jsonify({'content': f'Erro na Wikipedia: {str(wiki_error)}'})
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    print("🚀 Iniciando servidor Flask...")
    print("📍 URL: http://localhost:8000")
    print("🏠 Home: GET /")
    print("💚 Health: GET /health") 
    print("🔍 Wikipedia: POST /tools/buscar_wikipedia")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0', 
        port=8000, 
        debug=True,
        use_reloader=False  # Evita problemas de reload
    )