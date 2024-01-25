from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import pdf2image
import openai
import io
import base64
from openai import OpenAI


# Load OpenAI API key from environment variable
load_dotenv()
client = OpenAI(api_key="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")


# Function to get OpenAI response
def get_openai_response(input_text, prompt):
    conversation = [
        {"role": "system", "content": "You are a technical recruiter ats."},
        {"role": "user", "content": input_text},
        {"role": "assistant", "content": prompt},
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.7,
        max_tokens=256,
    )
    return response.choices[0].message.content

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(
            uploaded_file.read(), poppler_path=r"C:\Program Files\poppler\poppler-23.11.0\Library\bin"
        )
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode(),
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="ATS Checker", page_icon=":bar_chart:", layout="wide")


st.title("Applicant Tracking System")


input_text = st.text_area("Job Description:", key="input")

uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])


if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

submit1 = st.button("Tell me about Resume")
submit2 = st.button("How can I improve my skill")
submit3 = st.button("What are the keywords that are missing")
submit4 = st.button("Percentage Match")


input_prompt1 = "As an  Technical Recruiter and HR Manager, your role is to thoroughly analyze the candidate's resume. Provide a detailed overview, highlighting key qualifications, experiences, and skills in the form of a list."

input_prompt2 = "In your capacity as a seasoned Technical Recruiter and HR Manager, your task is to offer constructive guidance to the candidate on enhancing their skill set. Identify areas for improvement and provide actionable recommendations to help the candidate strengthen their skills, making them more competitive in the targeted industry. Just return a list of areas to improve, in short."

input_prompt3 = "As an expert Technical Recruiter and HR Manager, your responsibility is to identify missing keywords in the candidate's resume that are crucial for the targeted job. Evaluate the resume's alignment with industry-relevant terms and suggest key terms that should be included to enhance visibility and resonance with potential employers. Return a list of matched skills as well as missing skills."

input_prompt4 = "Analyze the candidate's resume in comparison to the provided job description and provide a percentage match. Consider the qualifications, skills, and experiences mentioned in both the job description and the resume."

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, input_prompt1)
        st.subheader("Resume Analysis:")
        st.write(response)

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, input_prompt2)
        st.subheader("Skill Improvement Recommendations:")
        st.write(response)

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, input_prompt3)
        st.subheader("Keyword Suggestions:")
        st.write(response)

if submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, input_prompt4)
        st.subheader("Percentage Match Analysis:")
        st.write(response)
