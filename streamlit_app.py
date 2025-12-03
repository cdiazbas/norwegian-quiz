import streamlit as st
import pandas as pd
import random

# Page configuration
st.set_page_config(
    page_title="Norwegian B2 Quiz",
    page_icon="🇳🇴",
    layout="centered"
)

# Custom CSS for minimalist, modern design
st.markdown("""
<style>
    .main { padding-top: 0; }
    /* Streamlit main block container padding for cleaner mobile spacing */
    .stMainBlockContainer {
        padding-left: 0.5rem; /* minimal side margin */
        padding-right: 0.5rem; /* minimal side margin */
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    
    .question-card {
        background-color: #F5F7FA; /* soft neutral */
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #007C73; /* teal accent */
    }
    
    .question-text {
        font-size: 1.2rem;
        font-weight: 500;
        color: #1F2937; /* high-contrast dark */
        margin: 0;
    }
    
    .success-box {
        background-color: #DDF3EA; /* gentle success bg */
        border-left: 4px solid #2E7D32; /* success border */
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .success-box p {
        color: #1B5E20; /* success text */
        margin: 0;
        font-weight: 500;
    }
    
    .error-box {
        background-color: #FBE9E7; /* gentle error bg */
        border-left: 4px solid #D84315; /* error border */
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .error-box p {
        color: #7F2A1D; /* error text */
        margin: 0;
        font-weight: 500;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #007C73; /* teal accent */
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        transition: background-color 0.3s;
        margin: 0.25rem 0;
    }
    
    .stButton>button:hover {
        background-color: #006861; /* teal hover */
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #007C73; /* accent for metric value */
    }
    
    .score-container {
        background-color: #F5F7FA;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
    }

    /* Compact metrics at top */
    .metrics-wrap {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        margin-bottom: 0.25rem;
        flex-wrap: wrap;
    }
    .metric-chip {
        background: #E6F3F1; /* tinted chip bg */
        color: #007C73; /* accent chip text */
        border-radius: 12px;
        padding: 0.35rem 0.6rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Mobile tweaks */
    @media (max-width: 480px) {
        .main { padding-top: 0; }
        .question-card { padding: 0.9rem; margin: 0.4rem 0; }
        .question-text { font-size: 1.05rem; }
        .stButton>button { padding: 0.8rem 1rem; font-size: 1rem; }
        div[data-testid="stMetricValue"] { font-size: 1.25rem; }
        .metrics-wrap { gap: 0.4rem; }
        .metric-chip { font-size: 0.8rem; padding: 0.3rem 0.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Load questions data
@st.cache_data
def load_questions():
    df = pd.read_csv('data/questions.csv')
    return df

# Initialize session state
def init_session_state():
    if 'questions_df' not in st.session_state:
        st.session_state.questions_df = load_questions()
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'correct_count' not in st.session_state:
        st.session_state.correct_count = 0
    if 'total_count' not in st.session_state:
        st.session_state.total_count = 0
    if 'selected_answer' not in st.session_state:
        st.session_state.selected_answer = None
    if 'evaluated' not in st.session_state:
        st.session_state.evaluated = False
    # No category filtering in mobile-first UI

# Get new random question
def get_new_question():
    df = st.session_state.questions_df
    
    if len(df) > 0:
        st.session_state.current_question = df.sample(n=1).iloc[0].to_dict()
        st.session_state.selected_answer = None
        st.session_state.evaluated = False
        st.session_state.total_count += 1
    else:
        st.session_state.current_question = None

# Initialize
init_session_state()

# Header
st.title("🇳🇴 Norwegian B2 Quiz")

# Top controls: compact metrics + new question button
colA, colB = st.columns([2, 1])
with colA:
    correct = st.session_state.correct_count
    total = st.session_state.total_count
    accuracy = (correct / total * 100) if total > 0 else None
    summary_text = f"Correctas {correct}/{total}" + (f" · {accuracy:.1f}%" if accuracy is not None else "")
    st.markdown(
        f"<div class=\"metrics-wrap\"><span class=\"metric-chip\">{summary_text}</span></div>",
        unsafe_allow_html=True
    )
with colB:
    if st.button("📝 Nueva Pregunta", use_container_width=True):
        get_new_question()

# Sidebar removed for mobile-first UI

# Main content
if st.session_state.current_question is None:
    st.info("👆 Haz clic en 'Nueva Pregunta' para comenzar")
else:
    q = st.session_state.current_question
    
    # Question
    st.markdown(f'<div class="question-card"><p class="question-text">{q["pregunta"]}</p></div>', unsafe_allow_html=True)
    
    # Options
    options = [q['opcion_1'], q['opcion_2'], q['opcion_3']]
    
    st.session_state.selected_answer = st.radio(
        "Selecciona tu respuesta:",
        options,
        index=options.index(st.session_state.selected_answer) if st.session_state.selected_answer in options else 0,
        key=f"radio_{st.session_state.total_count}"
    )
    
    # Evaluate button
    if st.button("✓ Evaluar", use_container_width=True):
        st.session_state.evaluated = True
        
        # Check which option was selected
        selected_index = options.index(st.session_state.selected_answer) + 1
        correct_index = int(q['respuesta_correcta'])
        
        if selected_index == correct_index:
            st.session_state.correct_count += 1
    
    # Show feedback if evaluated
    if st.session_state.evaluated:
        selected_index = options.index(st.session_state.selected_answer) + 1
        correct_index = int(q['respuesta_correcta'])
        
        if selected_index == correct_index:
            st.markdown(f"""
            <div class="success-box">
                <p>✓ ¡Correcto!</p>
                <p style="margin-top: 0.5rem; font-weight: 400;">{q['explicacion_1']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            explanation_key = f'explicacion_{selected_index}'
            st.markdown(f"""
            <div class="error-box">
                <p>✗ Incorrecto</p>
                <p style="margin-top: 0.5rem; font-weight: 400;">{q[explanation_key]}</p>
                <p style="margin-top: 0.8rem; font-weight: 400; border-top: 1px solid #f5c6cb; padding-top: 0.8rem;">
                    <strong>Respuesta correcta:</strong> {q[f'opcion_{correct_index}']}<br>
                    <em>{q['explicacion_1']}</em>
                </p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #6c757d; font-size: 0.9rem;">Practica y aprende noruego a tu ritmo</p>',
    unsafe_allow_html=True
)
