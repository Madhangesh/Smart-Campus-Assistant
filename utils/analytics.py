def init_analytics(st):
    if "questions" not in st.session_state:
        st.session_state.questions = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = []
