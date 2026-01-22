import re
import os
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import joblib

script_dir = os.path.dirname(os.path.abspath(__file__))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters
    return text

def load_model_and_tokenizer():
    loaded_model = joblib.load(f'{script_dir}/RAILS1.0alpha_text_classification.pkl')
    loaded_vectorizer = joblib.load(f'{script_dir}/Tfidf_vectorizer.pkl')
    
    return loaded_model, loaded_vectorizer

# Function to classify input text with loaded model and tokenizer
def classify_text_with_loaded_model(comment, model, vectorizer):
    comment = preprocess_text(comment)
    comment_tfidf = vectorizer.transform([comment])
    prediction = model.predict(comment_tfidf)
    return prediction[0]