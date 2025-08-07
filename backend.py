from flask import Flask, request, jsonify
from supabase import create_client
import os

app = Flask(__name__)

# Supabase config
SUPABASE_URL = "https://ohcueiiahpywgvwglmqj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oY3VlaWlhaHB5d2d2d2dsbXFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQxMzkwMDAsImV4cCI6MjA2OTcxNTAwMH0.99XL1ZheV0pTA09TqiAffNBfSURE22zzRS3mRDyjoi0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/verificar', methods=['POST'])
def verificar():
    data = request.get_json()
    chave = data.get('key')

    if not chave:
        return jsonify({'status': 'erro', 'mensagem': 'Chave não fornecida'}), 400

    response = supabase.table("licenses").select("*").eq("key", chave).execute()

    if not response.data:
        return jsonify({'status': 'invalida', 'mensagem': 'Licença não encontrada'}), 403

    licenca = response.data[0]

    if licenca["expirada"]:
        return jsonify({'status': 'expirada', 'mensagem': 'Licença expirada'}), 403

    if licenca["usos"] >= licenca["limite"]:
        return jsonify({'status': 'limite', 'mensagem': 'Licença atingiu o limite de uso'}), 403

    # Atualiza uso
    supabase.table("licenses").update({"usos": licenca["usos"] + 1}).eq("key", chave).execute()

    return jsonify({'status': 'valida', 'mensagem': 'Licença válida'}), 200

# 🔥 Requisito para funcionar na Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
