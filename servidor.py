from flask import Flask, request, jsonify
import wikipedia

app = Flask(__name__)

@app.route('/tools/buscar_wikipedia', methods=['POST'])
def buscar_wikipedia():
    try:
        data = request.get_json()
        busca = data.get('busca', '')
        
        if not busca:
            return jsonify({'error': 'Parâmetro busca é obrigatório'}), 400
        
        # Configura Wikipedia para português
        wikipedia.set_lang("pt")
        
        try:
            resultado = wikipedia.summary(busca, sentences=3)
            return jsonify({'content': resultado})
        except wikipedia.exceptions.DisambiguationError as e:
            # Se há ambiguidade, pega a primeira opção
            resultado = wikipedia.summary(e.options[0], sentences=3)
            return jsonify({'content': resultado})
        except wikipedia.exceptions.PageError:
            return jsonify({'content': f'Não foi encontrada informação sobre "{busca}" na Wikipedia.'})
        except Exception as e:
            return jsonify({'content': f'Erro ao buscar: {str(e)}'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    print("Servidor MCP iniciado em http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)