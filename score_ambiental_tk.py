import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Caminho do arquivo de dados
DATA_FILE = 'score_ambiental_data.json'

class ScoreAmbientalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Score Ambiental")
        self.root.geometry("800x600")
        
        # Carregar dados do usuário
        self.carregar_dados()
        
        # Iniciar com a tela inicial
        self.mostrar_tela_inicial()
    
    def carregar_dados(self):
        # Estrutura padrão do usuário
        usuario_padrao = {
            'nome': 'Usuário',
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
            'termos_aprendidos': {}
        }

        # Tenta carregar dados existentes
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    dados_carregados = json.load(f)
                
                # Mescla os dados carregados com a estrutura padrão
                self.usuario = {**usuario_padrao, **dados_carregados}
                
                # Garante que todas as categorias padrão existam
                for cat_nome, cat_dados in usuario_padrao['categorias'].items():
                    if cat_nome not in self.usuario['categorias']:
                        self.usuario['categorias'][cat_nome] = cat_dados
                    
                    # Garante que cada categoria tenha todos os campos necessários
                    for campo, valor in cat_dados.items():
                        if campo not in self.usuario['categorias'][cat_nome]:
                            self.usuario['categorias'][cat_nome][campo] = valor
                
                # Garante que as listas/dicionários vazios sejam inicializados se não existirem
                if 'historico' not in self.usuario or not isinstance(self.usuario['historico'], list):
                    self.usuario['historico'] = []
                    
                if 'termos_aprendidos' not in self.usuario or not isinstance(self.usuario['termos_aprendidos'], dict):
                    self.usuario['termos_aprendidos'] = {}
                
                # Garante que o nível e pontuação total existam
                if 'nivel' not in self.usuario:
                    self.usuario['nivel'] = 1
                if 'pontuacao_total' not in self.usuario:
                    self.usuario['pontuacao_total'] = 0
                
            except (json.JSONDecodeError, KeyError) as e:
                # Se houver erro ao ler o arquivo, usa a estrutura padrão
                print(f"Erro ao carregar arquivo: {e}. Usando dados padrão.")
                self.usuario = usuario_padrao
        else:
            # Se o arquivo não existir, usa a estrutura padrão
            self.usuario = usuario_padrao
            self.salvar_dados()
    
    def salvar_dados(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.usuario, f, ensure_ascii=False, indent=2)
    
    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def mostrar_tela_inicial(self):
        self.limpar_tela()
        
        # Título
        ttk.Label(self.root, text="SCORE AMBIENTAL", font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        # Mensagem de boas-vindas
        ttk.Label(self.root, text=f"Bem-vindo, {self.usuario['nome']}!", font=('Helvetica', 14)).pack(pady=10)
        
        # Pontuação total e nível
        frame_info = ttk.Frame(self.root)
        frame_info.pack(pady=10)
        
        ttk.Label(frame_info, text=f"Nível: {self.usuario['nivel']}", font=('Helvetica', 12)).pack()
        ttk.Label(frame_info, text=f"Pontuação Total: {self.usuario['pontuacao_total']} pts", 
                 font=('Helvetica', 16, 'bold')).pack()
        
        # Botões principais
        botoes = [
            ("Registrar Atividade", self.mostrar_tela_registro),
            ("Meu Progresso", self.mostrar_meu_progresso),
            ("Ranking", self.mostrar_ranking),
            ("Sair", self.root.quit)
        ]
        
        for texto, comando in botoes:
            ttk.Button(self.root, text=texto, command=comando, width=20).pack(pady=5)
        
        # Atividades recentes
        ttk.Label(self.root, text="\nAtividades Recentes", font=('Helvetica', 14, 'bold')).pack()
        
        if self.usuario['historico']:
            frame_atividades = ttk.Frame(self.root)
            frame_atividades.pack(pady=10, padx=20, fill='x')
            
            # Cabeçalho
            ttk.Label(frame_atividades, text="Data", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, padx=5, pady=2)
            ttk.Label(frame_atividades, text="Atividade", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2)
            ttk.Label(frame_atividades, text="Pontos", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, padx=5, pady=2)
            
            # Lista de atividades (as 5 mais recentes)
            for i, atv in enumerate(self.usuario['historico'][-5:][::-1], 1):
                ttk.Label(frame_atividades, text=atv['data']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
                ttk.Label(frame_atividades, text=atv['atividade']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
                ttk.Label(frame_atividades, text=f"+{atv['pontos']} pts").grid(row=i, column=2, padx=5, pady=2, sticky='e')
        else:
            ttk.Label(self.root, text="Nenhuma atividade registrada ainda.").pack()
    
    def calcular_pontuacao_automatica(self, categoria, descricao):
        """
        Calcula a pontuação automaticamente usando uma abordagem mais inteligente:
        - Análise de contexto e semântica
        - Frequência de termos relevantes
        - Relacionamento entre palavras
        - Impacto ambiental estimado
        """
        # Garante que descricao seja uma string e remove espaços em branco
        descricao = str(descricao or '').strip()
        if not descricao:
            return 5  # mínimo
            
        # Converter para minúsculas para comparação sem case sensitive
        descricao_lower = descricao.lower()
        palavras = descricao_lower.split()
        
        # Pontuação base (tamanho da descrição, com limite)
        pontos = min(len(palavras) * 1.5, 25)  # Máximo de 25 pontos por tamanho descrição detalhada
        
        # 2. Análise de contexto por categoria
        contextos = {
            'Água': {
                'termos': {
                    'banho': {'sinonimos': ['banho', 'banhar', 'ducha'], 'peso': 0.8},
                    'torneira': {'sinonimos': ['torneira', 'chuveiro', 'torneira aberta'], 'peso': 0.7},
                    'reutilizar': {'sinonimos': ['reutilizar', 'reaproveitar', 'usar novamente'], 'peso': 1.0},
                    'vazamento': {'sinonimos': ['vazamento', 'vazando', 'vazou'], 'peso': 0.9},
                    'chuva': {'sinonimos': ['água da chuva', 'coletar chuva'], 'peso': 0.8}
                },
                'fator': 1.2
            },
            'Energia': {
                'termos': {
                    'luz': {'sinonimos': ['luz', 'luzes', 'lâmpada'], 'peso': 0.7},
                    'desligar': {'sinonimos': ['desligar', 'desliguei', 'desligado'], 'peso': 0.8},
                    'eletrônico': {'sinonimos': ['eletrônico', 'eletrodoméstico', 'aparelho'], 'peso': 0.7},
                    'solar': {'sinonimos': ['solar', 'painel solar', 'energia solar'], 'peso': 1.2},
                    'eletricidade': {'sinonimos': ['eletricidade', 'energia elétrica'], 'peso': 0.9}
                },
                'fator': 1.3
            },
            # ... (outras categorias com a mesma estrutura)
            'Mobilidade': {
                'termos': {
                    'bicicleta': {'sinonimos': ['bicicleta', 'bike', 'pedalar'], 'peso': 1.1},
                    'caminhar': {'sinonimos': ['caminhar', 'andando', 'a pé'], 'peso': 0.9},
                    'transporte': {'sinonimos': ['ônibus', 'metrô', 'trem', 'transporte público'], 'peso': 0.8},
                    'carona': {'sinonimos': ['carona', 'carona solidária'], 'peso': 0.7},
                    'veículo': {'sinonimos': ['carro', 'moto', 'veículo'], 'peso': -0.5}
                },
                'fator': 1.4
            },
            'Alimentação': {
                'termos': {
                    'orgânico': {'sinonimos': ['orgânico', 'sem agrotóxico'], 'peso': 1.2},
                    'vegetariano': {'sinonimos': ['vegetariano', 'vegetariana'], 'peso': 1.1},
                    'vegano': {'sinonimos': ['vegano', 'vegana'], 'peso': 1.1},
                    'horta': {'sinonimos': ['horta', 'plantar', 'cultivar'], 'peso': 1.0},
                    'desperdício': {'sinonimos': ['desperdício', 'desperdiçar', 'desperdiçando'], 'peso': 0.9}
                },
                'fator': 1.1
            },
            'Resíduos': {
                'termos': {
                    'reciclar': {'sinonimos': ['reciclar', 'reciclagem'], 'peso': 1.2},
                    'compostagem': {'sinonimos': ['compostagem', 'compostar'], 'peso': 1.1},
                    'lixo': {'sinonimos': ['lixo', 'resíduo'], 'peso': 0.8},
                    'reduzir': {'sinonimos': ['reduzir', 'redução'], 'peso': 1.0},
                    'reutilizar': {'sinonimos': ['reutilizar', 'reaproveitar'], 'peso': 1.1}
                },
                'fator': 1.2
            },
            'Bem-estar': {
                'termos': {
                    'meditação': {'sinonimos': ['meditação', 'meditar'], 'peso': 0.9},
                    'yoga': {'sinonimos': ['yoga', 'ioga'], 'peso': 0.9},
                    'exercício': {'sinonimos': ['exercício', 'atividade física'], 'peso': 0.8},
                    'saúde': {'sinonimos': ['saúde', 'saudável'], 'peso': 0.8},
                    'qualidade de vida': {'sinonimos': ['qualidade de vida', 'bem-estar'], 'peso': 1.0}
                },
                'fator': 1.0
            },
            'Consumo Consciente': {
                'termos': {
                    'sustentável': {'sinonimos': ['sustentável', 'sustentabilidade'], 'peso': 1.2},
                    'consciente': {'sinonimos': ['consciente', 'consciência'], 'peso': 1.1},
                    'ecológico': {'sinonimos': ['ecológico', 'ecológica'], 'peso': 1.1},
                    'responsável': {'sinonimos': ['responsável', 'responsabilidade'], 'peso': 1.0},
                    'desperdício zero': {'sinonimos': ['desperdício zero', 'lixo zero'], 'peso': 1.3}
                },
                'fator': 1.1
            },
            'Educação Ambiental': {
                'termos': {
                    'ensinar': {'sinonimos': ['ensinar', 'educar', 'explicar'], 'peso': 1.0},
                    'oficina': {'sinonimos': ['oficina', 'workshop', 'curso'], 'peso': 1.1},
                    'palestra': {'sinonimos': ['palestra', 'apresentação'], 'peso': 1.0},
                    'conscientização': {'sinonimos': ['conscientização', 'conscientizar'], 'peso': 1.2},
                    'projeto': {'sinonimos': ['projeto', 'iniciativa'], 'peso': 1.0}
                },
                'fator': 1.1
            },
            'Tecnologia Verde': {
                'termos': {
                    'energia renovável': {'sinonimos': ['energia renovável', 'fonte limpa'], 'peso': 1.3},
                    'sustentabilidade': {'sinonimos': ['sustentabilidade', 'sustentável'], 'peso': 1.2},
                    'eficiência energética': {'sinonimos': ['eficiência energética', 'economia de energia'], 'peso': 1.2},
                    'inovação sustentável': {'sinonimos': ['inovação sustentável', 'tecnologia limpa'], 'peso': 1.3},
                    'painel solar': {'sinonimos': ['painel solar', 'energia solar'], 'peso': 1.2}
                },
                'fator': 1.2
            }
        }
        
        # Pega o contexto da categoria atual ou um dicionário vazio se não existir
        contexto = contextos.get(categoria, {'termos': {}, 'fator': 1.0})
        
        # 1. Pontuação por termos fixos
        pontos_contexto = 0
        for termo, dados in contexto.get('termos', {}).items():
            for sinonimo in dados['sinonimos']:
                if sinonimo in descricao_lower:
                    pontos_contexto += 10 * dados['peso']

        pontos += pontos_contexto
        
        # 2. Bônus por termos aprendidos dinamicamente
        termos_aprendidos = self.usuario.get('termos_aprendidos', {}).get(categoria, {})
        for termo, info in termos_aprendidos.items():
            if termo in descricao_lower:
                pontos += 10 * info.get('peso', 0.5)  # 10 pontos * peso do termo
        
        # 3. Bônus por números na descrição (ex: tempo de banho, quantidade de itens)
        import re
        if re.search(r'\d+', descricao_lower):
            pontos += 5
            
        # 4. Bônus por descrições mais longas e detalhadas
        if len(palavras) > 20:
            pontos += 10
        elif len(palavras) > 10:
            pontos += 5
            
        # 5. Aplicar fator da categoria
        pontos = int(pontos * contexto.get('fator', 1.0))
        
        # 6. Limites mínimos e máximos
        pontos = max(5, min(pontos, 100))  # Mínimo 5, máximo 100 pontos
        
        return pontos
    
    def aprender_termos_da_descricao(self, categoria, descricao):
        """
        Lê a descrição que o usuário digitou e atualiza o dicionário
        self.usuario['termos_aprendidos'] com novos termos ou reforça termos existentes.
        """
        descricao = (descricao or "").lower()

        # Palavras que não valem a pena aprender (stopwords simples)
        stopwords = {
            'eu','de','da','do','das','dos','a','o','os','as','um','uma','uns','umas',
            'e','pra','para','por','com','sem','no','na','nos','nas','em','que','foi',
            'tava','estava','fiz','fazer','usei','usar','use','usar','uso','hoje','ontem',
            'minha','meu','minhas','meus', 'com', 'sem', 'por', 'para', 'nao', 'sim', 'tambem', 'muito',
            'pouco', 'mais', 'menos', 'muito', 'pouco', 'tanto', 'quanto', 'como', 'assim', 'entao', 'depois'
        }

        # Separa em palavras bem básicas (só letras e números)
        import re
        termos_brutos = re.findall(r'[a-zA-ZÀ-ÿ0-9]+', descricao)

        # Mantém só palavras/expressões úteis
        termos_filtrados = [
            t for t in termos_brutos
            if len(t) > 2 and t not in stopwords
        ]

        if not termos_filtrados:
            return  # nada pra aprender

        # Garante a categoria no dicionário
        if categoria not in self.usuario['termos_aprendidos']:
            self.usuario['termos_aprendidos'][categoria] = {}

        cat_dict = self.usuario['termos_aprendidos'][categoria]

        # Atualiza contagem de cada termo
        for termo in termos_filtrados:
            if termo in cat_dict:
                cat_dict[termo]['vezes_usado'] += 1
            else:
                # Valor inicial
                cat_dict[termo] = {
                    'vezes_usado': 1,
                    'peso': 0.5  # peso inicial neutro
                }

        # Depois de atualizar frequências, recalcula pesos normalizados
        total_uso = sum(item['vezes_usado'] for item in cat_dict.values())

        if total_uso > 0:
            for termo, info in cat_dict.items():
                # Peso proporcional à frequência relativa do termo dentro da categoria
                freq_relativa = info['vezes_usado'] / total_uso
                info['peso'] = round(freq_relativa * 1.2, 3)  # ex: 0.0 ~ 1.2 aprox.

        # Salva imediatamente no arquivo
        self.salvar_dados()

    def mostrar_tela_registro(self):
        self.limpar_tela()
        
        ttk.Label(self.root, text="Registrar Nova Atividade", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        # Formulário
        frame_form = ttk.Frame(self.root)
        frame_form.pack(pady=10, padx=20, fill='x')
        
        # Categoria
        ttk.Label(frame_form, text="Categoria:").grid(row=0, column=0, sticky='w', pady=5)
        categoria_var = tk.StringVar(value=list(self.usuario['categorias'].keys())[0])
        
        def atualizar_sugestao(*args):
            categoria = categoria_var.get()
            descricao = descricao_var.get()
            if descricao:
                pontos = self.calcular_pontuacao_automatica(categoria, descricao)
                pontos_var.set(pontos)
                pontos_scale.set(pontos)
        
        categoria_menu = ttk.Combobox(
            frame_form, 
            textvariable=categoria_var, 
            values=list(self.usuario['categorias'].keys()),
            state='readonly'
        )
        categoria_menu.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        categoria_var.trace('w', atualizar_sugestao)
        
        # Descrição
        ttk.Label(frame_form, text="Descrição da atividade:").grid(row=1, column=0, sticky='w', pady=5)
        descricao_var = tk.StringVar()
        descricao_entry = ttk.Entry(frame_form, textvariable=descricao_var, width=40)
        descricao_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        
        # Pontuação calculada automaticamente
        ttk.Label(frame_form, text="Pontuação:", font=('Helvetica', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        pontos_var = tk.IntVar()
        pontos_label = ttk.Label(frame_form, text="0 pontos", font=('Helvetica', 10, 'bold'), foreground='green')
        pontos_label.grid(row=2, column=1, sticky='w', padx=5)
        
        # Atualizar pontuação quando a descrição ou categoria mudar
        def atualizar_pontuacao(*args):
            if descricao_var.get().strip():
                pontos = self.calcular_pontuacao_automatica(categoria_var.get(), descricao_var.get())
                pontos_var.set(pontos)
                pontos_label.config(text=f"{pontos} pontos")
            else:
                pontos_var.set(0)
                pontos_label.config(text="0 pontos")
        
        descricao_var.trace('w', atualizar_pontuacao)
        categoria_var.trace('w', atualizar_pontuacao)
        
        # Frame para botões
        frame_botoes = ttk.Frame(self.root)
        frame_botoes.pack(pady=20)
        
        def salvar_atividade():
            if not descricao_var.get().strip():
                messagebox.showwarning("Atenção", "Por favor, descreva a atividade.")
                return
                
            categoria = categoria_var.get()
            descricao = descricao_var.get()
            
            # 1. Aprender com a descrição fornecida
            self.aprender_termos_da_descricao(categoria, descricao)
            
            # 2. Calcular pontos automaticamente (já considerando termos aprendidos)
            pontos = self.calcular_pontuacao_automatica(categoria, descricao)
            
            # 3. Registrar a atividade no histórico
            nova_atividade = {
                'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'categoria': categoria,
                'atividade': descricao,
                'pontos': pontos
            }
            
            self.usuario['historico'].append(nova_atividade)
            
            # 4. Atualizar pontuação total e da categoria
            self.usuario['pontuacao_total'] += pontos
            self.usuario['categorias'][categoria]['pontos'] += pontos
            
            # 5. Verificar se subiu de nível
            cat_info = self.usuario['categorias'][categoria]
            if cat_info['pontos'] >= cat_info['meta']:
                cat_info['nivel'] += 1
                cat_info['meta'] *= 2  # Dobra a meta para o próximo nível
                messagebox.showinfo(
                    "Parabéns!", 
                    f"Você subiu para o nível {cat_info['nivel']} em {categoria}!\n"
                    f"Nova meta: {cat_info['meta']} pontos"
                )
            
            # 6. Salvar todas as alterações
            self.salvar_dados()
            messagebox.showinfo("Sucesso", f"Atividade registrada! Você ganhou {pontos} pontos.")
            self.mostrar_tela_inicial()
            # Salvar dados e voltar para a tela inicial
            self.salvar_dados()
            self.mostrar_tela_inicial()
        
        ttk.Button(frame_botoes, text="Salvar", command=salvar_atividade).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Cancelar", command=self.mostrar_tela_inicial).pack(side='left', padx=5)
        
        # Dicas para ganhar mais pontos
        frame_dicas = ttk.LabelFrame(self.root, text="Dicas para Ganhar Mais Pontos")
        frame_dicas.pack(pady=10, padx=20, fill='x')

        dicas_texto = """• Seja específico: "Tomei banho de 5 minutos" vale mais que "Tomei banho rápido"
• Mencione detalhes: "Desliguei o computador e o monitor ao sair"
• Combine ações: "Fiz uma refeição vegetariana com ingredientes orgânicos"
• Descreva o impacto: "Evitei o uso de 3 sacolas plásticas"
• Use palavras-chave: reciclar, economizar, reutilizar, energia solar, bicicleta, etc."""
        ttk.Label(frame_dicas, text=dicas_texto, justify='left', wraplength=700).pack(padx=10, pady=10)
        
        # Atualizar pontuação inicial
        atualizar_pontuacao()
    
    def mostrar_meu_progresso(self):
        self.limpar_tela()
        
        ttk.Label(self.root, text="Meu Progresso", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        # Frame para as barras de progresso
        frame_progresso = ttk.Frame(self.root)
        frame_progresso.pack(pady=10, padx=20, fill='x')
        
        for i, (categoria, dados) in enumerate(self.usuario['categorias'].items()):
            # Nome da categoria
            ttk.Label(frame_progresso, text=categoria, width=15, anchor='w').grid(row=i, column=0, pady=5, sticky='w')
            
            # Barra de progresso
            progresso = (dados['pontos'] / dados['meta']) * 100
            progresso = min(100, progresso)  # Limitar a 100%
            
            style = ttk.Style()
            style_name = f"{categoria.lower()}.Horizontal.TProgressbar"
            style.configure(style_name, troughcolor='#f0f0f0', background='#4CAF50')
            
            pb = ttk.Progressbar(frame_progresso, orient='horizontal', length=300, 
                                mode='determinate', style=style_name)
            pb['value'] = progresso
            pb.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
            
            # Porcentagem
            ttk.Label(frame_progresso, text=f"{dados['pontos']}/{dados['meta']} ({progresso:.1f}%)", 
                     width=15).grid(row=i, column=2, padx=5, pady=5)
        
        # Botão Voltar
        ttk.Button(self.root, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=20)
    
    def mostrar_ranking(self):
        self.limpar_tela()
        
        ttk.Label(self.root, text="Ranking", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        # Em uma versão real, aqui você buscaria os dados de vários usuários
        # Por enquanto, mostramos apenas o ranking do usuário atual
        
        frame_ranking = ttk.Frame(self.root)
        frame_ranking.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Cabeçalho
        ttk.Label(frame_ranking, text="Posição", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(frame_ranking, text="Nome", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2, sticky='w')
        ttk.Label(frame_ranking, text="Pontuação", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, padx=5, pady=2)
        ttk.Label(frame_ranking, text="Nível", font=('Helvetica', 10, 'bold')).grid(row=0, column=3, padx=5, pady=2)
        
        # Dados do usuário (simulando um ranking)
        dados_ranking = [
            (1, "Campeão", 5000, 5),
            (2, "Vice-campeão", 4500, 4),
            (3, "Terceiro lugar", 4000, 4),
            (4, self.usuario['nome'], self.usuario['pontuacao_total'], self.usuario['nivel']),
            (5, "Quinto lugar", 2000, 2)
        ]
        
        for i, (posicao, nome, pontos, nivel) in enumerate(dados_ranking, 1):
            # Destacar o usuário atual
            bg_color = '#e6f7ff' if nome == self.usuario['nome'] else ''
            
            ttk.Label(frame_ranking, text=str(posicao), background=bg_color).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            ttk.Label(frame_ranking, text=nome, background=bg_color).grid(row=i, column=1, padx=5, pady=2, sticky='w')
            ttk.Label(frame_ranking, text=str(pontos), background=bg_color).grid(row=i, column=2, padx=5, pady=2, sticky='e')
            ttk.Label(frame_ranking, text=str(nivel), background=bg_color).grid(row=i, column=3, padx=5, pady=2, sticky='e')
        
        # Botão Voltar
        ttk.Button(self.root, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreAmbientalApp(root)
    root.mainloop()
