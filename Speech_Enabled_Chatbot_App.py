# Import necessary libraries
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import streamlit as st
import speech_recognition as sr
from PyPDF2 import PdfFileReader
from docx import Document
import docx2txt

# Initialize NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Define a function to transcribe speech into text using the speech recognition algorithm
def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something:")
        audio = r.listen(source)
        print("Audio captured")
        try:
            text = r.recognize_google(audio)
            print("Transcribed text:", text)
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
            return "Sorry, I couldn't understand what you said."
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return "Sorry, I couldn't understand what you said."

# Define a function to read text from a file
def read_file(file):
    file_extension = file.name.split('.')[-1].lower()
    if file_extension == 'txt':
        return file.read().decode("utf-8")
    elif file_extension == 'pdf':
        pdf_file = PdfFileReader(file)
        text = ''
        for page in range(pdf_file.numPages):
            text += pdf_file.getPage(page).extractText()
        return text
    elif file_extension == 'docx':
        text = docx2txt.process(file)
        return text
    else:
        return "Unsupported file format."

# Define a simple chatbot function using NLTK
def chatbot_response(user_input):
    # Tokenize the user input
    tokens = word_tokenize(user_input)

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Define a simple response based on the user input
    if 'hello' in lemmatized_tokens or 'hi' in lemmatized_tokens:
        return 'Hello! How can I assist you today?'
    elif 'how' in lemmatized_tokens and 'are' in lemmatized_tokens and 'you' in lemmatized_tokens:
        return 'I\'m doing well, thank you for asking!'
    else:
        return 'I didn\'t quite understand that. Can you please rephrase?'

# Create a Streamlit app that allows the user to provide either text or speech input to the chatbot
st.title("Speech-Enabled Chatbot")
st.write("Please provide some input:")

# Allow users to upload their file
uploaded_file = st.file_uploader("Choose a file:", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    # Read the contents of the uploaded file
    user_input = read_file(uploaded_file)
    response = chatbot_response(user_input)
    st.write("Chatbot Response:")
    st.write(response)

# Allow users to provide text input
user_input_text = st.text_input("Type something:", "")

if st.button("Submit"):
    response = chatbot_response(user_input_text)
    st.write("Chatbot Response:")
    st.write(response)

# Allow users to provide speech input
if st.button("Speak"):
    user_input = transcribe_speech()
    response = chatbot_response(user_input)
    st.write("Chatbot Response:")
    st.write(response)
