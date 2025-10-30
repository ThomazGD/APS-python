# Score Ambiental - Aplicativo Desktop

Aplicativo desktop desenvolvido em Python com PySimpleGUI para monitoramento de hábitos sustentáveis.

## Funcionalidades

- Cadastro e login de usuários
- Registro de atividades sustentáveis
- Acompanhamento de pontuação por categoria
- Níveis de progresso
- Histórico de atividades
- Interface gráfica amigável

## Requisitos

- Python 3.6 ou superior
- PySimpleGUI

## Instalação

1. Instale as dependências:

```bash
pip install PySimpleGUI
```

2. Execute o aplicativo:

```bash
python score_ambiental.py
```

## Como Usar

1. **Cadastro**:
   - Na tela inicial, clique em "Cadastrar"
   - Preencha os dados solicitados
   - Clique em "Cadastrar"

2. **Login**:
   - Na tela inicial, clique em "Entrar"
   - Informe email e senha
   - Clique em "Entrar"

3. **Registrar Atividade**:
   - No painel principal, clique em "Registrar Atividade"
   - Selecione a categoria
   - Descreva a atividade
   - Defina a pontuação
   - Clique em "Salvar"

4. **Acompanhar Progresso**:
   - Visualize seu nível atual e pontuação total
   - Acompanhe o progresso em cada categoria
   - Veja seu histórico de atividades

## Estrutura do Projeto

- `score_ambiental.py`: Código-fonte principal
- `score_ambiental_data.json`: Armazena os dados do usuário

## Personalização

Você pode personalizar o aplicativo editando:

- Cores e temas no código (variável `sg.theme()`)
- Categorias de atividades na variável `user_data`
- Fórmula de pontuação e níveis

## Licença

Este projeto está licenciado sob a licença MIT.
