import streamlit as st
import pandas as pd
import os
from PIL import Image

from handlers.csv_handler import (
    summarize_dataframe,
    generate_code_from_gpt,
    execute_generated_code,
    ask_gpt_to_explain_result
)
from handlers.rag_handler import load_and_embed_text
from handlers.followup_handler import generate_followup_answer
from handlers.export_pdf import export_chat_to_pdf

# Page setup
st.set_page_config(
    page_title="InsightPilot",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🧭 InsightPilot – Chat with Your Data")

# Session state defaults
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("domain", "General")
st.session_state.setdefault("use_rag", False)
st.session_state.setdefault("latest_plot", None)
st.session_state.setdefault("latest_result", None)

# Sidebar
st.sidebar.markdown("### ⚙️ Options")
st.session_state.domain = st.sidebar.selectbox("Domain", ["General", "Finance", "Healthcare"])
st.session_state.use_rag = st.sidebar.toggle("Enable RAG")
show_code = st.sidebar.toggle("Show Generated Code", value=True)

if st.sidebar.button("📝 Export Session to PDF"):
    if st.session_state.chat_history:
        filename = export_chat_to_pdf(st.session_state.chat_history)
        with open(filename, "rb") as f:
            st.sidebar.download_button("⬇️ Download PDF", f, file_name=filename)
    else:
        st.sidebar.info("No chat to export yet.")

# File upload
uploaded_file = st.file_uploader("📁 Upload your CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    summary = summarize_dataframe(df)

    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    # Preload RAG index
    if st.session_state.use_rag and not os.path.exists("faiss_index/index.faiss"):
        with st.spinner("📚 Indexing knowledge base..."):
            domain_file = f"rag_knowledge/{st.session_state.domain.lower()}.txt"
            if os.path.exists(domain_file):
                load_and_embed_text(domain_file)
            else:
                st.warning("⚠️ No knowledge file found for this domain.")

    # Chat interface
    for entry in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(entry["question"])
        with st.chat_message("assistant"):
            st.markdown(entry["answer"])
            if entry.get("result") and not entry.get("plot"):
                st.markdown(f"**📈 Result:** {entry['result']}")
            if entry.get("code"):
                with st.expander("📜 Generated Code"):
                    st.code(entry["code"], language="python")
            if entry.get("plot") and os.path.exists(entry["plot"]):
                st.image(Image.open(entry["plot"]))

    # Input box at bottom
    if prompt := st.chat_input("Ask a question about your data"):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            code = None
            answer = None
            plot_path = None
            result = None

            try:
                if st.session_state.use_rag:
                    answer = generate_followup_answer(prompt)
                    result = None
                    plot_path = None
                    st.session_state.latest_result = None
                else:
                    code = generate_code_from_gpt(summary, prompt, st.session_state.domain)
                    result, plot_path = execute_generated_code(code, df)
                    answer = ask_gpt_to_explain_result(result, prompt, st.session_state.domain)
                    st.session_state.latest_result = result if not plot_path else None

            except Exception as e:
                answer = f"⚠️ Error: {e}"

            st.session_state.chat_history.append({
                "question": prompt,
                "answer": answer,
                "code": code if show_code else None,
                "plot": plot_path,
                "result": result if not plot_path else None
            })

            st.markdown(answer)
            if result and not plot_path:
                st.markdown(f"**📈 Result:** {result}")
            if code and show_code:
                with st.expander("📜 Generated Code"):
                    st.code(code, language="python")
            if plot_path and os.path.exists(plot_path):
                st.image(Image.open(plot_path))

        st.rerun()
