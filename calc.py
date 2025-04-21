import streamlit as st
import math
import re
from simpleeval import simple_eval

# Configuração da página
st.set_page_config(
    page_title="Calc-App!",
    layout="wide",  # Usar layout wide para melhor uso do espaço
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
        /* Reduz o tamanho do logo em dispositivos móveis */
        @media (max-width: 768px) {{
            .centered-logo img {{
                width: 150px;
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

# CSS para estilizar a interface da calculadora
st.markdown("""
    <style>
    /* Estilo dos botões e contêiner da calculadora */
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 5px;
    }
    
    /* Garantir que o texto do visor seja preto */
    div[data-testid="stText"] > div > p {
        color: black !important;
        font-weight: bold !important;
        font-size: 24px !important;
        text-align: right !important;
    }
    
    /* Melhorias para telas pequenas */
    @media (max-width: 768px) {
        .stButton > button {
            height: 45px;
            font-size: 18px;
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

# Função para atualizar a expressão
def atualizar_expressao(valor):
    # Bloquear operadores no início ou após outro operador
    if valor in ["\u00F7", "\u00D7", "\uFF0D", "\uFF0B"]:
        if not st.session_state.expression or st.session_state.expression[-1] in ["\u00F7", "\u00D7", "\uFF0D", "\uFF0B"]:
            return  # Não adiciona o operador
    st.session_state.expression += valor
    
# Colunas para centralizar a calculadora
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Criamos um contêiner com bordas para o visor
    st.markdown("""
    <div style="
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px 15px;
        margin-bottom: 15px;
        background-color: white;
        min-height: 50px;
    ">
    """, unsafe_allow_html=True)
    
    # Exibir a expressão
    st.text(st.session_state.expression)
    
    # Fechar o contêiner
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Botões da calculadora (usando ícones Unicode consistentes)
    buttons = [
        ["7", "8", "9", "\u00F7"],  # ícone de divisão
        ["4", "5", "6", "\u00D7"],  # ícone de multiplicação
        ["1", "2", "3", "\uFF0D"],  # ícone de subtração
        ["0", ".", "=", "\uFF0B"],  # ícone de soma
        ["%", "\u221a", "C", "Del"]
    ]
    
    # Loop para adicionar os botões
    for row in buttons:
        cols = st.columns(4)  # Sempre 4 colunas por linha
        for i, button in enumerate(row):
            with cols[i]:
                if st.button(button, key=f"btn_{button}_{buttons.index(row)}_{i}"):
                    if button == "=":
                        # Quando o usuário clicar em igual, faz o cálculo
                        st.session_state.expression = str(calcular(st.session_state.expression))
                    elif button == "C":
                        # Limpa a expressão
                        st.session_state.expression = ""
                    elif button == "Del":
                        # Apaga o último caractere
                        st.session_state.expression = st.session_state.expression[:-1]
                    elif button == "\u221a":
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
                    elif button == "%":
                        # Adiciona o símbolo de porcentagem para ser tratado na função calcular
                        atualizar_expressao("%")
                    else:
                        # Adiciona o número ou operador personalizado à expressão
                        atualizar_expressao(button)
                    
                    # Recarregar a página para atualizar
                    st.rerun()

# Informações de contato
st.markdown("""
---
<div style='text-align: center;'>
<h4>Calc-App! | Calculadora Web c/ raiz quadrada e porcentagem</h4>
<p>Por Ary Ribeiro. Contato, através do email: <a href='mailto:aryribeiro@gmail.com'>aryribeiro@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)