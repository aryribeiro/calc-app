import streamlit as st
import math
import re
from simpleeval import simple_eval

# Configuração da página
st.set_page_config(
    page_title="Calc-App!",
    layout="centered",
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
st.title("Calc-App!")

st.markdown("""
💬 Bem-vindos ao meu web app!
""")

# Variáveis para controlar a expressão
if "expression" not in st.session_state:
    st.session_state.expression = ""

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

# Processar botões e ações
def processar_acao(acao):
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
        atualizar_expressao(acao)
    else:
        # Adiciona o número ou operador personalizado à expressão
        atualizar_expressao(acao)
    
    # Forçar recarregamento da página
    st.rerun()

# Função para atualizar a expressão
def atualizar_expressao(valor):
    # Bloquear operadores no início ou após outro operador
    if valor in ["\u00F7", "\u00D7", "\uFF0D", "\uFF0B"]:
        if not st.session_state.expression or st.session_state.expression[-1] in ["\u00F7", "\u00D7", "\uFF0D", "\uFF0B"]:
            return  # Não adiciona o operador
    st.session_state.expression += valor

# Botões da calculadora (usando ícones Unicode consistentes)
buttons = [
    ["7", "8", "9", "\u00F7"],  # ícone de divisão
    ["4", "5", "6", "\u00D7"],  # ícone de multiplicação
    ["1", "2", "3", "\uFF0D"],  # ícone de subtração
    ["0", ".", "=", "\uFF0B"],  # ícone de soma
    ["%", "\u221a", "C", "Del"]
]

# Criando um CSS personalizado para a calculadora
st.markdown("""
<style>
    /* Estilo para o contêiner principal da calculadora */
    .calculator {
        max-width: 400px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
    }
    
    /* Estilo para o display */
    .calc-display {
        width: 100%;
        height: 60px;
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-bottom: 10px;
        position: relative;
        overflow: hidden;
    }
    
    .calc-display span {
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 28px;
        font-weight: bold;
        color: black;
    }
    
    /* Grid de botões */
    .calc-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 5px;
    }
    
    /* Estilo dos botões */
    .calc-button {
        height: 50px;
        background-color: #f2f2f2;
        border: 1px solid #ccc;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        cursor: pointer;
    }
    
    .calc-button:hover {
        background-color: #e6e6e6;
    }
    
    /* Ajustes para dispositivos móveis */
    @media (max-width: 480px) {
        .calculator {
            max-width: 100%;
        }
        
        .calc-button {
            height: 45px;
            font-size: 18px;
        }
        
        .calc-display {
            height: 50px;
        }
        
        .calc-display span {
            font-size: 24px;
        }
    }
    
    /* Ainda mais compacto para telas muito pequenas */
    @media (max-width: 320px) {
        .calc-button {
            height: 40px;
            font-size: 16px;
        }
        
        .calc-grid {
            gap: 3px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Criando a calculadora com HTML puro para controle total do layout
st.markdown(f"""
<div class="calculator">
    <div class="calc-display">
        <span>{st.session_state.expression}</span>
    </div>
    <div class="calc-grid">
""", unsafe_allow_html=True)

# Gerando HTML para cada botão
for row in buttons:
    for button in row:
        button_value = button
        button_display = button
        # Criando um ID único para cada botão
        button_id = f"btn_{button}"
        
        st.markdown(f"""
        <div class="calc-button" id="{button_id}" onclick="handleClick('{button_value}')">{button_display}</div>
        """, unsafe_allow_html=True)

# Fechando os contêineres
st.markdown("""
    </div>
</div>

<script>
    // Função para lidar com cliques nos botões
    function handleClick(value) {
        // Esta função é executada no navegador
        // Enviando ação para o Streamlit via formulário
        const data = new FormData();
        data.append('acao', value);
        fetch('', {
            method: 'POST',
            body: data
        }).then(response => {
            // Recarregar a página para aplicar a mudança
            window.location.reload();
        });
    }
</script>
""", unsafe_allow_html=True)

# Formulário oculto para capturar cliques nos botões HTML
with st.form(key='calc_form', clear_on_submit=True):
    acao = st.text_input("Ação", key="acao", label_visibility="collapsed")
    submitted = st.form_submit_button("Enviar", style="display:none;")
    
    if submitted and acao:
        processar_acao(acao)

# Informações de contato
st.markdown("""
---
#### Calc-App! | Calculadora Web c/ raiz quadrada e porcentagem
Por Ary Ribeiro. Contato, através do email: aryribeiro@gmail.com
""")