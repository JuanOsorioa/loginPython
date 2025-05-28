import streamlit as st

# guardado de datos tmporal
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {}

st.set_page_config(page_title="Plataforma Área de la Salud", layout="centered")

# CSS 
st.markdown("""
    <style>
        /* Eliminar padding y header */
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

        /* Contenedor principal visual */
        .main-container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 35px rgba(0, 60, 80, 0.2);
            max-width: 480px;
            margin: 0 auto;
        }

        /* Título principal */
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

        /* Inputs y labels */
        label, .css-16idsys, .css-qrbaxs, .css-1cpxqw2, .css-1v0mbdj, .st-bw {
            color: black !important;
            font-weight: 600 !important;
        }

        input, .stTextInput input {
            color: black !important;
            background-color: #E1F5FE !important;
        }

        /* Arregla el radio group */
        div[data-baseweb="radio"] {
            background-color: transparent !important;
        }

        div[data-baseweb="radio"] label {
            color: black !important;
            font-weight: bold;
            font-size: 16px;
        }

        /* Botones */
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

        /* Mensajes */
        .stSuccess, .stError, .stWarning {
            font-size: 16px;
            font-weight: 600;
            border-radius: 14px;
            padding: 14px 22px;
        }
    </style>
""", unsafe_allow_html=True)

# Contenedor
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Título y subtítulo
st.markdown('<h2 class="title">Bienvenido</h2>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Inicia sesión o crea tu cuenta para acceder.</p>', unsafe_allow_html=True)

# Radio
modo = st.radio("Selecciona una opción", ["Iniciar sesión", "Registrarse"])

if modo == "Iniciar sesión":
    usuario = st.text_input("Nombre de usuario", placeholder="Escribe tu usuario")
    clave = st.text_input("Contraseña", type="password", placeholder="Escribe tu contraseña")

    if st.button("Ingresar"):
        if usuario in st.session_state.usuarios and st.session_state.usuarios[usuario] == clave:
            st.success(f"Bienvenido, {usuario}")
        else:
            st.error("Usuario o contraseña incorrectos.")

elif modo == "Registrarse":
    nuevo_usuario = st.text_input("Nuevo nombre de usuario", placeholder="Crea tu usuario")
    nueva_clave = st.text_input("Nueva contraseña", type="password", placeholder="Crea tu contraseña")
    confirmar_clave = st.text_input("Confirmar contraseña", type="password", placeholder="Confirma tu contraseña")

    if st.button("Crear cuenta"):
        if nuevo_usuario in st.session_state.usuarios:
            st.warning("El usuario ya existe. Elige otro nombre.")
        elif nueva_clave != confirmar_clave:
            st.warning("Las contraseñas no coinciden.")
        elif len(nueva_clave) < 4:
            st.warning("La contraseña debe tener al menos 4 caracteres.")
        elif nuevo_usuario.strip() == "":
            st.warning("El nombre de usuario no puede estar vacío.")
        else:
            st.session_state.usuarios[nuevo_usuario] = nueva_clave
            st.success(f"Usuario '{nuevo_usuario}' creado con éxito. Ahora inicia sesión.")

st.markdown('</div>', unsafe_allow_html=True)
