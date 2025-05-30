import streamlit as st
from backend.auth import Auth
import datetime

# Importar la clase Auth del backend
# Configuración de página
st.set_page_config(page_title="Plataforma Área de la Salud - Registro", layout="centered")

# CSS actualizado para un diseño más consistente
st.markdown("""
    <style>
        /* Fondo de la app */
        .stApp {
            background-color: #e0f7fa;
        }

        /* Contenedor principal */
        .main-container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 2rem auto;
        }

        /* Títulos */
        h1, h2, h3, h4, h5, h6, .stTitle {
            color: #333333;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        /* Subtítulos */
        .stSubheader {
            color: #555555;
            font-weight: 600;
            margin-bottom: 1rem;
            text-align: center;
        }

        /* Inputs */
        input, .stTextInput input, .stNumberInput input, .stTextArea textarea {
            color: #333333 !important;
            background-color: #ffffff !important;
            border: 1px solid #cccccc !important;
            border-radius: 8px !important;
            padding: 10px !important;
        }

        /* Botones */
        button[kind="primary"] {
            background-color: #007BFF !important;
            color: white !important;
            font-weight: bold;
            font-size: 16px;
            border-radius: 8px;
            padding: 10px 0;
            width: 100%;
            margin-top: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button[kind="primary"]:hover {
            background-color: #0056b3 !important;
        }

        /* Botones secundarios */
        .stButton button {
            background-color: #6c757d !important;
            color: white !important;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 16px;
            margin: 10px 5px;
        }

        /* Mensajes */
        .stSuccess, .stError, .stWarning {
            font-size: 14px;
            font-weight: 600;
            border-radius: 8px;
            padding: 12px 20px;
            margin-top: 1rem;
        }

        /* Barra de pasos */
        .stepper-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }

        .step {
            text-align: center;
        }

        .step-circle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: #cccccc;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            color: white;
            margin: 0 auto;
        }

        .step-circle.active {
            background-color: #007BFF;
        }

        .step-circle.completed {
            background-color: #28a745;
        }

        .step-label {
            margin-top: 8px;
            font-size: 14px;
            color: #555555;
        }

        .step-line {
            flex-grow: 1;
            height: 2px;
            background-color: #cccccc;
            margin: 0 10px;
        }

        .step-line.active {
            background-color: #007BFF;
        }

        .step-line.completed {
            background-color: #28a745;
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
        stepper_html = "<div class='stepper-container'>"
        for i, step in enumerate(self.steps):
            step_class = "completed" if i < self.current_step else "active" if i == self.current_step else ""
            stepper_html += f"""
            <div class='step'>
                <div class='step-circle {step_class}'>{i + 1}</div>
                <div class='step-label'>{step}</div>
            </div>"""
            if i < len(self.steps) - 1:
                line_class = "completed" if i < self.current_step else "active" if i == self.current_step else ""
                stepper_html += f"<div class='step-line {line_class}'></div>"
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
        
        st.session_state.fecha_nacimiento = st.date_input(
            "Fecha de nacimiento", 
            min_value=datetime.date(1900, 1, 1),  # Fecha mínima permitida
            max_value=datetime.date.today()      # Fecha máxima permitida (hoy)
)
        
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