import PySimpleGUI as sg
import json
import os
from datetime import datetime

# Configuração do tema
sg.ChangeLookAndFeel('LightGreen3')

# Caminho do arquivo de dados
DATA_FILE = 'score_ambiental_data.json'

# Inicializar dados do usuário
user_data = {
    'nome': '',
    'nivel': 1,
    'pontuacao_total': 0,
    'categorias': {
        'agua': {'pontos': 0, 'meta': 100},
        'energia': {'pontos': 0, 'meta': 100},
        'mobilidade': {'pontos': 0, 'meta': 100},
        'alimentacao': {'pontos': 0, 'meta': 100},
        'residuos': {'pontos': 0, 'meta': 100},
        'bem_estar': {'pontos': 0, 'meta': 100}
    },
    'historico': []
}

def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return user_data

def salvar_dados(dados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def tela_inicial():
    layout = [
        [sg.Text('SCORE AMBIENTAL', font=('Helvetica', 20, 'bold'), justification='center', expand_x=True)],
        [sg.Image('logo.png', size=(200, 200), pad=(150, 20))] if os.path.exists('logo.png') else [sg.Text('Bem-vindo ao Score Ambiental!', font=('Helvetica', 14), pad=(100, 50))],
        [sg.Button('Entrar', size=(15, 2), key='-LOGIN-'), sg.Button('Cadastrar', size=(15, 2), key='-REGISTER-')],
        [sg.Button('Sair', size=(10, 1), button_color=('white', 'red'), pad=(180, 20))]
    ]
    return sg.Window('Score Ambiental - Início', layout, finalize=True, element_justification='center')

def tela_cadastro():
    layout = [
        [sg.Text('Cadastro de Novo Usuário', font=('Helvetica', 16))],
        [sg.Text('Nome:'), sg.Input(key='-NOME-', size=(30, 1))],
        [sg.Text('Email:'), sg.Input(key='-EMAIL-', size=(30, 1))],
        [sg.Text('Senha:'), sg.Input(key='-SENHA-', password_char='*', size=(30, 1))],
        [sg.Text('Confirme a senha:'), sg.Input(key='-CONFIRMA_SENHA-', password_char='*', size=(25, 1))],
        [sg.Button('Cadastrar', key='-CADASTRAR-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]
    return sg.Window('Cadastro', layout, finalize=True, element_justification='center')

def tela_login():
    layout = [
        [sg.Text('Login', font=('Helvetica', 16))],
        [sg.Text('Email:'), sg.Input(key='-LOGIN_EMAIL-', size=(30, 1))],
        [sg.Text('Senha:'), sg.Input(key='-LOGIN_SENHA-', password_char='*', size=(30, 1))],
        [sg.Button('Entrar', key='-ENTRAR-'), sg.Button('Voltar', key='-VOLTAR_LOGIN-')]
    ]
    return sg.Window('Login', layout, finalize=True, element_justification='center')

def tela_principal(usuario):
    # Layout da barra lateral
    sidebar = [
        [sg.Text(f'Olá, {usuario["nome"]}!', font=('Helvetica', 12, 'bold'))],
        [sg.Text(f'Nível: {usuario["nivel"]}')],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESSO-', bar_color=('green', 'white'))],
        [sg.Text('Pontuação Total:')],
        [sg.Text(f'{usuario["pontuacao_total"]} pts', font=('Helvetica', 16, 'bold'))],
        [sg.Button('Registrar Atividade', size=(20, 2), key='-REG_ATIVIDADE-')],
        [sg.Button('Meu Progresso', size=(20, 2), key='-PROGRESSO_BTN-')],
        [sg.Button('Ranking', size=(20, 2), key='-RANKING-')],
        [sg.Button('Sair', size=(10, 1), button_color=('white', 'red'), pad=(20, 20))]
    ]

    # Layout principal
    main_area = [
        [sg.Text('Atividades Recentes', font=('Helvetica', 16))],
        [sg.Table(
            values=[[atv['data'], atv['atividade'], f"+{atv['pontos']} pts"] for atv in usuario['historico'][-5:][::-1]],
            headings=['Data', 'Atividade', 'Pontos'],
            auto_size_columns=True,
            display_row_numbers=False,
            justification='left',
            num_rows=min(5, len(usuario['historico'])),
            key='-TABELA_ATIVIDADES-',
            row_height=30
        )],
        [sg.Text('\nResumo das Categorias', font=('Helvetica', 14))],
        [sg.Frame('', [
            [sg.Text(cat.capitalize(), size=(12, 1)), 
             sg.ProgressBar(100, orientation='h', size=(30, 20), key=f'-PROG_{cat.upper()}-', 
                           bar_color=('green', 'white'))]
            for cat in usuario['categorias'].keys()
        ])]
    ]

    layout = [
        [
            sg.Column(sidebar, vertical_alignment='top', size=(250, 600)),
            sg.VSeparator(),
            sg.Column(main_area, size=(600, 600), scrollable=True, vertical_scroll_only=True)
        ]
    ]

    window = sg.Window('Score Ambiental - Painel', layout, finalize=True, resizable=True, element_justification='center')
    # Atualizar a barra de progresso
    progresso = (usuario['pontuacao_total'] % 1000) / 10  # Progresso para o próximo nível
    window['-PROGRESSO-'].update(progresso)
    
    # Atualizar barras de progresso das categorias
    for cat in usuario['categorias'].keys():
        progresso_cat = (usuario['categorias'][cat]['pontos'] / usuario['categorias'][cat]['meta']) * 100
        window[f'-PROG_{cat.upper()}-'].update(progresso_cat)
    
    return window

def tela_registrar_atividade(usuario):
    categorias = list(usuario['categorias'].keys())
    
    layout = [
        [sg.Text('Registrar Nova Atividade', font=('Helvetica', 16))],
        [sg.Text('Categoria:'), 
         sg.Combo(categorias, default_value=categorias[0], key='-CATEGORIA-', size=(20, 1))],
        [sg.Text('Descrição:'), sg.Input(key='-DESCRICAO-', size=(40, 1))],
        [sg.Text('Pontos:'), sg.Slider(range=(1, 100), default_value=10, orientation='h', key='-PONTOS-', size=(30, 20))],
        [sg.Button('Salvar', key='-SALVAR_ATIVIDADE-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    
    return sg.Window('Registrar Atividade', layout, finalize=True, element_justification='center')

def main():
    # Carregar dados do usuário
    usuario = carregar_dados()
    
    # Iniciar com a tela inicial
    janela_atual = 'inicio'
    janela = tela_inicial()
    janela_atividade = None
    
    while True:
        janela, evento, valores = sg.read_all_windows()
        
        # Fechar a aplicação
        if evento == sg.WIN_CLOSED or evento == 'Sair' or (janela == janela_atividade and evento == '-CANCELAR-'):
            if janela == janela_atividade:
                janela_atividade.close()
                janela_atividade = None
            else:
                break
        
        # Navegação entre telas
        elif evento == '-REGISTER-':
            janela.hide()
            janela_cadastro = tela_cadastro()
            janela_atual = 'cadastro'
            
        elif evento == '-LOGIN-':
            janela.hide()
            janela_login = tela_login()
            janela_atual = 'login'
            
        elif evento == '-VOLTAR-':
            janela.close()
            janela = tela_inicial()
            janela_atual = 'inicio'
            
        elif evento == '-VOLTAR_LOGIN-':
            janela.close()
            janela = tela_inicial()
            janela_atual = 'inicio'
            
        elif evento == '-CADASTRAR-':
            # Validação simples
            if not valores['-NOME-'] or not valores['-EMAIL-'] or not valores['-SENHA-']:
                sg.popup('Por favor, preencha todos os campos!', title='Erro')
                continue
                
            if valores['-SENHA-'] != valores['-CONFIRMA_SENHA-']:
                sg.popup('As senhas não conferem!', title='Erro')
                continue
                
            # Atualizar dados do usuário
            usuario['nome'] = valores['-NOME-']
            usuario['email'] = valores['-EMAIL-']
            
            # Salvar dados
            salvar_dados(usuario)
            
            sg.popup('Cadastro realizado com sucesso!', title='Sucesso')
            janela.close()
            janela = tela_principal(usuario)
            janela_atual = 'principal'
            
        elif evento == '-ENTRAR-':
            # Simulação de login (em um sistema real, verificar credenciais)
            if not valores['-LOGIN_EMAIL-'] or not valores['-LOGIN_SENHA-']:
                sg.popup('Por favor, preencha todos os campos!', title='Erro')
                continue
                
            # Se for o primeiro acesso, usar o cadastro
            if not usuario.get('email'):
                usuario['email'] = valores['-LOGIN_EMAIL-']
                usuario['nome'] = 'Usuário'  # Nome padrão
                salvar_dados(usuario)
            
            janela.close()
            janela = tela_principal(usuario)
            janela_atual = 'principal'
            
        elif evento == '-REG_ATIVIDADE-':
            janela_atividade = tela_registrar_atividade(usuario)
            
        elif evento == '-SALVAR_ATIVIDADE-':
            if not valores['-DESCRICAO-']:
                sg.popup('Por favor, informe uma descrição para a atividade!', title='Erro')
                continue
                
            # Atualizar pontuação
            categoria = valores['-CATEGORIA-']
            pontos = int(valores['-PONTOS-'])
            
            usuario['categorias'][categoria]['pontos'] += pontos
            usuario['pontuacao_total'] += pontos
            
            # Verificar se subiu de nível (a cada 1000 pontos)
            novo_nivel = (usuario['pontuacao_total'] // 1000) + 1
            if novo_nivel > usuario['nivel']:
                usuario['nivel'] = novo_nivel
                sg.popup(f'Parabéns! Você subiu para o nível {novo_nivel}!', title='Novo Nível')
            
            # Registrar no histórico
            usuario['historico'].append({
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'atividade': valores['-DESCRICAO-'],
                'categoria': categoria,
                'pontos': pontos
            })
            
            # Salvar dados
            salvar_dados(usuario)
            
            # Atualizar a tela principal
            janela.close()
            janela = tela_principal(usuario)
            janela_atividade.close()
            janela_atividade = None
            
            sg.popup('Atividade registrada com sucesso!', title='Sucesso')
    
    # Fechar janelas ao sair
    if 'janela' in locals():
        janela.close()
    if 'janela_atividade' in locals() and janela_atividade is not None:
        janela_atividade.close()

if __name__ == '__main__':
    main()
