import streamlit as st

# css
st.markdown("""
    <style>
        .stApp {
            background-color: #e0f7fa;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h4, h5, h6, p, label, div, span {
            color: #004d40 !important;
        }

        
        .stButton > button {
            background-color: #007acc;
            color: white !important;
            border-radius: 10px;
            border: none;
            padding: 0.6em 1.2em;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #005b9f;
            transform: scale(1.03);
        }

        .welcome-box {
            background-color: #ffffff;
            border-left: 6px solid #007acc;
            padding: 1.5em;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }

        .heart {
            color: red;
            font-size: 22px;
        }
    </style>
""", unsafe_allow_html=True)

#  sesión 
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = ""

#  Login
if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align: center;'>🩺 Ingreso al Sistema</h1>", unsafe_allow_html=True)
    st.markdown("Por favor, inicie sesion para acceder a sus datos.")

    usuario = st.text_input("👤 Nombre de usuario")
    clave = st.text_input("🔐 Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario and clave:  # aqui va la base de datos
            st.session_state.autenticado = True
            st.session_state.usuario_actual = usuario
            st.success("Inicio de sesión exitoso.")
        else:
            st.error("Usuario o contraseña incorrectos.")

#  Pagina principal
if st.session_state.autenticado:
    nombre = st.session_state.usuario_actual.capitalize()
    
    st.markdown(f"""
        <div class="welcome-box">
            <h2>👨‍⚕️ Bienvenido, <strong>{nombre}</strong></h2>
            <p class="heart">❤️ Tu salud es prioridad.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📄 ¿Desea descargar sus datos en PDF?")
    st.button("Descargar PDF")
