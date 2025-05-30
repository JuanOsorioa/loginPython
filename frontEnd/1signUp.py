import streamlit as st
from backend.auth import Auth
# Importar la clase Auth del backend
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

        /* Botón de login especial */
        .login-button {
            background-color: #4CAF50 !important;
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

        .login-button:hover {
            background-color: #45A049 !important;
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
        
        # Información básica
        st.markdown("**📋 Información básica**")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.primer_nombre = st.text_input("Primer nombre", placeholder="Ej: Juan")
            st.session_state.primer_apellido = st.text_input("Primer apellido", placeholder="Ej: Pérez")
        with col2:
            st.session_state.segundo_nombre = st.text_input("Segundo nombre (opcional)", placeholder="Ej: Carlos")
            st.session_state.segundo_apellido = st.text_input("Segundo apellido (opcional)", placeholder="Ej: García")
        
        st.session_state.fecha_nacimiento = st.date_input("Fecha de nacimiento")
        
        st.session_state.correo = st.text_input("Correo electrónico", placeholder="ejemplo@correo.com")
        
        # Contacto y ubicación
        st.markdown("**📞 Contacto y ubicación**")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.celular = st.text_input("Número de celular", placeholder="Ej: +57 300 123 4567")
        with col2:
            st.session_state.ubicacion = st.text_input("Ciudad/Ubicación", placeholder="Ej: Medellín, Antioquia")
        
        st.session_state.direccion = st.text_area("Dirección completa", 
                                                placeholder="Ej: Calle 50 # 25-30, Barrio Laureles", 
                                                height=80)
        
        # Datos médicos
        st.markdown("**🏥 Información médica**")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.tipo_sangre = st.selectbox("Tipo de sangre", 
                                                      ["Seleccionar...", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                                      index=0)
        with col2:
            st.session_state.presion = st.text_input("Presión arterial", placeholder="Ej: 120/80")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.estatura = st.number_input("Estatura (cm)", 
                                                      min_value=100, 
                                                      max_value=250, 
                                                      value=170, 
                                                      step=1)
        with col2:
            st.session_state.peso = st.number_input("Peso (kg)", 
                                                  min_value=30.0, 
                                                  max_value=300.0, 
                                                  value=70.0, 
                                                  step=0.5)
        with col3:
            st.session_state.temperatura = st.number_input("Temperatura corporal (°C)", 
                                                         min_value=35.0, 
                                                         max_value=42.0, 
                                                         value=36.5, 
                                                         step=0.1)

        col1, col2 = st.columns(2)
        if col1.button("Volver"):
            st.session_state.registro_paso = 1
        if col2.button("Siguiente"):
            # Validar campos obligatorios
            campos_requeridos = [
                st.session_state.get('primer_nombre', ''),
                st.session_state.get('primer_apellido', ''),
                st.session_state.get('correo', ''),
                st.session_state.get('celular', ''),
                st.session_state.get('ubicacion', ''),
                st.session_state.get('direccion', ''),
                st.session_state.get('presion', '')
            ]
            
            if (all(campos_requeridos) and 
                st.session_state.get('tipo_sangre', '') != "Seleccionar..." and
                st.session_state.get('fecha_nacimiento') is not None):
                st.session_state.registro_paso = 3
            else:
                st.warning("Por favor completa todos los campos obligatorios para continuar.")

    # Paso 3: Confirmación
    elif st.session_state.registro_paso == 3:
        st.subheader("Paso 3: Confirmación")

        st.markdown("**👤 Datos de acceso**")
        st.write("**Usuario:**", st.session_state.new_username)
        
        st.markdown("**📋 Información personal**")
        
        # Construir nombre completo para mostrar
        primer_nombre = st.session_state.get('primer_nombre', '')
        segundo_nombre = st.session_state.get('segundo_nombre', '')
        primer_apellido = st.session_state.get('primer_apellido', '')
        segundo_apellido = st.session_state.get('segundo_apellido', '')
        
        nombre_completo = f"{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}".strip()
        nombre_completo = ' '.join(nombre_completo.split())  # Eliminar espacios extra
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Nombre completo:**", nombre_completo)
            st.write("**Correo:**", st.session_state.get('correo', ''))
            st.write("**Celular:**", st.session_state.get('celular', ''))
            st.write("**Ubicación:**", st.session_state.get('ubicacion', ''))
        with col2:
            st.write("**Fecha de nacimiento:**", st.session_state.get('fecha_nacimiento', ''))
            st.write("**Tipo de sangre:**", st.session_state.get('tipo_sangre', ''))
            st.write("**Presión arterial:**", st.session_state.get('presion', ''))
            st.write("**Temperatura:**", f"{st.session_state.get('temperatura', 0)}°C")
        
        st.write("**Dirección:**", st.session_state.get('direccion', ''))
        st.write("**Estatura:**", f"{st.session_state.get('estatura', 0)} cm")
        st.write("**Peso:**", f"{st.session_state.get('peso', 0)} kg")

        col1, col2 = st.columns(2)
        try:
            if Auth.register_user(st.session_state):
                st.session_state.registro_paso = 4
        except Exception as e:
            st.error(f"Error al registrar: {e}")

    # Paso 4: Éxito
    elif st.session_state.registro_paso == 4:
        st.subheader("Genial, ya estás registrado 🎉")
        st.success("Tu cuenta fue creada con éxito.")
        
        # Botón para ir al login
        if st.button("Ir al Login", key="login_redirect"):
            # Limpiar el estado del registro
            st.session_state.registro_paso = 1
            # Limpiar todos los campos del formulario
            campos_a_limpiar = [
                'new_username', 'new_password', 'confirm_password',
                'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
                'fecha_nacimiento', 'correo', 'celular', 'ubicacion', 'direccion', 
                'presion', 'tipo_sangre', 'estatura', 'peso', 'temperatura'
            ]
            
            for campo in campos_a_limpiar:
                if campo in st.session_state:
                    del st.session_state[campo]
            
            # Mostrar mensaje y enlace manual
            st.success("¡Registro completado! Ahora puedes iniciar sesión.")
            st.markdown("**[Haz clic aquí para ir al Login](http://localhost:8501/2login)**")
            st.info("O ejecuta: streamlit run C:/Users/juani/login_app/frontEnd/pages/2login.py")

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    mostrar()