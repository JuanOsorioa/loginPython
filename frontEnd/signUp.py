import streamlit as st

class StepperBar:
    def __init__(self, steps, orientation='horizontal', active_color='blue', completed_color='green', inactive_color='gray'):
        self.steps = steps
        self.current_step = 0
        self.orientation = orientation
        self.active_color = active_color
        self.completed_color = completed_color
        self.inactive_color = inactive_color

    def set_current_step(self, step):
        if 0 <= step < len(self.steps):
            self.current_step = step
        else:
            raise ValueError("Step index out of range")

    def display(self):
        if self.orientation == 'horizontal':
            return self._display_horizontal()
        elif self.orientation == 'vertical':
            return self._display_vertical()
        else:
            raise ValueError("Orientation must be either 'horizontal' or 'vertical'")

    def _display_horizontal(self):
        stepper_html = "<div style='display:flex; justify-content:space-between; align-items:center;'>"
        for i, step in enumerate(self.steps):
            color = self.completed_color if i < self.current_step else self.inactive_color
            current_color = self.active_color if i == self.current_step else color
            stepper_html += f"""
            <div style='text-align:center;'>
                <div style='width:30px; height:30px; border-radius:50%; background-color:{current_color}; display:inline-block;'></div>
                <div style='margin-top:5px;'>{step}</div>
            </div>"""
            if i < len(self.steps) - 1:
                stepper_html += f"<div style='flex-grow:1; height:2px; background-color:{self.inactive_color};'></div>"
        stepper_html += "</div>"
        return stepper_html

def mostrar():
    st.title("Crear cuenta nueva")

    steps = ["Acceso", "Datos personales", "Confirmación", "Final"]
    if "registro_paso" not in st.session_state:
        st.session_state.registro_paso = 1

    # Mostrar barra de pasos
    stepper = StepperBar(steps)
    stepper.set_current_step(st.session_state.registro_paso - 1)
    st.markdown(stepper.display(), unsafe_allow_html=True)

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
            # Aquí normalmente se conectaría a la base de datos
            st.session_state.registro_paso = 4

    # Paso 4: Éxito y redirección
    elif st.session_state.registro_paso == 4:
        st.subheader("Genial, ya estás registrado 🎉")
        st.success("Tu cuenta fue creada con éxito.")
        if st.button("Ir al inicio de sesión"):
            st.switch_page("pages/login.py")  # Asegúrate de tener el archivo login.py en la misma carpeta

if __name__ == "__main__":
    mostrar()
