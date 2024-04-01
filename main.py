import os

import streamlit as st
from streamlit_option_menu import option_menu

from PIL import Image

from teja_utility import (load_gemini_pro_model,
                          gemini_pro_vision_response,
                          embedding_model_response,
                          gemini_pro_response)


working_directory = os.path.dirname(os.path.abspath(__file__))

# setting up the page configuration
st.set_page_config(
    page_title="TEJA AI....",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:

    selected = option_menu(menu_title="Teja AI",
            options=["ChatBot","Image Captioning","Embed Text","Ask Me Anything"],
             menu_icon='robot', icons=['chat-dots-fill','image-fill','textarea-t','patch-question-fill'],
             default_index=0)

# function to translate role b/w gemini-pro and streamlit  terminology
def  tranlate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if selected == "ChatBot":

    model = load_gemini_pro_model()

    # Initialize chat session in streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # streamlit page title

    st.title("🤖 Chatbot")

    # display chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(tranlate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # input field for user's message
    user_prompt = st.chat_input(" Ask Teja-Pro.......")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # display teja pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


# Image captioning
if selected == "Image Captioning":

    # title
    st.title("📷 snap narrate")

    uploaded_image=st.file_uploader("Upload an image.....",type=["jpeg","jpg","png"])
    default_prompt = st.text_input("what you want from this image....")

    if st.button("Generate Caption "):
        image = Image.open(uploaded_image)

        col1, col2= st.columns(2)

        with col1:
            resized_image=image.resize((800, 500))
            st.image(resized_image)

        #getting the response from gemini-pro-vision model
        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)


if selected == "Embed Text":

    st.title("🔡Embed Text")

    #input text box
    input_text = st.text_area(label="", placeholder="Enter the text to get the embeddings...")

    if st.button("Get embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)

# question-answering page
if selected == "Ask Me Anything":

    st.title("❔Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label="", placeholder="Ask Teja-Pro.....")

    if st.button("Get an answer"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)

