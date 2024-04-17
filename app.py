import os
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key = os.getenv("API_Key"))

def get_gemini_response(query, pdf_content, prompt):
    
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([query, pdf_content[0], prompt])
    
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        image=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=image[0]
        first_page = image[0]
        
        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr, format = 'JPEG')
        image_byte_arr = image_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(image_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
st.set_page_config(page_title = "Application Tracking System")
st.header("ATS System")
input_text = st.text_area("Job Description: ", key = "input")
uploaded_file = st.file_uploader("Upload Your Resume (PDF): ", type = ['pdf'])

if uploaded_file is not None:
    st.write("File Uploaded Successfully")

submit1 = st.button("Summary of your resume")
submit2 = st.button("Percentage Match")
submit3 = st.button("How can I improvise my skills ?")

input_prompt1 = """
 You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
 your task is to highlight and summarize all the things mentioned in the resume in image format.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume provided in image provided against the provided job description in the prompt. give me the percentage of match if the resume in image matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt3 = """
 You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume provided in image provided against the provided job description in the prompt. give me the ways to improvise the skills mentioned in resume so that it matches the job description.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

