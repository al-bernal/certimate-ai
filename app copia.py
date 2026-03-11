import streamlit as st

st.set_page_config(page_title="CertiMate AI", page_icon="📘", layout="centered")

# ----- Estado de sesión -----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola, soy CertiMate AI. Puedo ayudarte a estudiar certificaciones cloud y AI. "
                "Pregúntame cualquier concepto y te lo explicaré de forma clara."
            ),
        }
    ]

if "exam" not in st.session_state:
    st.session_state.exam = "AZ-104"

if "mode" not in st.session_state:
    st.session_state.mode = "Explicación"

# ----- Sidebar -----
with st.sidebar:
    st.title("⚙️ Configuración")

    st.session_state.exam = st.selectbox(
        "Certificación",
        ["AZ-104", "AI-102", "AWS AI Practitioner", "AWS ML Specialty"],
        index=0,
    )

    st.session_state.mode = st.selectbox(
        "Modo",
        ["Explicación", "Resumen", "Quiz"],
        index=0,
    )

    if st.button("🗑️ Borrar conversación"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversación reiniciada. ¿Qué tema quieres estudiar ahora?",
            }
        ]
        st.rerun()

# ----- Título -----
st.title("📘 CertiMate AI")
st.caption("Asistente básico para estudiar certificaciones cloud y AI")

# ----- Mostrar historial -----
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----- Función de respuesta local -----
def local_response(user_text: str, exam: str, mode: str) -> str:
    if mode == "Resumen":
        return (
            f"**Resumen para {exam}:**\n\n"
            f"Tema consultado: **{user_text}**\n\n"
            "- Definición breve del concepto\n"
            "- Cuándo se utiliza\n"
            "- Punto clave para examen\n"
            "- Error común que debes evitar\n\n"
            "Esta es una versión local de demostración. Después podemos conectar una API real."
        )

    if mode == "Quiz":
        return (
            f"**Quiz de práctica para {exam}:**\n\n"
            f"Pregunta sobre: **{user_text}**\n\n"
            "A. Opción 1\n"
            "B. Opción 2\n"
            "C. Opción 3\n"
            "D. Opción 4\n\n"
            "Respóndeme con la letra que elijas y luego puedo explicarte por qué sería correcta o incorrecta."
        )

    return (
        f"**Explicación para {exam}:**\n\n"
        f"Has preguntado por: **{user_text}**\n\n"
        "1. Qué es\n"
        "2. Para qué sirve\n"
        "3. Ejemplo práctico\n"
        "4. Cómo podría aparecer en examen\n\n"
        "Esta es una demo local para enseñarte la estructura del agente."
    )

# ----- Input del usuario -----
prompt = st.chat_input("Escribe una duda, por ejemplo: ¿Qué es Azure RBAC?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    answer = local_response(prompt, st.session_state.exam, st.session_state.mode)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)