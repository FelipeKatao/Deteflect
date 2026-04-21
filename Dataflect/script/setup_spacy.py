import spacy
import subprocess
import sys
import os

MODEL_NAME = "pt_core_news_sm"
MODEL_PATH = "models/nlp"

def download_model():
    subprocess.check_call(
        [sys.executable, "-m", "spacy", "download", MODEL_NAME]
    )

def save_model():
    nlp = spacy.load(MODEL_NAME)

    os.makedirs("models", exist_ok=True)

    nlp.to_disk(MODEL_PATH)

    print("Modelo salvo em:", MODEL_PATH)

if __name__ == "__main__":
    download_model()
    save_model()
