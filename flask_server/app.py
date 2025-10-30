from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Caminho do arquivo de dados
DATA_FILE = 'data/usuarios.json'

def carregar_usuarios():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def salvar_usuarios(usuarios):
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

# Rota para criar um novo usuário
@app.route('/api/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    usuarios = carregar_usuarios()
    
    # Gera um ID único para o usuário
    user_id = str(uuid.uuid4())
    
    # Cria a estrutura básica do usuário
    usuarios[user_id] = {
        'id': user_id,
        'nome': dados.get('nome', 'Usuário'),
        'email': dados.get('email', ''),
        'senha': dados.get('senha', ''),  # Em produção, use hash de senha!
        'nivel': 1,
        'pontuacao_total': 0,
        'categorias': {
            'Água': {'pontos': 0, 'meta': 100, 'nivel': 1},
            'Energia': {'pontos': 0, 'meta': 100, 'nivel': 1},
            'Mobilidade': {'pontos': 0, 'meta': 100, 'nivel': 1},
            'Alimentação': {'pontos': 0, 'meta': 100, 'nivel': 1},
            'Resíduos': {'pontos': 0, 'meta': 100, 'nivel': 1},
            'Bem-estar': {'pontos': 0, 'meta': 100, 'nivel': 1},
            'Consumo Consciente': {'pontos': 0, 'meta': 100, 'nivel': 1},
            'Educação Ambiental': {'pontos': 0, 'meta': 100, 'nivel': 1},
            'Tecnologia Verde': {'pontos': 0, 'meta': 100, 'nivel': 1}
        },
        'historico': [],
        'termos_aprendidos': {},
        'data_criacao': datetime.now().isoformat()
    }
    
    salvar_usuarios(usuarios)
    return jsonify({'sucesso': True, 'usuario_id': user_id, 'usuario': usuarios[user_id]}), 201

# Rota para autenticar usuário
@app.route('/api/login', methods=['POST'])
def login():
    dados = request.get_json()
    usuarios = carregar_usuarios()
    
    for user_id, usuario in usuarios.items():
        if (usuario.get('email') == dados.get('email') and 
            usuario.get('senha') == dados.get('senha')):  # Em produção, use verificação de hash
            return jsonify({'sucesso': True, 'usuario_id': user_id, 'usuario': usuario})
    
    return jsonify({'sucesso': False, 'erro': 'Credenciais inválidas'}), 401

# Rota para obter dados do usuário
@app.route('/api/usuarios/<user_id>', methods=['GET'])
def obter_usuario(user_id):
    usuarios = carregar_usuarios()
    if user_id in usuarios:
        return jsonify(usuarios[user_id])
    return jsonify({'erro': 'Usuário não encontrado'}), 404

# Rota para atualizar dados do usuário
@app.route('/api/usuarios/<user_id>', methods=['PUT'])
def atualizar_usuario(user_id):
    usuarios = carregar_usuarios()
    if user_id not in usuarios:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    dados = request.get_json()
    
    # Atualiza apenas os campos fornecidos
    for key, value in dados.items():
        if key in ['nome', 'email', 'senha', 'nivel', 'pontuacao_total']:
            usuarios[user_id][key] = value
        elif key == 'categorias':
            for cat_nome, cat_dados in value.items():
                if cat_nome in usuarios[user_id]['categorias']:
                    usuarios[user_id]['categorias'][cat_nome].update(cat_dados)
        elif key == 'historico':
            usuarios[user_id]['historico'] = value
        elif key == 'termos_aprendidos':
            usuarios[user_id]['termos_aprendidos'] = value
    
    salvar_usuarios(usuarios)
    return jsonify(usuarios[user_id])

# Rota para obter o ranking de usuários
@app.route('/api/ranking', methods=['GET'])
def obter_ranking():
    usuarios = carregar_usuarios()
    
    # Cria uma lista de usuários com informações para o ranking
    ranking = []
    for user_id, usuario in usuarios.items():
        ranking.append({
            'id': user_id,
            'nome': usuario['nome'],
            'nivel': usuario['nivel'],
            'pontuacao_total': usuario['pontuacao_total']
        })
    
    # Ordena por pontuação total (decrescente)
    ranking.sort(key=lambda x: x['pontuacao_total'], reverse=True)
    
    # Adiciona a posição no ranking
    for i, user in enumerate(ranking, 1):
        user['posicao'] = i
    
    return jsonify(ranking)

# Rota para adicionar uma nova atividade
@app.route('/api/usuarios/<user_id>/atividades', methods=['POST'])
def adicionar_atividade(user_id):
    usuarios = carregar_usuarios()
    if user_id not in usuarios:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    dados = request.get_json()
    categoria = dados.get('categoria')
    descricao = dados.get('descricao', '')
    pontos = dados.get('pontos', 0)
    
    # Adiciona a atividade ao histórico
    nova_atividade = {
        'id': str(uuid.uuid4()),
        'data': datetime.now().isoformat(),
        'categoria': categoria,
        'descricao': descricao,
        'pontos': pontos
    }
    
    usuarios[user_id]['historico'].append(nova_atividade)
    
    # Atualiza a pontuação da categoria e total
    if categoria in usuarios[user_id]['categorias']:
        usuarios[user_id]['categorias'][categoria]['pontos'] += pontos
        usuarios[user_id]['pontuacao_total'] += pontos
        
        # Verifica se subiu de nível
        cat_info = usuarios[user_id]['categorias'][categoria]
        if cat_info['pontos'] >= cat_info['meta']:
            cat_info['nivel'] += 1
            cat_info['meta'] *= 2  # Dobra a meta para o próximo nível
    
    salvar_usuarios(usuarios)
    return jsonify(nova_atividade), 201

# Rota para obter histórico de atividades de um usuário
@app.route('/api/usuarios/<user_id>/historico', methods=['GET'])
def obter_historico(user_id):
    usuarios = carregar_usuarios()
    if user_id not in usuarios:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify(usuarios[user_id]['historico'])

# Rota para atualizar termos aprendidos
@app.route('/api/usuarios/<user_id>/termos', methods=['POST'])
def atualizar_termos(user_id):
    usuarios = carregar_usuarios()
    if user_id not in usuarios:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    dados = request.get_json()
    categoria = dados.get('categoria')
    termos = dados.get('termos', {})
    
    if 'termos_aprendidos' not in usuarios[user_id]:
        usuarios[user_id]['termos_aprendidos'] = {}
    
    if categoria not in usuarios[user_id]['termos_aprendidos']:
        usuarios[user_id]['termos_aprendidos'][categoria] = {}
    
    # Atualiza os termos aprendidos
    for termo, info in termos.items():
        if termo in usuarios[user_id]['termos_aprendidos'][categoria]:
            # Atualiza contagem e peso se o termo já existe
            usuarios[user_id]['termos_aprendidos'][categoria][termo]['contagem'] += info.get('contagem', 1)
            usuarios[user_id]['termos_aprendidos'][categoria][termo]['peso'] = info.get('peso', 1.0)
        else:
            # Adiciona novo termo
            usuarios[user_id]['termos_aprendidos'][categoria][termo] = {
                'contagem': info.get('contagem', 1),
                'peso': info.get('peso', 1.0)
            }
    
    salvar_usuarios(usuarios)
    return jsonify(usuarios[user_id]['termos_aprendidos'])

if __name__ == '__main__':
    # Cria o diretório de dados se não existir
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, port=5000)
