import streamlit as st

#este es el titulo

st.title("Inicio de sesión")

# las casillas de datos
usuario = st.text_input("Nombre de usuario")
clave = st.text_input("Contraseña", type="password")

# el boton con las condiciones de ingreso
if st.button("Ingresar"):
    if usuario == "angus" and clave == "1021":
        st.success("Bienvenido")
    else:
        st.error("Usuario o contraseña incorrectos")