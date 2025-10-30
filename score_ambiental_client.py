import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
import requests
from datetime import datetime, timedelta
from tkinter import simpledialog

# ========================
# CONFIG
# ========================
API_BASE_URL = "http://localhost:5000/api"

COLORS = {
    'primary': '#2C3E50',     # Azul escuro (cabeçalho)
    'secondary': '#3498DB',   # Azul
    'success': '#2ECC71',     # Verde
    'danger': '#E74C3C',      # Vermelho
    'warning': '#F39C12',     # Laranja
    'light': '#ECF0F1',       # Cinza claro
    'dark': '#2C3E50',        # Azul escuro
    'white': '#FFFFFF',       # Branco
    'background': '#F5F7FA',  # Cinza muito claro (fundo geral)
    'text': '#2C3E50',        # Azul escuro (texto)
    'border': '#BDC3C7'       # Cinza borda
}


class ScoreAmbientalClient:
    def __init__(self, root):
        self.root = root
        self.usuario = None
        self.usuario_id = None
        self.current_screen = None

        # Janela base
        self.root.title("EcoScore - Seu Score Ambiental")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=COLORS['background'])

        # fonte padrão
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=10)

        # estilos
        self.setup_styles()

        # centraliza
        self.center_window()

        # tela inicial = login
        self.mostrar_tela_login()

    # -------------------------------------------------
    # INFRA
    # -------------------------------------------------
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')

        # geral
        style.configure('.', font=('Segoe UI', 10))

        # frames
        style.configure('TFrame', background=COLORS['background'])

        style.configure('Header.TFrame',
                        background=COLORS['primary'],
                        borderwidth=0)

        style.configure('Sidebar.TFrame',
                        background=COLORS['dark'])

        style.configure('ContentOuter.TFrame',
                        background=COLORS['background'])

        style.configure('Card.TFrame',
                        background='white',
                        borderwidth=0,
                        relief='flat')

        style.configure('Footer.TFrame',
                        background=COLORS['primary'],
                        height=40)

        # labels
        style.configure('Title.TLabel',
                        font=('Segoe UI', 20, 'bold'),
                        background=COLORS['primary'],
                        foreground='white')

        style.configure('SectionTitle.TLabel',
                        font=('Segoe UI', 14, 'bold'),
                        background='white',
                        foreground=COLORS['dark'])

        style.configure('CardTitle.TLabel',
                        font=('Segoe UI', 12, 'bold'),
                        background='white',
                        foreground=COLORS['dark'])

        style.configure('MetricValue.TLabel',
                        font=('Segoe UI', 28, 'bold'),
                        background='white',
                        foreground=COLORS['primary'])

        style.configure('Description.TLabel',
                        font=('Segoe UI', 10),
                        background='white',
                        foreground=COLORS['text'])

        style.configure('Subtitle.TLabel',
                        font=('Segoe UI', 10),
                        background='white',
                        foreground='#666666')

        style.configure('Text.TLabel',
                        font=('Segoe UI', 10),
                        background='white',
                        foreground=COLORS['text'])

        style.configure('Muted.TLabel',
                        font=('Segoe UI', 9),
                        background='white',
                        foreground='#888888')

        style.configure('SuccessText.TLabel',
                        font=('Segoe UI', 10, 'bold'),
                        background='white',
                        foreground=COLORS['success'])

        style.configure('DangerText.TLabel',
                        font=('Segoe UI', 10, 'bold'),
                        background='white',
                        foreground=COLORS['danger'])

        style.configure('Footer.TLabel',
                        font=('Segoe UI', 9),
                        background=COLORS['primary'],
                        foreground='white')

        style.configure('FormLabel.TLabel',
                        font=('Segoe UI', 10, 'bold'),
                        background='white',
                        foreground=COLORS['dark'])

        style.configure('FormValue.TLabel',
                        font=('Segoe UI', 11, 'bold'),
                        background='white',
                        foreground=COLORS['dark'])

        # botões
        style.configure('TButton',
                        font=('Segoe UI', 10),
                        padding=10,
                        relief='flat',
                        borderwidth=0)

        style.configure('Accent.TButton',
                        background=COLORS['success'],
                        foreground='white')
        style.map('Accent.TButton',
                  background=[('active', '#25a25a'), ('pressed', '#1e8c4f')],
                  foreground=[('disabled', '#a0a0a0')])

        style.configure('Secondary.TButton',
                        background=COLORS['light'],
                        foreground=COLORS['dark'])
        style.map('Secondary.TButton',
                  background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')],
                  foreground=[('disabled', '#a0a0a0')])

        style.configure('Nav.TButton',
                        anchor='w',
                        padding=(15, 10),
                        background=COLORS['dark'],
                        foreground='white',
                        font=('Segoe UI', 10),
                        borderwidth=0)
        style.map('Nav.TButton',
                  background=[('active', '#3b4b5d'),
                              ('pressed', '#1e2a36')],
                  foreground=[('disabled', '#888888')])

        # entry / combobox
        style.configure('TEntry',
                        fieldbackground='white',
                        borderwidth=1,
                        relief='solid')
        style.configure('TCombobox',
                        fieldbackground='white',
                        background='white',
                        arrowsize=15,
                        borderwidth=1,
                        relief='solid')

        # scrollbar
        style.configure('TScrollbar',
                        background=COLORS['light'],
                        arrowsize=15,
                        borderwidth=0)

        # progressbar
        style.configure('TProgressbar',
                        background=COLORS['success'],
                        troughcolor=COLORS['light'],
                        borderwidth=0)

        # barra colorida embaixo dos cards
        style.configure('ColorBar.TFrame',
                        background=COLORS['primary'])

        # opções extras para listas
        self.root.option_add('*TCombobox*Listbox.font', ('Segoe UI', 10))
        self.root.option_add('*TCombobox*Listbox.background', 'white')
        self.root.option_add('*TCombobox*Listbox.foreground', COLORS['text'])
        self.root.option_add('*TCombobox*Listbox.selectBackground', COLORS['secondary'])
        self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')

        # estilo para Text widget
        text_style = {
            'background': 'white',
            'foreground': COLORS['text'],
            'font': ('Segoe UI', 10)
        }
        for key, value in text_style.items():
            self.root.option_add(f'*Text*{key}', value)

    def fazer_requisicao(self, metodo, endpoint, dados=None, auth_required=True):
        headers = {}
        if auth_required and self.usuario_id:
            headers['Authorization'] = f"Bearer {self.usuario_id}"

        url = f"{API_BASE_URL}{endpoint}"

        # DEBUG antes da request
        print("=== REQUISIÇÃO ===")
        print("Método :", metodo)
        print("URL    :", url)
        print("Headers:", headers)
        print("Body   :", dados)
        print("==================")

        try:
            if metodo == 'GET':
                response = requests.get(url, headers=headers)
            elif metodo == 'POST':
                response = requests.post(url, json=dados, headers=headers)
            elif metodo == 'PUT':
                response = requests.put(url, json=dados, headers=headers)
            else:
                raise ValueError(f"Método {metodo} não suportado")

            # DEBUG depois da resposta
            print("=== RESPOSTA ===")
            print("Status code:", response.status_code)
            print("Texto bruto :", response.text)
            print("================")

            if 200 <= response.status_code < 300:
                if response.text.strip():
                    try:
                        return response.json()
                    except ValueError:
                        print("⚠ Resposta 2xx mas não é JSON parseável.")
                        return {}
                return {}
            else:
                messagebox.showerror("Erro", f"Erro na requisição: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print("XXX EXCEPTION XXX")
            print(e)
            messagebox.showerror("Erro de Conexão",
                                 f"Não foi possível conectar ao servidor: {e}")
            return None

    def fazer_logout(self):
        self.usuario = None
        self.usuario_id = None
        self.mostrar_tela_login()

    # -------------------------------------------------
    # LÓGICA DE PONTOS
    # -------------------------------------------------
    def calcular_pontos_para_proximo_nivel(self):
        """
        Cada nível exige nível*100 pontos totais.
        Usa pontuacao_total que vem da API.
        """
        nivel_atual = self.usuario.get('nivel', 1)
        pontos_totais = self.usuario.get('pontuacao_total', 0)
        alvo = nivel_atual * 100
        faltam = max(0, alvo - pontos_totais)
        return faltam

    # -------------------------------------------------
    # ESTATÍSTICAS DO USUÁRIO
    # -------------------------------------------------
    def calcular_estatisticas_usuario(self):
        """
        Lê self.usuario (pegando /usuarios/<id>) e gera métricas:
        - pontos_hoje
        - pontos_7dias
        - media_pontos_por_atividade
        - categoria_top (categoria que mais somou pontos no total)
        - ultimas_atividades (lista das últimas 10)
        """
        # garantir dados atualizados
        dados = self.fazer_requisicao('GET', f'/usuarios/{self.usuario_id}')
        if dados:
            self.usuario = dados

        historico = self.usuario.get('historico', [])
        if not isinstance(historico, list):
            historico = []

        # normalizar datas pra datetime real
        def parse_dt(dt_str):
            # tenta ISO: "2025-10-30T15:33:58.639381"
            try:
                return datetime.fromisoformat(dt_str)
            except Exception:
                # fallback se vier "dd/mm/YYYY HH:MM"
                try:
                    return datetime.strptime(dt_str, "%d/%m/%Y %H:%M")
                except Exception:
                    return None

        agora = datetime.now()
        hoje_data = agora.date()
        sete_dias_atras = agora - timedelta(days=7)

        pontos_hoje = 0
        pontos_7dias = 0
        soma_pontos_total = 0
        total_atividades = 0
        pontos_por_categoria = {}

        # ordenar histórico mais recente primeiro
        historico_ordenado = sorted(
            historico,
            key=lambda x: x.get('data', ''),
            reverse=True
        )

        for atv in historico_ordenado:
            pts = atv.get('pontos', 0) or 0
            cat = atv.get('categoria', 'Outros')
            data_raw = atv.get('data')
            dt = parse_dt(data_raw)

            soma_pontos_total += pts
            total_atividades += 1

            # conta por categoria
            pontos_por_categoria[cat] = pontos_por_categoria.get(cat, 0) + pts

            if dt:
                if dt.date() == hoje_data:
                    pontos_hoje += pts
                if dt >= sete_dias_atras:
                    pontos_7dias += pts

        # média
        if total_atividades > 0:
            media_pontos = soma_pontos_total / total_atividades
        else:
            media_pontos = 0

        # top categoria
        if pontos_por_categoria:
            categoria_top = max(pontos_por_categoria, key=pontos_por_categoria.get)
        else:
            categoria_top = "—"

        # últimas 10 atividades
        ultimas_atividades = historico_ordenado[:10]

        return {
            'pontos_hoje': pontos_hoje,
            'pontos_7dias': pontos_7dias,
            'media_pontos': media_pontos,
            'categoria_top': categoria_top,
            'ultimas_atividades': ultimas_atividades
        }

    # -------------------------------------------------
    # COMPONENTES DE INTERFACE (REUSO)
    # -------------------------------------------------
    def montar_layout_base(self, titulo_header):
        """
        Cria header, sidebar e área principal.
        Retorna (content_frame) onde a tela específica vai desenhar.
        """
        self.limpar_tela()

        # HEADER
        header = ttk.Frame(self.root, style='Header.TFrame')
        header.pack(fill='x')
        ttk.Label(header,
                  text=titulo_header,
                  style='Title.TLabel').pack(pady=15)

        # ÁREA PRINCIPAL (sidebar + conteúdo)
        main_frame = ttk.Frame(self.root, style='ContentOuter.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)

        # SIDEBAR
        sidebar = ttk.Frame(main_frame, style='Sidebar.TFrame', width=200)
        sidebar.pack(side='left', fill='y', padx=(0, 20))

        nav_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        nav_frame.pack(fill='x', padx=10, pady=10)

        botoes_nav = [
            ("🏠 Início", self.mostrar_tela_principal),
            ("📝 Registrar Atividade", self.mostrar_tela_registro),
            ("📊 Meu Progresso", self.mostrar_meu_progresso),
            ("📈 Estatísticas", self.mostrar_estatisticas),
            ("🏆 Ranking", self.mostrar_ranking),
            ("⚙️ Configurações", self.mostrar_configuracoes),
            ("🚪 Sair", self.fazer_logout)
        ]

        for texto, comando in botoes_nav:
            ttk.Button(nav_frame,
                       text=texto,
                       style='Nav.TButton',
                       command=comando).pack(fill='x', pady=2, ipady=8)

        # CONTEÚDO (card branco grande)
        content = ttk.Frame(main_frame, style='Card.TFrame')
        content.pack(expand=True, fill='both')

        return content

    def criar_metric_card(self, parent, title, value, subtitle, color_hex):
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(side='left', expand=True, fill='both', padx=5, pady=5)

        # título
        ttk.Label(card,
                  text=title,
                  style='CardTitle.TLabel',
                  foreground=color_hex,
                  background='white').pack(anchor='w', padx=15, pady=(15, 5))

        # valor
        ttk.Label(card,
                  text=value,
                  style='MetricValue.TLabel',
                  foreground=color_hex,
                  background='white').pack(anchor='w', padx=15, pady=5)

        # subtítulo
        ttk.Label(card,
                  text=subtitle,
                  style='Subtitle.TLabel',
                  background='white').pack(anchor='w', padx=15, pady=(0, 15))

        # barra de destaque
        bar = ttk.Frame(card, style='ColorBar.TFrame', height=4)
        bar.pack(side='bottom', fill='x')

        return card

    def bloc_atividades_recentes(self, parent, limit=5):
        bloco = ttk.Frame(parent, style='Card.TFrame')
        bloco.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(bloco,
                  text="📅 Atividades Recentes",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(10, 5), padx=10)

        atividades = []
        if self.usuario and self.usuario.get('atividades'):
            atividades = self.usuario.get('atividades', [])
        elif self.usuario and self.usuario.get('historico'):
            atividades = self.usuario.get('historico', [])

        if not atividades:
            ttk.Label(bloco,
                      text="Nenhuma atividade registrada ainda.",
                      style='Text.TLabel',
                      background='white').pack(pady=20, padx=10, anchor='w')
            return bloco

        # mais recente primeiro
        atividades_ordenadas = sorted(
            atividades,
            key=lambda x: x.get('data', ''),
            reverse=True
        )[:limit]

        for atv in atividades_ordenadas:
            data_iso = atv.get('data', '')
            data_fmt = data_iso.split('T')[0] if 'T' in data_iso else data_iso

            desc = atv.get('descricao', 'Sem descrição')
            pontos = atv.get('pontos', 0)

            linha = ttk.Frame(bloco, style='Card.TFrame')
            linha.pack(fill='x', padx=10, pady=5)

            top_row = ttk.Frame(linha, style='Card.TFrame')
            top_row.pack(fill='x')

            ttk.Label(top_row,
                      text=data_fmt,
                      style='Muted.TLabel').pack(side='left')

            ttk.Label(top_row,
                      text=f"+{pontos} pts",
                      style=('SuccessText.TLabel' if pontos > 0 else 'DangerText.TLabel')
                      ).pack(side='right')

            ttk.Label(linha,
                      text=desc,
                      style='Description.TLabel',
                      wraplength=600,
                      justify='left').pack(anchor='w', pady=(2, 0))

        return bloco

    # -------------------------------------------------
    # TELAS
    # -------------------------------------------------

    # LOGIN
    def mostrar_tela_login(self):
        self.limpar_tela()

        main_frame = ttk.Frame(self.root, style='Card.TFrame')
        main_frame.pack(expand=True, padx=40, pady=40)

        ttk.Label(main_frame, text="🌱 EcoScore", style='Title.TLabel').pack(pady=(30, 10))
        ttk.Label(main_frame, text="Faça login para continuar",
                  style='Subtitle.TLabel',
                  background='white').pack(pady=(0, 30))

        form_frame = ttk.Frame(main_frame, style='Card.TFrame')
        form_frame.pack(padx=40, pady=10, fill='x')

        # Email
        ttk.Label(form_frame, text="Email", style='FormLabel.TLabel').grid(
            row=0, column=0, pady=(0, 5), sticky='w')
        email_var = tk.StringVar()
        email_entry = ttk.Entry(form_frame, textvariable=email_var, width=40)
        email_entry.grid(row=1, column=0, pady=(0, 20), ipady=8)

        # Senha
        ttk.Label(form_frame, text="Senha", style='FormLabel.TLabel').grid(
            row=2, column=0, pady=(0, 5), sticky='w')
        senha_var = tk.StringVar()
        senha_entry = ttk.Entry(form_frame, textvariable=senha_var, show="•", width=40)
        senha_entry.grid(row=3, column=0, pady=(0, 20), ipady=8)

        btns = ttk.Frame(form_frame, style='Card.TFrame')
        btns.grid(row=4, column=0, pady=(10, 20))

        ttk.Button(btns,
                   text="Entrar",
                   style='Accent.TButton',
                   command=lambda: self.fazer_login(email_var.get(), senha_var.get())
                   ).pack(side='left', padx=5, ipadx=20)

        ttk.Button(btns,
                   text="Criar Conta",
                   style='Secondary.TButton',
                   command=self.mostrar_tela_cadastro
                   ).pack(side='left', padx=5, ipadx=20)

        ttk.Label(main_frame,
                  text="© 2025 EcoScore - Todos os direitos reservados",
                  style='Subtitle.TLabel',
                  background='white',
                  font=('Segoe UI', 8)).pack(pady=(20, 10))

        email_entry.focus()

        for widget in [email_entry, senha_entry]:
            widget.bind('<Return>', lambda e: self.fazer_login(email_var.get(), senha_var.get()))

    def fazer_login(self, email, senha):
        if not email or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        dados = {'email': email, 'senha': senha}
        response = self.fazer_requisicao('POST', '/login', dados, auth_required=False)

        if response and response.get('sucesso'):
            self.usuario_id = response.get('usuario_id')
            self.usuario = response.get('usuario', {})
            self.mostrar_tela_principal()
        else:
            messagebox.showerror("Erro de Login", "Email ou senha inválidos.")

    # CADASTRO
    def mostrar_tela_cadastro(self):
        self.limpar_tela()

        main_frame = ttk.Frame(self.root, style='Card.TFrame')
        main_frame.pack(expand=True, padx=40, pady=40)

        ttk.Label(main_frame, text="Criar Nova Conta",
                  style='Title.TLabel').pack(pady=(30, 10))
        ttk.Label(main_frame, text="Preencha os dados para se cadastrar",
                  style='Subtitle.TLabel',
                  background='white').pack(pady=(0, 30))

        form_frame = ttk.Frame(main_frame, style='Card.TFrame')
        form_frame.pack(padx=40, pady=10, fill='x')

        # Nome
        ttk.Label(form_frame, text="Nome Completo", style='FormLabel.TLabel').grid(
            row=0, column=0, pady=(0, 5), sticky='w')
        nome_var = tk.StringVar()
        nome_entry = ttk.Entry(form_frame, textvariable=nome_var, width=40)
        nome_entry.grid(row=1, column=0, pady=(0, 15), ipady=8)

        # Email
        ttk.Label(form_frame, text="E-mail", style='FormLabel.TLabel').grid(
            row=2, column=0, pady=(0, 5), sticky='w')
        email_var = tk.StringVar()
        email_entry = ttk.Entry(form_frame, textvariable=email_var, width=40)
        email_entry.grid(row=3, column=0, pady=(0, 15), ipady=8)

        # Senha
        ttk.Label(form_frame, text="Senha", style='FormLabel.TLabel').grid(
            row=4, column=0, pady=(0, 5), sticky='w')
        senha_var = tk.StringVar()
        senha_entry = ttk.Entry(form_frame, textvariable=senha_var, show="•", width=40)
        senha_entry.grid(row=5, column=0, pady=(0, 15), ipady=8)

        # Confirmar Senha
        ttk.Label(form_frame, text="Confirmar Senha", style='FormLabel.TLabel').grid(
            row=6, column=0, pady=(0, 5), sticky='w')
        confirmar_senha_var = tk.StringVar()
        confirmar_senha_entry = ttk.Entry(form_frame, textvariable=confirmar_senha_var, show="•", width=40)
        confirmar_senha_entry.grid(row=7, column=0, pady=(0, 20), ipady=8)

        def cadastrar():
            nome = nome_var.get().strip()
            email = email_var.get().strip()
            senha = senha_var.get()
            confirmar_senha = confirmar_senha_var.get()

            if not all([nome, email, senha, confirmar_senha]):
                messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
                return

            if senha != confirmar_senha:
                messagebox.showwarning("Atenção", "As senhas não conferem!")
                return

            dados = {'nome': nome, 'email': email, 'senha': senha}
            resposta = self.fazer_requisicao('POST', '/cadastrar', dados, auth_required=False)

            if resposta and resposta.get('sucesso'):
                messagebox.showinfo("Sucesso", "Cadastro realizado! Faça login.")
                self.mostrar_tela_login()
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar. Tente novamente.")

        btn_frame = ttk.Frame(form_frame, style='Card.TFrame')
        btn_frame.grid(row=8, column=0, pady=(10, 20))

        ttk.Button(btn_frame,
                   text="Cadastrar",
                   style='Accent.TButton',
                   command=cadastrar).pack(side='left', padx=5, ipadx=20)

        ttk.Button(btn_frame,
                   text="Voltar ao Login",
                   style='Secondary.TButton',
                   command=self.mostrar_tela_login).pack(side='left', padx=5, ipadx=20)

        nome_entry.focus()

        for widget in [nome_entry, email_entry, senha_entry, confirmar_senha_entry]:
            widget.bind('<Return>', lambda e: cadastrar())

    # DASHBOARD PRINCIPAL
    def mostrar_tela_principal(self):
        content = self.montar_layout_base("🌱 Meu Score Ambiental")

        # Boas-vindas
        welcome_frame = ttk.Frame(content, style='Card.TFrame')
        welcome_frame.pack(fill='x', padx=10, pady=10)

        nome_user = self.usuario.get('nome', 'Usuário')
        ttk.Label(welcome_frame,
                  text=f"Olá, {nome_user}!",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(10, 5), padx=10)

        ttk.Label(welcome_frame,
                  text="Bem-vindo ao seu painel de controle ambiental.",
                  style='Text.TLabel',
                  background='white').pack(anchor='w', padx=10, pady=(0, 10))

        # Métricas
        metrics_frame = ttk.Frame(content, style='Card.TFrame')
        metrics_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(metrics_frame,
                  text="📊 Suas Métricas",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(10, 5), padx=10)

        metrics_row = ttk.Frame(metrics_frame, style='Card.TFrame')
        metrics_row.pack(fill='x', padx=10, pady=(0, 10))

        pontos_totais = self.usuario.get('pontuacao_total', 0)
        nivel_atual = self.usuario.get('nivel', 1)
        faltam = self.calcular_pontos_para_proximo_nivel()

        self.criar_metric_card(
            metrics_row,
            "Pontuação Total",
            str(pontos_totais),
            "Pontos acumulados",
            COLORS['primary']
        )

        self.criar_metric_card(
            metrics_row,
            "Nível Atual",
            str(nivel_atual),
            f"Nível {nivel_atual}",
            COLORS['secondary']
        )

        self.criar_metric_card(
            metrics_row,
            "Próximo Nível",
            f"+{faltam} pts",
            "Faltam para subir de nível",
            COLORS['success']
        )

        # Atividades Recentes
        self.bloc_atividades_recentes(content, limit=5)

        # Rodapé
        footer = ttk.Frame(self.root, style='Footer.TFrame')
        footer.pack(side='bottom', fill='x')
        ttk.Label(footer,
                  text="© 2025 EcoScore - Todos os direitos reservados",
                  style='Footer.TLabel').pack(pady=5)

    # REGISTRAR ATIVIDADE
    def mostrar_tela_registro(self):
        content = self.montar_layout_base("📝 Registrar Atividade")

        form_frame = ttk.Frame(content, style='Card.TFrame')
        form_frame.pack(padx=40, pady=30, fill='both', expand=True)

        ttk.Label(form_frame,
                  text="Nova Atividade",
                  style='SectionTitle.TLabel').grid(
            row=0, column=0, columnspan=2, pady=(0, 20), sticky='w')

        # Categoria
        ttk.Label(form_frame,
                  text="Categoria:",
                  style='FormLabel.TLabel').grid(
            row=1, column=0, pady=5, sticky='w')

        categorias = [
            'Água', 'Energia', 'Mobilidade', 'Alimentação',
            'Resíduos', 'Bem-estar', 'Consumo Consciente',
            'Educação Ambiental', 'Tecnologia Verde'
        ]

        categoria_var = tk.StringVar()
        categoria_combo = ttk.Combobox(
            form_frame,
            textvariable=categoria_var,
            values=categorias,
            state='readonly',
            width=30
        )
        categoria_combo.grid(row=1, column=1, pady=5, sticky='w')
        categoria_combo.current(0)

        # Descrição
        ttk.Label(form_frame,
                  text="Descrição:",
                  style='FormLabel.TLabel').grid(
            row=2, column=0, pady=5, sticky='nw')

        descricao_text = tk.Text(form_frame,
                                 height=5,
                                 width=40,
                                 wrap='word',
                                 font=('Segoe UI', 10))
        descricao_text.grid(row=2, column=1, pady=5, sticky='ew')

        # Pontuação estimada
        ttk.Label(form_frame,
                  text="Pontuação estimada:",
                  style='FormLabel.TLabel').grid(
            row=3, column=0, pady=5, sticky='w')

        pontos_var = tk.StringVar(value="0")
        pontos_label = ttk.Label(form_frame,
                                 text="0 pontos",
                                 style='FormValue.TLabel',
                                 background='white')
        pontos_label.grid(row=3, column=1, pady=5, sticky='w')

        def calcular_pontuacao_descricao(descricao, categoria):
            PONTOS_POR_PALAVRA = 2
            BONUS_POR_CATEGORIA = {
                'reciclagem': 5,
                'reutilizacao': 5,
                'economia_agua': 7,
                'economia_energia': 7,
                'mobilidade': 5,
                'outros': 2
            }
            num_palavras = len(descricao.split())
            pontos_local = num_palavras * PONTOS_POR_PALAVRA
            pontos_local += BONUS_POR_CATEGORIA.get(categoria.lower().replace(" ", "_"), 0)
            pontos_local = max(1, min(pontos_local, 50))
            return pontos_local

        def atualizar_pontuacao(event=None):
            descricao = descricao_text.get("1.0", tk.END).strip()
            categoria = categoria_var.get()
            if descricao and categoria:
                pontos_calc = calcular_pontuacao_descricao(descricao, categoria)
                pontos_var.set(str(pontos_calc))
                pontos_label.config(text=f"{pontos_calc} pontos")
            else:
                pontos_var.set("0")
                pontos_label.config(text="0 pontos")

        descricao_text.bind('<KeyRelease>', atualizar_pontuacao)
        categoria_combo.bind('<<ComboboxSelected>>', atualizar_pontuacao)

        # Botões
        btn_frame = ttk.Frame(form_frame, style='Card.TFrame')
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))

        def salvar_atividade():
            descricao = descricao_text.get("1.0", tk.END).strip()
            categoria = categoria_var.get()
            pontos = int(pontos_var.get()) if pontos_var.get().isdigit() else 0

            if not descricao or not categoria:
                messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
                return
            if pontos <= 0:
                messagebox.showwarning("Atenção", "A atividade deve ter uma pontuação maior que zero.")
                return

            dados = {
                'categoria': categoria,
                'descricao': descricao,
                'pontos': pontos,
                'data': datetime.now().isoformat()
            }

            resposta = self.fazer_requisicao('POST',
                                             f'/usuarios/{self.usuario_id}/atividades',
                                             dados)

            if resposta and resposta.get('id'):
                # atualiza usuário
                user_atualizado = self.fazer_requisicao('GET', f'/usuarios/{self.usuario_id}')
                if user_atualizado:
                    self.usuario = user_atualizado

                messagebox.showinfo(
                    "Sucesso",
                    f"Atividade registrada! (+{pontos} pts)"
                )
                self.mostrar_tela_principal()
            else:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível registrar a atividade. Veja o terminal para detalhes."
                )

        ttk.Button(btn_frame,
                   text="Salvar Atividade",
                   style='Accent.TButton',
                   command=salvar_atividade).pack(side='left', padx=5, ipadx=20)

        ttk.Button(btn_frame,
                   text="Cancelar",
                   style='Secondary.TButton',
                   command=self.mostrar_tela_principal).pack(side='left', padx=5, ipadx=20)

        atualizar_pontuacao()

    # MEU PROGRESSO
    def mostrar_meu_progresso(self):
        content = self.montar_layout_base("📊 Meu Progresso")

        # pega usuário atualizado
        resposta = self.fazer_requisicao('GET', f'/usuarios/{self.usuario_id}')
        if resposta:
            self.usuario = resposta

        frame_progresso = ttk.Frame(content, style='Card.TFrame')
        frame_progresso.pack(pady=20, padx=20, fill='x')

        ttk.Label(frame_progresso,
                  text="Progresso por Categoria",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(0, 15))

        categorias_user = self.usuario.get('categorias', {})

        grid_frame = ttk.Frame(frame_progresso, style='Card.TFrame')
        grid_frame.pack(fill='x')

        for i, (categoria, dados) in enumerate(categorias_user.items()):
            pontos = dados.get('pontos', 0)
            meta = dados.get('meta', 0)
            progresso = (pontos / meta) * 100 if meta > 0 else 0
            progresso = min(100, progresso)

            ttk.Label(grid_frame,
                      text=categoria,
                      style='Text.TLabel',
                      background='white',
                      width=20).grid(row=i, column=0, pady=5, sticky='w')

            style_temp = ttk.Style()
            style_name = f"{categoria}.Horizontal.TProgressbar"
            style_temp.configure(style_name,
                                 troughcolor='#f0f0f0',
                                 background=COLORS['success'])

            pb = ttk.Progressbar(grid_frame,
                                 orient='horizontal',
                                 length=300,
                                 mode='determinate',
                                 style=style_name)
            pb['value'] = progresso
            pb.grid(row=i, column=1, padx=10, pady=5, sticky='w')

            ttk.Label(grid_frame,
                      text=f"{pontos}/{meta} ({progresso:.1f}%)",
                      style='Text.TLabel',
                      background='white',
                      width=20).grid(row=i, column=2, padx=5, pady=5, sticky='w')

    # ESTATÍSTICAS (AGORA FUNCIONA)
    def mostrar_estatisticas(self):
        content = self.montar_layout_base("📈 Estatísticas")

        stats = self.calcular_estatisticas_usuario()

        # Bloco resumo (cards de métricas)
        metrics_frame = ttk.Frame(content, style='Card.TFrame')
        metrics_frame.pack(fill='x', padx=20, pady=(20, 10))

        ttk.Label(metrics_frame,
                  text="Resumo recente",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(10, 5), padx=10)

        metrics_row = ttk.Frame(metrics_frame, style='Card.TFrame')
        metrics_row.pack(fill='x', padx=10, pady=(0, 10))

        self.criar_metric_card(
            metrics_row,
            "Pontos Hoje",
            str(stats['pontos_hoje']),
            "Somados no dia atual",
            COLORS['primary']
        )

        self.criar_metric_card(
            metrics_row,
            "Últimos 7 dias",
            str(stats['pontos_7dias']),
            "Total de pontos na última semana",
            COLORS['secondary']
        )

        self.criar_metric_card(
            metrics_row,
            "Média / Atividade",
            f"{stats['media_pontos']:.1f}",
            "Pontos médios por registro",
            COLORS['success']
        )

        # Categoria destaque
        destaque_frame = ttk.Frame(content, style='Card.TFrame')
        destaque_frame.pack(fill='x', padx=20, pady=(10, 10))

        ttk.Label(destaque_frame,
                  text="Categoria que mais pontuou",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(10, 5), padx=10)

        ttk.Label(destaque_frame,
                  text=stats['categoria_top'],
                  style='MetricValue.TLabel',
                  foreground=COLORS['warning'],
                  background='white').pack(anchor='w', padx=20, pady=(0, 15))

        # Lista das últimas atividades
        ult_frame = ttk.Frame(content, style='Card.TFrame')
        ult_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        ttk.Label(ult_frame,
                  text="Últimas atividades registradas",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(10, 5), padx=10)

        if not stats['ultimas_atividades']:
            ttk.Label(ult_frame,
                      text="Nenhuma atividade registrada ainda.",
                      style='Text.TLabel',
                      background='white').pack(anchor='w', padx=20, pady=(0, 10))
        else:
            # cabeçalho
            header_row = ttk.Frame(ult_frame, style='Card.TFrame')
            header_row.pack(fill='x', padx=15, pady=(0, 5))

            ttk.Label(header_row, text="Data", style='FormLabel.TLabel',
                      background='white', width=18).grid(row=0, column=0, sticky='w')
            ttk.Label(header_row, text="Categoria", style='FormLabel.TLabel',
                      background='white', width=18).grid(row=0, column=1, sticky='w')
            ttk.Label(header_row, text="Descrição", style='FormLabel.TLabel',
                      background='white', width=40).grid(row=0, column=2, sticky='w')
            ttk.Label(header_row, text="Pontos", style='FormLabel.TLabel',
                      background='white', width=10).grid(row=0, column=3, sticky='e')

            # linhas
            for i, atv in enumerate(stats['ultimas_atividades'], start=1):
                linha = ttk.Frame(ult_frame, style='Card.TFrame')
                linha.pack(fill='x', padx=15, pady=2)

                data_raw = atv.get('data', '')
                if "T" in data_raw:
                    data_fmt = data_raw.replace("T", " ").split(".")[0]
                else:
                    data_fmt = data_raw

                cat = atv.get('categoria', '—')
                desc = atv.get('descricao', 'Sem descrição')
                pts = atv.get('pontos', 0)

                tk.Label(linha, text=data_fmt, anchor='w', width=18, bg='white').grid(row=0, column=0, sticky='w')
                tk.Label(linha, text=cat, anchor='w', width=18, bg='white').grid(row=0, column=1, sticky='w')
                tk.Label(linha, text=desc, anchor='w', width=40, bg='white', justify='left', wraplength=400).grid(row=0, column=2, sticky='w')
                tk.Label(linha, text=str(pts), anchor='e', width=10, bg='white').grid(row=0, column=3, sticky='e')

    # CONFIGURAÇÕES
    def mostrar_configuracoes(self):
        content = self.montar_layout_base("⚙️ Configurações")

        bloco = ttk.Frame(content, style='Card.TFrame')
        bloco.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(bloco,
                  text="Configurações da Conta",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(10, 5), padx=10)

        ttk.Label(bloco,
                  text="Aqui futuramente você vai alterar nome, senha, preferências de notificação etc.",
                  style='Text.TLabel',
                  background='white').pack(anchor='w', padx=10, pady=(0, 10))

        ttk.Button(bloco,
                   text="Sair da conta",
                   style='Secondary.TButton',
                   command=self.fazer_logout).pack(anchor='w', padx=10, pady=(20, 0))

    # RANKING
    def mostrar_ranking(self):
        content = self.montar_layout_base("🏆 Ranking")

        ttk.Label(content,
                  text="Ranking de Usuários",
                  style='SectionTitle.TLabel').pack(anchor='w', pady=(20, 10), padx=20)

        # busca ranking via API
        resposta = self.fazer_requisicao('GET', '/ranking')
        if not resposta:
            ttk.Label(content,
                      text="Não foi possível carregar o ranking.",
                      style='Text.TLabel',
                      background='white').pack(anchor='w', padx=20, pady=(0, 10))
            return

        # container com scroll
        container = ttk.Frame(content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, highlightthickness=0, bg='white')
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')

        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", on_configure)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # cabeçalho
        header_row = ttk.Frame(scrollable_frame, style='Card.TFrame')
        header_row.grid(row=0, column=0, sticky='w', pady=(0, 10))

        ttk.Label(header_row, text="Posição", style='FormLabel.TLabel',
                  background='white', width=10).grid(row=0, column=0, padx=5, sticky='w')
        ttk.Label(header_row, text="Nome", style='FormLabel.TLabel',
                  background='white', width=30).grid(row=0, column=1, padx=5, sticky='w')
        ttk.Label(header_row, text="Nível", style='FormLabel.TLabel',
                  background='white', width=10).grid(row=0, column=2, padx=5, sticky='e')
        ttk.Label(header_row, text="Pontuação", style='FormLabel.TLabel',
                  background='white', width=15).grid(row=0, column=3, padx=5, sticky='e')

        # linhas do ranking
        for i, usuario in enumerate(resposta, 1):
            linha = ttk.Frame(scrollable_frame, style='Card.TFrame')
            linha.grid(row=i, column=0, sticky='w')

            destaque = (usuario.get('id') == self.usuario_id)
            bg_color = '#E3F2FD' if destaque else 'white'

            tk.Label(linha, text=f"{i}º", anchor='w', width=10, bg=bg_color).grid(row=0, column=0, padx=5, pady=2, sticky='w')
            tk.Label(linha, text=usuario.get('nome', ''), anchor='w', width=30, bg=bg_color).grid(row=0, column=1, padx=5, pady=2, sticky='w')
            tk.Label(linha, text=str(usuario.get('nivel', '')), anchor='e', width=10, bg=bg_color).grid(row=0, column=2, padx=5, pady=2, sticky='e')
            tk.Label(linha, text=str(usuario.get('pontuacao_total', '')), anchor='e', width=15, bg=bg_color).grid(row=0, column=3, padx=5, pady=2, sticky='e')

        # posiciona scroll
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


# ========================
# MAIN
# ========================
if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreAmbientalClient(root)
    root.mainloop()
