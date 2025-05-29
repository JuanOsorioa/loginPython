import streamlit as st

# Configuración de página
st.set_page_config(page_title="Plataforma Área de la Salud - Registro", layout="centered")

# CSS con letras más oscuras
st.markdown("""
    <style>
        /* Fondo de la app */
        .stApp {
            background-color: #0277BD;
        }

        /* Contenedor principal del signup */
        .main-container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 35px rgba(0, 60, 80, 0.2);
            max-width: 480px;
            margin: 2rem auto 2rem auto;
        }

        /* Títulos */
        h1, h2, h3, h4, h5, h6, .stTitle {
            color: #111111;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1rem;
        }

        /* Subtítulos */
        .stSubheader {
            color: #222222;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        }

        /* Labels y texto de inputs */
        label, .css-16idsys, .css-qrbaxs, .css-1cpxqw2, .css-1v0mbdj, .st-bw {
            color: #111111 !important;
            font-weight: 600 !important;
        }

        input, .stTextInput input {
            color: #111111 !important;
            background-color: #E1F5FE !important;
            border-radius: 8px !important;
            padding: 8px !important;
        }

        /* Botones */
        button[kind="primary"] {
            background-color: #0288D1 !important;
            color: white !important;
            font-weight: bold;
            font-size: 16px;
            border-radius: 14px;
            padding: 12px 0;
            width: 100%;
            margin-top: 18px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button[kind="primary"]:hover {
            background-color: #0277BD !important;
        }

        /* Botones en columnas */
        .stButton button {
            min-width: 120px;
            margin: 8px 4px;
        }

        /* Mensajes */
        .stSuccess, .stError, .stWarning {
            font-size: 16px;
            font-weight: 600;
            border-radius: 14px;
            padding: 14px 22px;
            margin-top: 1rem;
        }

        /* Stepper: personalización */
        div[style*="display:flex"] {
            max-width: 480px;
            margin: 0 auto 2rem auto;
        }
        div[style*="border-radius:50%"] {
            box-shadow: 0 0 8px rgba(0,0,0,0.15);
            transition: background-color 0.3s ease;
        }
        div[style*="text-align:center"] > div:nth-child(2) {
            margin-top: 8px;
            font-weight: 600;
            color: #222222;
            font-size: 14px;
        }
        div[style*="flex-grow:1"] {
            background-color: #B0BEC5 !important;
            margin: 0 8px;
        }
    </style>
""", unsafe_allow_html=True)


class StepperBar:
    def __init__(self, steps, orientation='horizontal', active_color='#0288D1', completed_color='#4CAF50', inactive_color='#B0BEC5'):
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
                <div style='margin-top:5px; color:#222222;'>{step}</div>
            </div>"""
            if i < len(self.steps) - 1:
                stepper_html += f"<div style='flex-grow:1; height:2px; background-color:{self.inactive_color};'></div>"
        stepper_html += "</div>"
        return stepper_html


def mostrar():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

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
        st.session_state.presion = st.text_input("Presión")
        st.session_state.tipo_sangre = st.selectbox("Tipo de sangre", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        st.session_state.estatura = st.text_input("Estatura (cm)")
        st.session_state.peso = st.text_input("Peso (kg)")

        col1, col2 = st.columns(2)
        if col1.button("Volver"):
            st.session_state.registro_paso = 1
        if col2.button("Siguiente"):
            if all([st.session_state.nombre_completo, st.session_state.presion, st.session_state.tipo_sangre, st.session_state.estatura, st.session_state.peso]):
                st.session_state.registro_paso = 3
            else:
                st.warning("Completa todos los campos personales.")

    # Paso 3: Confirmación
    elif st.session_state.registro_paso == 3:
        st.subheader("Paso 3: Confirmación")

        st.write("**Usuario:**", st.session_state.new_username)
        st.write("**Nombre completo:**", st.session_state.nombre_completo)
        st.write("**Presión:**", st.session_state.presion)
        st.write("**Tipo de sangre:**", st.session_state.tipo_sangre)
        st.write("**Estatura:**", st.session_state.estatura)
        st.write("**Peso:**", st.session_state.peso)

        col1, col2 = st.columns(2)
        if col1.button("Volver"):
            st.session_state.registro_paso = 2
        if col2.button("Registrarse"):
            # Aquí guardarías los datos en la base de datos si fuera necesario
            st.session_state.registro_paso = 4

    # Paso 4: Éxito
    elif st.session_state.registro_paso == 4:
        st.subheader("Genial, ya estás registrado 🎉")
        st.success("Tu cuenta fue creada con éxito.")

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    mostrar()
