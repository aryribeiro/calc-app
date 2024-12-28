import streamlit as st
import math
import re
from simpleeval import simple_eval

# Título da aplicação
st.title("Calculadora Interativa")

# CSS para estilizar a interface da calculadora.
st.markdown("""
    <style>
    .stButton>button {
        height: 40px;
        width: 60px;
        font-size: 20px;
        border-radius: 8px;
        color: black;
        background-color: #f2f2f2;
        border: 1px solid #ccc;
        margin: 2px;
    }

    .stTextInput>div>div>input {
        font-size: 24px;
        height: 50px;
        text-align: right;
    }

    .stButton { margin: 0; }

    </style>
""", unsafe_allow_html=True)

# Função para realizar os cálculos com validação básica
def calcular(expressao):
    try:
        # Substituir operadores personalizados por operadores matemáticos
        expressao = expressao.replace("Di", "/").replace("Mu", "*").replace("Su", "-").replace("So", "+")

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
    if st.session_state.expression == "Erro":
        st.session_state.expression = valor
    else:
        st.session_state.expression += valor

# Botões da calculadora
buttons = [
    ("7", "8", "9", "Di"),
    ("4", "5", "6", "Mu"),
    ("1", "2", "3", "Su"),
    ("0", ".", "=", "So"),
    ("%", "\u221a", "C", "Del")
]

# Exibir os botões com colunas ajustadas
colunas = [st.columns(4) for _ in range(len(buttons))]

# Loop para adicionar os botões
for i, row in enumerate(buttons):
    for j, button in enumerate(row):
        with colunas[i][j]:
            if st.button(button):
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
                            st.session_state.expression = str(math.sqrt(float(st.session_state.expression)))
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

# Exibir o resultado
if st.session_state.expression:
    st.markdown(f"<h3>Resultado: {st.session_state.expression}</h3>", unsafe_allow_html=True)
