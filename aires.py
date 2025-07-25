import streamlit as st
import fitz  # PyMuPDF
import openai

# Load OpenAI API key from secrets or define it here
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "YOUR_OPENAI_API_KEY"

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Analyze resume using OpenAI
def analyze_resume(resume_text, job_role, weak_areas):
    prompt = f"""
You are an AI resume reviewer. A user is applying for the role of "{job_role}".
Their resume content is below:

--- Resume Start ---
{resume_text}
--- Resume End ---

They mentioned their weak areas are: {weak_areas}.

Evaluate the resume for this role. Do the following:
1. Estimate an ATS match score out of 100%
2. Highlight key skills or phrases missing
3. Suggest how the resume can be improved (structure, language, sections)
4. Recommend 2-3 free resources for each weak area mentioned

Format your answer in markdown.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=800
    )
    return response.choices[0].message["content"]

# Streamlit UI
st.set_page_config(page_title="AI Resume Scanner", layout="centered")
st.title("📄 AI-Powered Resume Scanner")

with st.form("resume_form"):
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    job_role = st.text_input("What role are you applying for?")
    weak_areas = st.text_input("What are the areas you feel you're lacking in? (comma-separated)")
    submit = st.form_submit_button("Analyze Resume")

if submit and uploaded_file:
    with st.spinner("Extracting and analyzing resume..."):
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume(resume_text, job_role, weak_areas)
            st.markdown("### 📝 AI Feedback")
            st.markdown(result)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
else:
    st.info("Please upload a PDF resume and fill in the fields to begin.")

