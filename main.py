import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

def save_to_db(question,answer):

    conn = sqlite3.connect("research.db")
    cursor = conn.cursor()

    question_date = (question,answer)

    cursor.execute("""INSERT INTO queries (question,answer)
                         VALUEs(?,?)""",question_date)


    conn.commit()
    conn.close()

def upload_to_gemini(streamlit_file):
    temp_path =streamlit_file.name
    with open(temp_path, "wb") as f:
        f.write(streamlit_file.getbuffer())
    
    gemini_file = client.files.upload(
        file=temp_path,
        config={
            "display_name": streamlit_file.name,
            "mime_type" : streamlit_file.type
        }
    )

    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    return gemini_file

def get_gemini_response(prompt,gemini_file=None):
    if gemini_file != None:
        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents = [
                prompt,
                {
                "fileData": {
                    "fileUri": gemini_file.uri,
                    "mimeType": gemini_file.mime_type
                }
            }
            ]       
        )
    else:
        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents = [prompt]       
        )

    return response.text

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

st.title("Insight buddy. ask me any question!")

question = st.text_input("What would you like to learn about?")
uploaded_file = st.file_uploader("Upload a file", type=["txt","pdf"])
if st.button("Ask"):
    if uploaded_file != None:
        gemini_file = upload_to_gemini(uploaded_file)
    else:
        gemini_file = None
    answer = get_gemini_response(question,gemini_file)
    st.write(answer)
    save_to_db(question,answer)
    