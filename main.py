import os
import google.generativeai as genai
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("ERROR: API key is missing! Set 'GOOGLE_GEMINI_API_KEY' in your environment.")

# Configure Google Gemini API
genai.configure(api_key=API_KEY)

# Get available models
available_models = [model.name for model in genai.list_models()]
print(f"Available models: {available_models}")

# Select a valid model (prefer latest Gemini model if available)
MODEL_NAME = "models/gemini-1.5-pro-latest" if "models/gemini-1.5-pro-latest" in available_models else available_models[0]
print(f"Using model: {MODEL_NAME}")

# Load the model
model = genai.GenerativeModel(MODEL_NAME)

# Define story generation function
def generate_story(prompt):
    try:
        response = model.generate_content(
            f"{prompt}\n\nWrite this in simple, easy-to-understand language, suitable for all readers."
        )
        return response.text.strip() if response.text else "No response generated."
    except Exception as e:
        return f"Error: {str(e)}"


# Gradio UI Setup
interface = gr.Interface(
    fn=generate_story,
    inputs=gr.Textbox(label="Enter a Story Prompt"),
    outputs=gr.Textbox(label="Generated Story"),
    title="AI Story Generator",
    description="Generate dynamic stories with AI based on your input.",
)

if __name__ == "__main__":
    interface.launch()
