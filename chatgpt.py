import streamlit as st
import json
import openai  # For ChatGPT API calls
from openai import OpenAI


# Configure the OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Add your API key to Streamlit secrets
client = OpenAI()

def parse_workflow(json_data):
    # Function to parse and display workflow steps in a user-friendly way
    steps = json_data.get("Steps", [])
    parsed_steps = []
    for step in steps:
        parsed_steps.append({
            "Step ID": step["Id"],
            "Name": step["Name"],
            "Type": step["StepType"],
            "Next Step ID": step.get("NextStepId"),
            "Inputs": step.get("Inputs"),
            "Outputs": step.get("Outputs"),
        })
    return parsed_steps

def get_chatgpt_response(prompt, json_data):
    # Make a call to the ChatGPT API to process the workflow based on user prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-3.5-turbo" depending on your access
        messages=[
            #{"role": "system", "content": "You are an assistant for industrial workflow processing."},
            {"role": "user", "content": f"{prompt}. Here is the JSON data: {json.dumps(json_data)}"}
        ],
        max_tokens=500  # Adjust token count as needed
    )
    return response['choices'][0]['message']['content']

# Streamlit App Layout
st.title("Industrial Workflow Analyzer")

uploaded_file = st.file_uploader("Upload your workflow JSON file", type="json")

if uploaded_file:
    # Load JSON
    workflow_data = json.load(uploaded_file)
    st.write("### Workflow Overview:")
    parsed_steps = parse_workflow(workflow_data)
    st.json(parsed_steps)  # Display parsed workflow steps

    # Prompt-based Interaction with ChatGPT
    prompt = st.text_input("Ask ChatGPT for workflow insights, modifications, or generation suggestions:")
    if st.button("Send to ChatGPT"):
        if prompt:
            try:
                response = get_chatgpt_response(prompt, workflow_data)
                st.write("### ChatGPT Response:")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter a prompt to get a response from ChatGPT.")
