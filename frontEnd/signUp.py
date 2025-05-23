import streamlit as st

def mostrar():
    st.title("Crear cuenta nueva")

    # Inicializamos el paso
    if "registro_paso" not in st.session_state:
        st.session_state.registro_paso = 1

    # Paso 1: Datos de acceso
    if st.session_state.registro_paso == 1:
        st.subheader("Paso 1: Ingresa tu nombre de usuario y contraseña")
        st.session_state.new_username = st.text_input("Nombre de usuario")
        st.session_state.new_password = st.text_input("Contraseña", type="password")
        st.session_state.confirm_password = st.text_input("Confirmar contraseña", type="password")

        if st.button("Siguiente"):
            if not st.session_state.new_username or not st.session_state.new_password or not st.session_state.confirm_password:
                st.warning("Completa todos los campos para continuar.")
            elif st.session_state.new_password != st.session_state.confirm_password:
                st.error("Las contraseñas no coinciden.")
            else:
                st.session_state.registro_paso = 2

    # Paso 2: Datos personales
    elif st.session_state.registro_paso == 2:
        st.subheader("Paso 2: Datos personales")
        st.session_state.nombre_completo = st.text_input("Nombre completo")
        st.session_state.rol = st.selectbox("Rol", ["usuario", "admin"])

        col1, col2 = st.columns(2)
        if col1.button("Volver"):
            st.session_state.registro_paso = 1

        if col2.button("Siguiente"):
            if st.session_state.nombre_completo:
                st.session_state.registro_paso = 3
            else:
                st.warning("Ingresa tu nombre completo.")

    # Paso 3: Confirmación
    elif st.session_state.registro_paso == 3:
        st.subheader("Paso 3: Confirmación")

        st.write("**Usuario:**", st.session_state.new_username)
        st.write("**Nombre completo:**", st.session_state.nombre_completo)
        st.write("**Rol:**", st.session_state.rol)

        col1, col2 = st.columns(2)
        if col1.button("Volver"):
            st.session_state.registro_paso = 2

        if col2.button("Registrarse"):
            # Aquí se llamaría a la función del backend para insertar en la base de datos
            st.success("¡Registro exitoso!")
            st.session_state.registro_paso = 1  # Resetear si deseas volver a empezar

if __name__ == "__main__":
    mostrar()
