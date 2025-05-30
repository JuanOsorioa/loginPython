import streamlit as st
from backend.auth import Auth
from backend.database import db
from fpdf import FPDF

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

# Sesión
if 'user' not in st.session_state:
    st.session_state.user = None

# Login
if not st.session_state.user:
    st.markdown("<h1 style='text-align: center;'>🩺 Ingreso al Sistema</h1>", unsafe_allow_html=True)
    st.markdown("Por favor, inicie sesión para acceder a sus datos.")

    usuario = st.text_input("👤 Nombre de usuario")
    clave = st.text_input("🔐 Contraseña", type="password")

    if st.button("Ingresar"):
        user = Auth.login_user(usuario, clave)
        if user:
            st.session_state.user = user
            st.success("Inicio de sesión exitoso.")
            st.rerun()  # Cambiado de experimental_rerun a rerun
        else:
            st.error("Usuario o contraseña incorrectos.")

def calcular_imc(peso, estatura):
    return peso / (estatura / 100) ** 2

def generar_informe_pdf(datos_usuario, datos_medicos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Informe Médico", ln=True, align="C")
    pdf.ln(10)

    # Datos personales
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nombre: {datos_usuario['primer_nombre']} {datos_usuario['primer_apellido']}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha de nacimiento: {datos_usuario['fecha_nacimiento']}", ln=True)
    pdf.cell(200, 10, txt=f"Correo: {datos_usuario['correo']}", ln=True)
    pdf.cell(200, 10, txt=f"Celular: {datos_usuario['celular']}", ln=True)
    pdf.ln(10)

    # Datos médicos
    imc = calcular_imc(datos_medicos["peso"], datos_medicos["estatura"])
    pdf.cell(200, 10, txt=f"IMC: {imc:.2f}", ln=True)
    if imc < 18.5:
        pdf.cell(200, 10, txt="Estado: Bajo peso. Se recomienda una dieta balanceada.", ln=True)
    elif 18.5 <= imc <= 24.9:
        pdf.cell(200, 10, txt="Estado: Peso normal. Mantenga un estilo de vida saludable.", ln=True)
    elif 25 <= imc <= 29.9:
        pdf.cell(200, 10, txt="Estado: Sobrepeso. Se recomienda actividad física regular.", ln=True)
    else:
        pdf.cell(200, 10, txt="Estado: Obesidad. Consulte a un especialista.", ln=True)

    pdf.cell(200, 10, txt=f"Presión arterial: {datos_medicos['presion']}", ln=True)
    if datos_medicos["presion"] == "normal":
        pdf.cell(200, 10, txt="Estado: Presión arterial normal.", ln=True)
    else:
        pdf.cell(200, 10, txt="Estado: Presión arterial anormal. Consulte a un médico.", ln=True)

    pdf.cell(200, 10, txt=f"Temperatura: {datos_medicos['temperatura']}°C", ln=True)
    if 36.1 <= datos_medicos["temperatura"] <= 37.2:
        pdf.cell(200, 10, txt="Estado: Temperatura normal.", ln=True)
    else:
        pdf.cell(200, 10, txt="Estado: Temperatura anormal. Podría indicar fiebre o hipotermia.", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Recomendaciones generales:", ln=True)
    pdf.cell(200, 10, txt="- Mantenga una dieta equilibrada.", ln=True)
    pdf.cell(200, 10, txt="- Realice actividad física regularmente.", ln=True)
    pdf.cell(200, 10, txt="- Consulte a un médico si presenta síntomas persistentes.", ln=True)

    return pdf

# Página principal
if st.session_state.user:
    nombre = st.session_state.user["nombre_usuario"].capitalize()
    
    st.markdown(f"""
        <div class="welcome-box">
            <h2>👨‍⚕️ Bienvenido, <strong>{nombre}</strong></h2>
            <p class="heart">❤️ Tu salud es prioridad.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📄 ¿Desea descargar sus datos en PDF?")
    if st.button("Descargar PDF"):
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            # Obtener datos del usuario
            cursor.execute("SELECT primer_nombre, primer_apellido, fecha_nacimiento, correo, celular FROM usuarios WHERE id = %s", (st.session_state.user["id"],))
            datos_usuario = cursor.fetchone()
            datos_usuario = dict(zip([desc[0] for desc in cursor.description], datos_usuario))

            # Obtener datos médicos
            cursor.execute("SELECT peso, estatura, presion, temperatura FROM datos_medicos WHERE usuario_id = %s", (st.session_state.user["id"],))
            datos_medicos = cursor.fetchone()
            datos_medicos = dict(zip([desc[0] for desc in cursor.description], datos_medicos))

            # Generar PDF
            pdf = generar_informe_pdf(datos_usuario, datos_medicos)
            pdf_output = f"{datos_usuario['primer_nombre']}_informe_medico.pdf"
            pdf.output(pdf_output)

            # Descargar PDF
            with open(pdf_output, "rb") as file:
                st.download_button("Haga clic aquí para descargar su informe médico", file, file_name=pdf_output)
        except Exception as e:
            st.error(f"Error al generar el informe: {e}")
        finally:
            cursor.close()
            db.return_connection(conn)
