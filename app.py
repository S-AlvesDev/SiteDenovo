from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
import os

app = Flask(__name__, template_folder='.', static_folder='.')  # Define '.' como pasta raiz

# Simulação de banco de dados
usuarios = {}

app.secret_key = 'chave_secreta'

@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html', logged_in=True)
    return render_template('index.html', logged_in=False)

@app.route('/mural')
def mural():
    if 'logged_in' in session and session['logged_in']:
        return render_template('mural.html')
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    senha = data.get("senha", "").strip()
    
    if email in usuarios and usuarios[email]["senha"] == senha:
        session['logged_in'] = True
        session['username'] = usuarios[email]["nome"]
        return jsonify({"success": True, "username": usuarios[email]["nome"]})
    
    return jsonify({"success": False, "message": "Usuário ou senha inválidos."})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get("nome", "").strip()
    sobrenome = data.get("sobrenome", "").strip()
    email = data.get("email", "").strip()
    senha = data.get("senha", "").strip()
    
    if not email:
        return jsonify({"success": False, "message": "Email inválido."})
    if email in usuarios:
        return jsonify({"success": False, "message": "Usuário já cadastrado."})
    
    usuarios[email] = {"nome": nome, "sobrenome": sobrenome, "senha": senha}
    return jsonify({"success": True})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))

# Rota para servir arquivos CSS e JS diretamente
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)  # Busca os arquivos no mesmo diretório

if __name__ == '__main__':
    app.run(debug=True)
