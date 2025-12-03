# 🇳🇴 Norwegian B2 Quiz

A minimalist, mobile‑first Streamlit app to practice Norwegian (B2 level). It shows a random question with three options, provides immediate feedback, and tracks your score.

## Features
- Single‑column, phone‑friendly UI (no sidebar)
- Compact metrics: `Correctas X/Total Y · %`
- Modern neutral + teal color palette
- Instant feedback with clear success/error boxes

## Quick Start
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open the local URL shown by Streamlit (usually `http://localhost:8501`).

## Data
- Questions are loaded from `data/questions.csv`.
- Expected columns: `categoria, pregunta, opcion_1, opcion_2, opcion_3, explicacion_1, explicacion_2, explicacion_3, respuesta_correcta`.

## Notes
- The UI is optimized for mobile: minimal margins, top‑aligned content, large touch targets.
- Category filtering was removed for simplicity; a random question is shown each time.

## Deploy
- You can deploy on Streamlit Community Cloud or any environment that supports Python.
- Keep `requirements.txt` up to date to ensure smooth deployment.
