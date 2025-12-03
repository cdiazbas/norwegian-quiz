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
    .main {
        padding-top: 2rem;
    }
    
    .category-badge {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .question-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 4px solid #1976d2;
    }
    
    .question-text {
        font-size: 1.2rem;
        font-weight: 500;
        color: #212529;
        margin: 0;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #4CAF50;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box p {
        color: #155724;
        margin: 0;
        font-weight: 500;
    }
    
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #f44336;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-box p {
        color: #721c24;
        margin: 0;
        font-weight: 500;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #1976d2;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: background-color 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1565c0;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #1976d2;
    }
    
    .score-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
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
    if 'category_filter' not in st.session_state:
        st.session_state.category_filter = "Todas"

# Get new random question
def get_new_question():
    df = st.session_state.questions_df
    
    # Filter by category if not "Todas"
    if st.session_state.category_filter != "Todas":
        df = df[df['categoria'] == st.session_state.category_filter]
    
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
st.markdown("### Practica tu noruego nivel B2")

# Sidebar with controls
with st.sidebar:
    st.markdown("## 📊 Estadísticas")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Correctas", st.session_state.correct_count)
    with col2:
        st.metric("Total", st.session_state.total_count)
    
    if st.session_state.total_count > 0:
        accuracy = (st.session_state.correct_count / st.session_state.total_count) * 100
        st.metric("Precisión", f"{accuracy:.1f}%")
    
    st.markdown("---")
    
    # Category filter
    st.markdown("## 🎯 Filtro")
    categories = ["Todas"] + sorted(st.session_state.questions_df['categoria'].unique().tolist())
    st.session_state.category_filter = st.selectbox(
        "Categoría",
        categories,
        index=categories.index(st.session_state.category_filter)
    )
    
    st.markdown("---")
    
    # New question button
    if st.button("📝 Nueva Pregunta", use_container_width=True):
        get_new_question()

# Main content
if st.session_state.current_question is None:
    st.info("👆 Haz clic en 'Nueva Pregunta' para comenzar")
else:
    q = st.session_state.current_question
    
    # Category badge
    st.markdown(f'<div class="category-badge">{q["categoria"]}</div>', unsafe_allow_html=True)
    
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
