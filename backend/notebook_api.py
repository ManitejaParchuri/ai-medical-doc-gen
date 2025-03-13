from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import uvicorn

app = FastAPI()

# Load datasets
patients_df = pd.read_csv("patients_data.csv")
examinations_df = pd.read_csv("examinations_data.csv")

# Prepare data for similarity search
examinations_df["full_text"] = examinations_df["symptoms"].astype(str) + " " + examinations_df["diagnosis"].astype(str)

# Load Summarization Model
summarizer = pipeline("summarization", model="t5-small")

class NotesInput(BaseModel):
    doctor_notes: str
    nurse_notes: str

# Summarize Notes
def summarize_notes(doctor_notes, nurse_notes):
    combined_text = doctor_notes + " " + nurse_notes
    summary = summarizer(combined_text, max_length=100, min_length=50, do_sample=False)
    return summary[0]["summary_text"]

# Find Similar Cases
def find_similar_cases(summary_text):
    vectorizer = TfidfVectorizer(stop_words="english")
    case_vectors = vectorizer.fit_transform(examinations_df["full_text"])
    query_vector = vectorizer.transform([summary_text])
    similarities = cosine_similarity(query_vector, case_vectors).flatten()
    top_indices = similarities.argsort()[-3:][::-1]
    return examinations_df.iloc[top_indices][["patient_id", "symptoms", "diagnosis"]].to_dict(orient="records")

@app.post("/process_notes")
def process_notes(input_data: NotesInput):
    summary = summarize_notes(input_data.doctor_notes, input_data.nurse_notes)
    similar_cases = find_similar_cases(summary)
    return {"summary": summary, "similar_cases": similar_cases}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8899)
