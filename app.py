import streamlit as st
from huggingface_hub import InferenceClient

# Your Hugging Face API key (replace this with your actual key)
api_key = "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"

# Initialize the Inference Client with the API key
client = InferenceClient(token=api_key)

# Custom CSS for styling the app
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(315deg, #4f2991 3%, #7dc4ff 38%, #36cfcc 68%, #a92ed3 98%);
        animation: gradient 15s ease infinite;
        background-size: 400% 400%;
        color: white;
    }

    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
    }

    .stSelectbox, .stTextInput {
        background-color: rgba(65, 105, 225, 0.8);
        border-radius: 5px;
        border: 1px solid #ccc;
    }

    .stButton {
        background-color: #36cfcc;
        color: white;
        border-radius: 5px;
    }

    .stButton:hover {
        background-color: #28b8b0;
    }

    .stMarkdown {
        font-size: 1.2em; /* Adjust this value for model's response */
    }
    </style>
""", unsafe_allow_html=True)

# Set the title and caption for the app
st.title("AI Tourist Guide")
st.markdown('<span style="font-size: 1.2em; font-weight: bold;">Your personal companion and friend!</span>', unsafe_allow_html=True)

# Model selection
models = ['distilgpt2', 'DialoGPT-small', 't5-small']
selected_model = st.selectbox('Select Model', models)

# Query input box
user_query = st.text_input('Enter your query')

# Display the selected model and author name with enhanced formatting
author_name = '**Zoha Zahid & Javeria Shah**'
st.markdown(f"### Created By: {author_name}")

model_mapping = {
    'distilgpt2': "meta-llama/Llama-3.2-1B-Instruct",
    'DialoGPT-small': "google/gemma-1.1-2b-it",
    't5-small': "tiiuae/falcon-7b-instruct"
}
selected_model_id = model_mapping.get(selected_model, "meta-llama/Llama-3.2-1B-Instruct")

def is_travel_related(query):
    travel_keywords = [
        "travel", "tourism", "vacation", "trip", "holiday", "destination",
        "hotel", "flight", "tourist", "guide", "landmark", "attraction",
        "itinerary", "sightseeing", "adventure", "culture", "explore"
    ]
    return any(keyword in query.lower() for keyword in travel_keywords)

# Handle user input and generate a response
if user_query:
    if is_travel_related(user_query):
        try:
            response = client.chat.completions.create(
                model=selected_model_id,
                messages=[{"role": "user", "content": user_query}],
                max_tokens=600
            )
            # Extract model's response
            model_reply = response["choices"][0]["message"]["content"]
            st.markdown(f"### **{selected_model}'s Response:**", unsafe_allow_html=True)
            st.markdown(f"<div class='stMarkdown'>{model_reply}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.markdown("### I cannot answer this. Please ask a travel or tourism-related question.", unsafe_allow_html=True)
