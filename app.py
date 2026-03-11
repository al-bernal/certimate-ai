import os
import re
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# =========================
# CARGA DE ENTORNO
# =========================
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================
st.set_page_config(
    page_title="CertiMate AI",
    page_icon="📘",
    layout="centered"
)

# =========================
# CLIENTE OPENAI
# =========================
client = None
if api_key:
    client = OpenAI(api_key=api_key)

# =========================
# ESTADO DE SESIÓN
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola, soy CertiMate AI. Puedo ayudarte a estudiar certificaciones cloud y AI. "
                "Usa el modo Explicación, Resumen o Quiz."
            ),
        }
    ]

if "exam" not in st.session_state:
    st.session_state.exam = "AZ-104"

if "mode" not in st.session_state:
    st.session_state.mode = "Explicación"

if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False

if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""

if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = ""

if "quiz_options" not in st.session_state:
    st.session_state.quiz_options = ""

if "quiz_correct_answer" not in st.session_state:
    st.session_state.quiz_correct_answer = ""

if "quiz_explanation" not in st.session_state:
    st.session_state.quiz_explanation = ""

if "quiz_waiting_next" not in st.session_state:
    st.session_state.quiz_waiting_next = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0


# =========================
# FUNCIONES DE RESET
# =========================
def reset_quiz_state() -> None:
    st.session_state.quiz_active = False
    st.session_state.quiz_topic = ""
    st.session_state.quiz_question = ""
    st.session_state.quiz_options = ""
    st.session_state.quiz_correct_answer = ""
    st.session_state.quiz_explanation = ""
    st.session_state.quiz_waiting_next = False


def reset_quiz_score() -> None:
    st.session_state.quiz_score = 0
    st.session_state.quiz_total = 0


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("⚙️ Configuración")

    exams = ["AZ-104", "AI-102", "AWS AI Practitioner", "AWS ML Specialty"]
    modes = ["Explicación", "Resumen", "Quiz"]

    st.session_state.exam = st.selectbox(
        "Certificación",
        exams,
        index=exams.index(st.session_state.exam),
    )

    st.session_state.mode = st.selectbox(
        "Modo",
        modes,
        index=modes.index(st.session_state.mode),
    )

    st.markdown("---")

    st.markdown("### 📊 Marcador del Quiz")
    st.write(f"**Puntuación:** {st.session_state.quiz_score} / {st.session_state.quiz_total}")

    if st.session_state.quiz_total > 0:
        percentage = int((st.session_state.quiz_score / st.session_state.quiz_total) * 100)
        st.progress(percentage)
        st.caption(f"Acierto actual: {percentage}%")
    else:
        st.caption("Todavía no has respondido preguntas.")

    if st.button("🔄 Reiniciar puntuación"):
        reset_quiz_score()
        st.rerun()

    st.markdown("---")
    st.markdown("**Ideas para probar**")
    st.caption("En Quiz, escribe un tema como: Storage Accounts, Azure RBAC, Amazon Lex...")

    if st.button("🗑️ Borrar conversación"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversación reiniciada. ¿Qué tema quieres estudiar ahora?",
            }
        ]
        reset_quiz_state()
        st.rerun()


# =========================
# UI PRINCIPAL
# =========================
st.title("📘 CertiMate AI")
st.caption("Asistente para estudiar certificaciones cloud y AI con explicación, resumen y quiz interactivo")

if not api_key:
    st.warning(
        "No se ha detectado OPENAI_API_KEY en el archivo .env. "
        "Añádela para usar respuestas reales con IA."
    )

# -------- Temas rápidos --------
st.markdown("### 🚀 Temas rápidos")
col1, col2, col3, col4 = st.columns(4)

quick_prompt = None

if col1.button("Azure RBAC"):
    quick_prompt = "Azure RBAC"

if col2.button("Storage Accounts"):
    quick_prompt = "Storage Accounts"

if col3.button("Azure Policy"):
    quick_prompt = "Azure Policy"

if col4.button("Amazon Lex"):
    quick_prompt = "Amazon Lex"

st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# PROMPTS
# =========================
def get_system_prompt(exam: str, mode: str) -> str:
    return f"""
Eres un asistente de estudio especializado en certificaciones cloud y AI.
La certificación actual del usuario es: {exam}.
El modo actual es: {mode}.

Responde siempre en español.
Sé claro, didáctico y estructurado.
No inventes información si no estás seguro.
Adapta la dificultad a una persona que está estudiando certificaciones técnicas.
""".strip()


def get_ai_response(user_text: str, exam: str, mode: str) -> str:
    if client is None:
        return "Error: falta configurar OPENAI_API_KEY en el archivo .env."

    if mode == "Explicación":
        user_prompt = f"""
Explica este concepto para la certificación {exam}: {user_text}

Quiero esta estructura:
1. Qué es
2. Para qué sirve
3. Ejemplo práctico
4. Cómo podría aparecer en examen
""".strip()

    elif mode == "Resumen":
        user_prompt = f"""
Haz un resumen del siguiente tema para la certificación {exam}: {user_text}

Quiero esta estructura:
- Definición breve
- Cuándo se usa
- Punto clave para examen
- Error común
""".strip()

    else:
        user_prompt = user_text

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": get_system_prompt(exam, mode)},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.output_text.strip()


# =========================
# QUIZ
# =========================
def parse_quiz_response(text: str):
    """
    Espera un formato como:
    Pregunta: ...
    A) ...
    B) ...
    C) ...
    D) ...
    Respuesta correcta: B
    Explicación: ...
    """

    question_match = re.search(
        r"Pregunta\s*:\s*(.+?)(?=\nA[\)\.])",
        text,
        re.DOTALL | re.IGNORECASE
    )

    options_match = re.search(
        r"(A[\)\.].*?\nB[\)\.].*?\nC[\)\.].*?\nD[\)\.].*?)(?=\nRespuesta correcta:|\Z)",
        text,
        re.DOTALL | re.IGNORECASE
    )

    answer_match = re.search(
        r"Respuesta correcta\s*:\s*([A-D])",
        text,
        re.IGNORECASE
    )

    explanation_match = re.search(
        r"Explicación\s*:\s*(.+)$",
        text,
        re.DOTALL | re.IGNORECASE
    )

    question = question_match.group(1).strip() if question_match else "No se pudo extraer la pregunta."
    options = options_match.group(1).strip() if options_match else "A) Opción A\nB) Opción B\nC) Opción C\nD) Opción D"
    correct_answer = answer_match.group(1).upper() if answer_match else "A"
    explanation = explanation_match.group(1).strip() if explanation_match else "No se pudo extraer la explicación."

    return question, options, correct_answer, explanation


def generate_quiz_question(topic: str, exam: str) -> str:
    if client is None:
        return "Error: falta configurar OPENAI_API_KEY en el archivo .env."

    quiz_prompt = f"""
Crea 1 pregunta tipo test sobre el tema "{topic}" para la certificación {exam}.

Requisitos:
- La pregunta debe ser realista y útil para examen.
- Debe tener 4 opciones.
- Solo 1 opción debe ser correcta.
- Las opciones incorrectas deben ser plausibles.
- No repitas la misma opción con otras palabras.

Devuélvelo EXACTAMENTE con este formato:

Pregunta: ...
A) ...
B) ...
C) ...
D) ...
Respuesta correcta: A
Explicación: ...

No añadas texto extra antes ni después.
""".strip()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": get_system_prompt(exam, "Quiz")},
            {"role": "user", "content": quiz_prompt},
        ],
    )

    raw_text = response.output_text.strip()

    question, options, correct_answer, explanation = parse_quiz_response(raw_text)

    st.session_state.quiz_active = True
    st.session_state.quiz_topic = topic
    st.session_state.quiz_question = question
    st.session_state.quiz_options = options
    st.session_state.quiz_correct_answer = correct_answer
    st.session_state.quiz_explanation = explanation
    st.session_state.quiz_waiting_next = False

    return (
        f"**Quiz de práctica para {exam}**\n\n"
        f"**Tema:** {topic}\n\n"
        f"**Pregunta:** {question}\n\n"
        f"{options}\n\n"
        "Respóndeme con **A, B, C o D**."
    )


def check_quiz_answer(user_text: str) -> str:
    answer = user_text.strip().upper()
    correct = st.session_state.quiz_correct_answer
    explanation = st.session_state.quiz_explanation
    topic = st.session_state.quiz_topic

    st.session_state.quiz_total += 1

    if answer == correct:
        st.session_state.quiz_score += 1
        result = "✅ **Correcto**"
    else:
        result = f"❌ **Incorrecto**\n\nLa respuesta correcta era **{correct}**."

    st.session_state.quiz_active = False
    st.session_state.quiz_waiting_next = True

    return (
        f"{result}\n\n"
        f"**Explicación:** {explanation}\n\n"
        f"**Puntuación actual:** {st.session_state.quiz_score} / {st.session_state.quiz_total}\n\n"
        f"Si quieres otra pregunta sobre **{topic}**, escribe **si**, **sí**, **otra** o **siguiente**."
    )


def wants_next_question(user_text: str) -> bool:
    normalized = user_text.strip().lower()
    return normalized in ["si", "sí", "otra", "siguiente", "otra pregunta"]


# =========================
# PROCESAMIENTO DE INPUT
# =========================
def process_prompt(prompt_text: str):
    st.session_state.messages.append({"role": "user", "content": prompt_text})

    with st.chat_message("user"):
        st.markdown(prompt_text)

    try:
        # QUIZ: si hay pregunta activa, espera A/B/C/D
        if st.session_state.mode == "Quiz" and st.session_state.quiz_active:
            if prompt_text.strip().upper() in ["A", "B", "C", "D"]:
                answer = check_quiz_answer(prompt_text)
            else:
                answer = "Estoy esperando una respuesta del quiz. Contéstame con **A, B, C o D**."

        # QUIZ: si acaba de terminar una pregunta y el usuario quiere otra
        elif st.session_state.mode == "Quiz" and st.session_state.quiz_waiting_next and wants_next_question(prompt_text):
            answer = generate_quiz_question(st.session_state.quiz_topic, st.session_state.exam)

        # QUIZ: si está esperando otra pero el usuario mete un tema nuevo
        elif st.session_state.mode == "Quiz" and st.session_state.quiz_waiting_next:
            answer = generate_quiz_question(prompt_text, st.session_state.exam)

        # QUIZ: primer tema nuevo
        elif st.session_state.mode == "Quiz":
            answer = generate_quiz_question(prompt_text, st.session_state.exam)

        # OTROS MODOS
        else:
            reset_quiz_state()
            answer = get_ai_response(prompt_text, st.session_state.exam, st.session_state.mode)

    except Exception as e:
        answer = f"Ha ocurrido un error al procesar la solicitud: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)


# -------- Procesar botón rápido --------
if quick_prompt:
    process_prompt(quick_prompt)

# -------- Procesar chat input --------
prompt = st.chat_input("Escribe una duda, por ejemplo: ¿Qué es Azure RBAC?")

if prompt:
    process_prompt(prompt)