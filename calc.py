import streamlit as st
import math
import re
from simpleeval import simple_eval

# Configuração da página
st.set_page_config(
    page_title="Calc-App!",
    layout="wide",  # Usar layout wide para melhor aproveitamento do espaço
    initial_sidebar_state="collapsed"
)

# URL do logo
logo_url = "https://i.imgur.com/yyDN6aD.png"

# Exibindo o logo pela URL
st.markdown(
    f"""
    <style>
        .centered-logo {{
            display: flex;
            justify-content: center;
        }}
        @media (max-width: 768px) {{
            .centered-logo img {{
                width: 200px;
            }}
        }}
    </style>
    <div class="centered-logo">
        <img src="{logo_url}" width="300">
    </div>
    """,
    unsafe_allow_html=True
)

# Título da aplicação
st.markdown("<h1 style='text-align: center;'>Calc-App!</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'>💬 Bem-vindos ao meu web app!</p>", unsafe_allow_html=True)

# CSS para criar um grid personalizado para a calculadora que funciona em dispositivos móveis
st.markdown("""
<style>
    /* Estilos para o contêiner principal da calculadora */
    .calc-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 10px;
    }
    
    /* Estilos para o display da calculadora */
    .calc-display {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px 15px;
        margin-bottom: 15px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    
    .calc-display p {
        margin: 0;
        padding: 0;
        font-size: 36px;
        font-weight: bold;
        color: black;
    }
    
    /* Grid para os botões da calculadora - Funciona em qualquer dispositivo */
    .calc-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
    }
    
    /* Estilos para os botões da calculadora */
    .calc-button {
        background-color: #f2f2f2;
        border: 1px solid #ccc;
        border-radius: 8px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
        user-select: none;
    }
    
    .calc-button:hover {
        background-color: #e6e6e6;
    }
    
    /* Ajustes específicos para dispositivos móveis */
    @media (max-width: 600px) {
        .calc-container {
            padding: 5px;
        }
        
        .calc-display {
            height: 50px;
        }
        
        .calc-display p {
            font-size: 28px;
        }
        
        .calc-grid {
            gap: 5px;
        }
        
        .calc-button {
            height: 45px;
            font-size: 20px;
        }
    }
    
    /* Ajustes para telas muito pequenas */
    @media (max-width: 350px) {
        .calc-button {
            height: 40px;
            font-size: 18px;
        }
        
        .calc-grid {
            gap: 3px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Função para realizar os cálculos com validação básica
def calcular(expressao):
    try:
        # Substituir operadores personalizados por operadores matemáticos
        expressao = expressao.replace("\u00F7", "/").replace("\u00D7", "*").replace("\uFF0D", "-").replace("\uFF0B", "+")

        # Substituir vírgula por ponto para compatibilidade com Python
        expressao = expressao.replace(",", ".")

        # Ajustar porcentagem para considerar o número anterior
        expressao = re.sub(r'(\d+)\s*-\s*(\d+)%', r'\1 - (\1 * \2 / 100)', expressao)
        expressao = re.sub(r'(\d+)\s*\+\s*(\d+)%', r'\1 + (\1 * \2 / 100)', expressao)
        expressao = re.sub(r'(\d+)\s*\*\s*(\d+)%', r'\1 * (\2 / 100)', expressao)
        expressao = re.sub(r'(\d+)\s*/\s*(\d+)%', r'\1 / (\2 / 100)', expressao)

        # Substituir √ por math.sqrt para calcular a raiz quadrada
        expressao = expressao.replace("\u221a", "math.sqrt")

        # Usar simpleeval para avaliar a expressão de forma segura
        resultado = simple_eval(expressao)

        # Se o resultado for um número inteiro, remover ponto e zero
        if isinstance(resultado, float) and resultado.is_integer():
            return int(resultado)  # Converte para inteiro, se for um número inteiro
        return resultado
    except Exception as e:
        return f"Erro: {str(e)}"

# Variáveis para controlar a expressão
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Variável para rastrear se uma ação de botão já foi processada
if "action_processed" not in st.session_state:
    st.session_state.action_processed = False

# Função para atualizar a expressão
def atualizar_expressao(valor):
    # Bloquear operadores no início ou após outro operador
    if valor in ["\u00F7", "\u00D7", "\uFF0D", "\uFF0B"]:
        if not st.session_state.expression or st.session_state.expression[-1] in ["\u00F7", "\u00D7", "\uFF0D", "\uFF0B"]:
            return  # Não adiciona o operador
    st.session_state.expression += valor
    st.session_state.action_processed = True

# Função para processar cliques em botões
def processar_acao(acao):
    if st.session_state.action_processed:
        return
    
    if acao == "=":
        # Quando o usuário clicar em igual, faz o cálculo
        st.session_state.expression = str(calcular(st.session_state.expression))
    elif acao == "C":
        # Limpa a expressão
        st.session_state.expression = ""
    elif acao == "Del":
        # Apaga o último caractere
        st.session_state.expression = st.session_state.expression[:-1]
    elif acao == "\u221a":
        # Calcula a raiz quadrada diretamente
        try:
            if st.session_state.expression:
                resultado = math.sqrt(float(st.session_state.expression))
                # Remover ponto e zero se o resultado for inteiro
                st.session_state.expression = str(int(resultado) if resultado.is_integer() else resultado)
            else:
                st.session_state.expression = "Erro: Vazio"
        except ValueError:
            st.session_state.expression = "Erro"
    elif acao == "%":
        # Adiciona o símbolo de porcentagem para ser tratado na função calcular
        atualizar_expressao("%")
    else:
        # Adiciona o número ou operador personalizado à expressão
        atualizar_expressao(acao)
    
    st.session_state.action_processed = True

# Centralizando a calculadora em uma coluna central
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Criando um contêiner HTML para a calculadora
    st.markdown(f"""
    <div class="calc-container">
        <div class="calc-display">
            <p>{st.session_state.expression}</p>
        </div>
        <div class="calc-grid">
    """, unsafe_allow_html=True)
    
    # Botões da calculadora
    buttons = [
        ["7", "8", "9", "\u00F7"],  # ícone de divisão
        ["4", "5", "6", "\u00D7"],  # ícone de multiplicação
        ["1", "2", "3", "\uFF0D"],  # ícone de subtração
        ["0", ".", "=", "\uFF0B"],  # ícone de soma
        ["%", "\u221a", "C", "Del"]
    ]
    
    # Criando botões usando HTML para garantir layout consistente em dispositivos móveis
    for row in buttons:
        for button in row:
            st.markdown(f"""
            <div class="calc-button" onclick="handleButtonClick('{button}')">{button}</div>
            """, unsafe_allow_html=True)
    
    # Fechando os contêineres HTML
    st.markdown("""
        </div>
    </div>
    
    <script>
        // Função para lidar com cliques nos botões
        function handleButtonClick(value) {
            // Enviando o valor clicado para o Streamlit via formulário
            const data = new FormData();
            data.append('acao', value);
            
            fetch('', {
                method: 'POST',
                body: data
            }).then(response => {
                window.location.reload();
            });
        }
    </script>
    """, unsafe_allow_html=True)
    
    # Usando um formulário escondido para receber as ações dos botões
    with st.form(key="calc_form", clear_on_submit=True):
        acao = st.text_input("Ação", key="acao", label_visibility="collapsed")
        submitted = st.form_submit_button("Enviar", type="primary")
        
        if submitted and acao:
            st.session_state.action_processed = False
            processar_acao(acao)
            st.rerun()
    
    # Adicionando também botões nativos do Streamlit como fallback
    col_rows = [st.columns(4) for _ in range(len(buttons))]
    
    for i, row in enumerate(buttons):
        for j, button in enumerate(row):
            with col_rows[i][j]:
                if st.button(button, key=f"btn_{i}_{j}"):
                    st.session_state.action_processed = False
                    processar_acao(button)
                    st.rerun()

# Informações de contato
st.markdown("""
---
<div style='text-align: center;'>
<h4>Calc-App! | Calculadora Web c/ raiz quadrada e porcentagem</h4>
<p>Por Ary Ribeiro. Contato, através do email: <a href='mailto:aryribeiro@gmail.com'>aryribeiro@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)