import streamlit as st

from utils.pdf_utils import extract_text_from_pdf
from utils.text_preprocessing import clean_and_chunk
from utils.embeddings import create_embeddings, model
from utils.vector_store import build_faiss_index, search_index
from utils.qa_engine import retrieve_chunks
from utils.answer_engine import build_answer
from utils.summarizer import summarize
from utils.quiz_generator import generate_mcq
from utils.analytics import init_analytics
from utils.intelligence import extract_topics

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Smart Campus Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# LOAD STYLES
# -------------------------------------------------
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------------------------
# CURSOR ANIMATION
# -------------------------------------------------
st.markdown("""
<div class="cursor"></div>
<script>
const cursor = document.querySelector('.cursor');
document.addEventListener('mousemove', e => {
  cursor.style.left = e.clientX + 'px';
  cursor.style.top = e.clientY + 'px';
});
</script>
""", unsafe_allow_html=True)

# -------------------------------------------------
# INIT ANALYTICS
# -------------------------------------------------
init_analytics(st)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("🎓 Smart Campus Assistant")
menu = st.sidebar.radio(
    "Navigation",
    ["Upload", "Ask", "Summarize", "Quiz", "Insights"]
)

st.markdown("<div class='main-card'>", unsafe_allow_html=True)

# =================================================
# 📤 UPLOAD DOCUMENTS
# =================================================
if menu == "Upload":
    st.header("📤 Upload Study Materials")

    files = st.file_uploader(
        "Upload text-based PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if files:
        with st.spinner("Processing documents..."):
            pages = []
            for f in files:
                extracted = extract_text_from_pdf(f)
                pages.extend(extracted)

            chunks = clean_and_chunk(pages)

            if len(chunks) == 0:
                st.error("❌ No readable text found. Please upload text-based PDFs.")
            else:
                embeddings = create_embeddings(chunks)

                if embeddings.shape[0] == 0:
                    st.error("❌ Failed to generate embeddings. Check document content.")
                else:
                    index = build_faiss_index(embeddings)

                    st.session_state.chunks = chunks
                    st.session_state.embeddings = embeddings
                    st.session_state.index = index

                    st.success("✅ Documents processed and indexed successfully!")

# =================================================
# 💬 ASK QUESTIONS
# =================================================
elif menu == "Ask":
    st.header("💬 Ask Your Notes")

    if "index" not in st.session_state:
        st.warning("⚠️ Please upload documents first.")
    else:
        question = st.text_input("Enter your question")

        if question:
            st.session_state.questions += 1

            q_emb = model.encode([question])

            idxs, _ = search_index(
                st.session_state.index,
                q_emb,
                k=5
            )

            top_chunks = retrieve_chunks(
                idxs[0],   # FAISS returns 2D array
                st.session_state.chunks
            )

            if not top_chunks:
                st.warning("No relevant content found.")
            else:
                answer, confidence, sources = build_answer(
                    question,
                    top_chunks,
                    model
                )

                st.subheader("📌 Answer")
                st.write(answer)

                st.metric("Confidence Score", confidence)

                with st.expander("📚 Sources Used"):
                    for s in sources:
                        st.caption(f"{s['source']} | Page {s['page']}")

# =================================================
# 📄 SUMMARIZATION
# =================================================
elif menu == "Summarize":
    st.header("📄 Document Summarization")

    if "chunks" not in st.session_state:
        st.warning("⚠️ Please upload documents first.")
    else:
        mode = st.selectbox("Summary Type", ["Short", "Detailed"])
        summary = summarize(st.session_state.chunks, mode)

        for s in summary:
            st.write("•", s)

# =================================================
# 📝 QUIZ
# =================================================
elif menu == "Quiz":
    st.header("📝 Practice Quiz")

    if "chunks" not in st.session_state:
        st.warning("⚠️ Please upload documents first.")
    else:
        quiz = generate_mcq(st.session_state.chunks)
        score = 0

        for i, q in enumerate(quiz):
            st.subheader(f"Q{i + 1}")
            ans = st.radio(
                q["question"],
                q["options"],
                key=f"quiz_{i}"
            )
            if ans == q["answer"]:
                score += 1

        if st.button("Submit Quiz"):
            st.session_state.quiz_score.append(score)
            st.success(f"🎯 Score: {score}/{len(quiz)}")

# =================================================
# 📊 INSIGHTS
# =================================================
elif menu == "Insights":
    st.header("📊 Learning Insights")

    st.metric("Questions Asked", st.session_state.questions)

    if st.session_state.quiz_score:
        st.metric(
            "Last Quiz Score",
            st.session_state.quiz_score[-1]
        )

    if "chunks" in st.session_state:
        topics = extract_topics(st.session_state.chunks)

        st.subheader("📌 Key Topics")
        for t, c in topics:
            st.write(f"• {t} ({c})")

st.markdown("</div>", unsafe_allow_html=True)
