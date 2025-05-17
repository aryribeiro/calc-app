import streamlit as st
import math
import re
from simpleeval import simple_eval

# Configuração da página
st.set_page_config(
    page_title="Calc-App!",
    layout="centered",
    page_icon="🧮",
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
st.title("Calc-App!")

st.markdown("""
💬 caso esteja no smartphone, deixe-o na horizontal p/ melhor visualização
""")

# CSS para estilizar a interface da calculadora com foco em responsividade
# Adicionando um grid CSS agressivo para forçar o layout em dispositivos móveis
st.markdown("""
    <style>
    /* Reset para os elementos do Streamlit em mobile */
    @media (max-width: 768px) {
        /* Forçar elementos horizontais em dispositivos móveis */
        .css-ocqkz7.e1tzin5v4,
        .css-1r6slb0.e1tzin5v2,
        .css-1kyxreq.etr89bj2,
        .css-5rimss.e16nr0p34,
        .stHorizontal {
            flex-direction: row !important;
            display: flex !important;
        }
        
        /* Forçar os elementos a ocuparem apenas 25% da largura (4 colunas) */
        .stHorizontal > div {
            width: 25% !important;
            min-width: 25% !important;
            flex: 1 1 25% !important;
        }
    }

    /* Estilo base dos botões */
    .stButton>button {
        height: 40px;
        width: 80%;
        font-size: 30px;
        border-radius: 8px;
        color: black;
        background-color: #f2f2f2;
        border: 1px solid #ccc;
        margin: 1px;
    }
    
    /* Define uma largura máxima para o contêiner da calculadora */
    .calculator-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 0;
    }
    
    /* Estilo para o display da calculadora */
    .calculator-display {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px 15px;
        margin-bottom: 15px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        width: calc(100% - 30px); /* Ajusta para incluir o padding */
        max-width: 100%;
    }
    
    .calculator-display h2 {
        margin: 0;
        padding: 0;
        font-size: 38px;
        color: black;
        font-weight: bold;
    }
    
    /* Remove padding extra das colunas do Streamlit */
    .row-widget.stButton {
        padding: 0 !important;
    }
    
    /* Melhoria para visualização em dispositivos móveis */
    @media (max-width: 768px) {
        /* Ajustes para o contêiner principal */
        .calculator-container {
            max-width: 100%;
            padding: 0 5px;
        }
        
        /* Ajustes para os botões */
        .stButton>button {
            width: 95%;
            height: 45px;
            font-size: 24px;
            padding: 0;
            margin: 2px 0;
        }
        
        /* Ajustes para o display */
        .calculator-display {
            height: 45px;
        }
        
        .calculator-display h2 {
            font-size: 28px;
        }
        
        /* Redução de padding geral para aproveitar melhor o espaço */
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            padding-top: 1rem;
            max-width: 100%;
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

# Contêiner da calculadora para controlar a largura
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# Exibir o display da calculadora usando um contêiner personalizado
st.markdown(
    f"""
    <div class="calculator-display">
        <h2>{st.session_state.expression}</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Botões da calculadora (usando ícones Unicode consistentes)
buttons = [
    ("7", "8", "9", "\u00F7"),  # ícone de divisão
    ("4", "5", "6", "\u00D7"),  # ícone de multiplicação
    ("1", "2", "3", "\uFF0D"),  # ícone de subtração
    ("0", ".", "=", "\uFF0B"),  # ícone de soma
    ("%", "\u221a", "C", "Del")
]

# Exibir os botões com colunas - usando gap específico e classe especial
for i, row in enumerate(buttons):
    cols = st.columns(4, gap="small")
    for j, button in enumerate(row):
        with cols[j]:
            # Adicionando chaves únicas aos botões
            if st.button(button, key=f"btn_{button}_{i}_{j}"):
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
                
                # Atualiza a página para mostrar a expressão atualizada
                st.rerun()

# Fechar o contêiner da calculadora
st.markdown('</div>', unsafe_allow_html=True)

# Informações de contato
st.markdown("""
---
#### 🧮 Calc-App! | Calculadora Web c/ raiz quadrada e porcentagem
Por Ary Ribeiro. Contato, através do email: aryribeiro@gmail.com
""")

st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        color: #333333;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    /* Esconde completamente todos os elementos da barra padrão do Streamlit */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    /* Remove qualquer espaço em branco adicional */
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Remove quaisquer margens extras */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)