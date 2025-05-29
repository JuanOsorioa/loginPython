import streamlit as st

# CSS
st.markdown("""
    <style>
        
        header, footer, .css-18e3th9 {visibility: hidden;}

        
        .stApp {
            background-color: #b3e5fc;
        }

        
        h1, p, label {
            color: black !important;
            font-weight: bold;
        }

        input {
            background-color: #e3f2fd !important;
            color: black !important;
        }

        ::placeholder {
            color: black !important;
        }

        
        .css-15zrgzn svg {
            filter: invert(100%);
        }

        
        .custom-button {
            background-color: #111;
            color: white;
            font-weight: bold;
            padding: 10px 24px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s ease;
        }

        .custom-button:hover {
            background-color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# primera parte
st.markdown("<h1 style='text-align: center;'>Bienvenido</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Por favor inicia sesión.</p>", unsafe_allow_html=True)

# usuario y clave
usuario = st.text_input("Nombre de usuario", placeholder="Escribe tu usuario")
clave = st.text_input("Contraseña", type="password", placeholder="Escribe tu contraseña")

# Botón de ingreso aca va la base de datos
if st.markdown('<button class="custom-button" type="submit">Ingresar</button>', unsafe_allow_html=True):
    st.info("ingresando.")
