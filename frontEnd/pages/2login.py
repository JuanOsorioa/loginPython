import streamlit as st
from backend.auth import Auth
# Importar la clase Auth del backend

# Configuración inicial de la página
st.set_page_config(page_title="Sistema de Salud - Inicio de Sesión", layout="centered")

# Estilo personalizado
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
        }

        header, footer {
            visibility: hidden;
            height: 0;
        }

        .stApp {
            background-color: #B3E5FC;
        }

        .main-container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 35px rgba(0, 60, 80, 0.2);
            max-width: 480px;
            margin: 0 auto;
        }

        h2.title {
            color: #000000;
            font-size: 2.8rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.2em;
        }

        .subtitle {
            color: #333;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 1.8em;
        }

        label, .css-16idsys, .css-qrbaxs, .css-1cpxqw2, .css-1v0mbdj, .st-bw {
            color: black !important;
            font-weight: 600 !important;
        }

        input, .stTextInput input {
            color: black !important;
            background-color: #E1F5FE !important;
        }

        button[kind="primary"] {
            background-color: #0288D1 !important;
            color: white !important;
            font-weight: bold;
            font-size: 16px;
            border-radius: 14px;
            padding: 12px;
            width: 100%;
            margin-top: 18px;
        }

        button[kind="primary"]:hover {
            background-color: #0277BD !important;
        }

        .stSuccess, .stError {
            font-size: 16px;
            font-weight: 600;
            border-radius: 14px;
            padding: 14px 22px;
        }
    </style>
""", unsafe_allow_html=True)

# Contenedor principal visual
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<h2 class="title">Bienvenido</h2>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Por favor inicia sesión para acceder al sistema.</p>', unsafe_allow_html=True)

# Formulario de inicio de sesión
usuario = st.text_input("Nombre de usuario", placeholder="Escribe tu usuario")
clave = st.text_input("Contraseña", type="password", placeholder="Escribe tu contraseña")

if st.button("Ingresar"):
    user = Auth.login_user(usuario, clave)
    if user:
        st.session_state.user = user
        st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)
