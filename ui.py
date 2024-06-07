import os
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv('API_KEY')
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {api_key}"} # Replace with your API key

def query(payload, max_new_tokens=1000):
    response = requests.post(API_URL, headers=headers, json={"inputs": payload["inputs"], "parameters": {"max_new_tokens": max_new_tokens}})
    return response.json()

# Streamlit UI
st.title("WritAssistant🖊️")

# User input sections
content = st.text_area("Enter your content:", height=100)
fix_instructions = st.text_area("What needs fixing? (e.g., grammar, clarity, tone)", height=50)

# Generate text based on user input
if st.button("Generate"):
    if content.strip() != "" and fix_instructions.strip() != "":
        payload = {"inputs": f"{content}\n** Fix:** {fix_instructions}"}
        output = query(payload)
        generated_text = output[0]['generated_text']

        # Extract and display only the modified content
        split_text = generated_text.split("\n** Fix:** ")
        modified_content = split_text[-1].strip()  # Get last part after the fix instruction
        st.write("Modified Text:")
        st.write(modified_content)
    else:
        error_message = ""
        if content.strip() == "":
            error_message += "Please enter content.\n"
        if fix_instructions.strip() == "":
            error_message += "Please specify what needs fixing."
        st.write(error_message)

