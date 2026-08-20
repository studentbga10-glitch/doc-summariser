import streamlit as st
from google import genai

st.set_page_config(page_title="Document Summariser", layout="centered")
st.title("Document Summariser")
st.markdown("Paste any document, article or report below. Get a structured summary in Traditional Chinese instantly.")

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

def summarise_document(text):
    prompt = f"""
You are a senior business analyst preparing a briefing for executive leadership.
Always respond in Traditional Chinese.

Summarise the following document using this exact structure:

0. 執行摘要 EXECUTIVE SUMMARY
   2 sentences maximum. Written for a busy executive who has 10 seconds to read.
   Must capture: what this is about + the single most important takeaway.

1. 文件概覽 OVERVIEW
   2 to 3 sentences. What is this document about and what is its purpose.

2. 重點摘要 KEY POINTS
   Maximum 5 bullet points. Facts and findings only, no opinions.

3. 待辦事項 ACTION ITEMS
   List specific actions required, who should act, and by when if stated.
   If no action items, write: 本文件不涉及具體待辦事項。

4. 風險評估 RISK ASSESSMENT
   List potential risks identified, rate each as High / Medium / Low.
   If no risks identified, write: 本文件未見明顯風險。

5. 結論 BOTTOM LINE
   1 sentence. The single most important conclusion from this document.

Document:
{text}
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

# Input
text_input = st.text_area(
    "Paste your document here",
    height=300,
    placeholder="Paste any article, report, meeting notes or email here..."
)

col1, col2 = st.columns([1, 4])
with col1:
    run = st.button("Summarise", type="primary")

if run:
    if not text_input.strip():
        st.warning("Please paste some text first.")
    else:
        with st.spinner("Analysing document..."):
            result = summarise_document(text_input)
        st.divider()
        st.markdown(result)
        st.divider()
        st.download_button(
            label="Download Summary",
            data=result,
            file_name="summary.txt",
            mime="text/plain"
        )
