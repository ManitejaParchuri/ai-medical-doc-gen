from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import uvicorn
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

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





# 🔹 Load & Prepare Data for Model Evaluation
def prepare_evaluation_data():
    # Convert text features to numerical representations
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(examinations_df["full_text"])  
    y = examinations_df["diagnosis"]  # Assuming 'diagnosis' is the label

    # Split data into training & test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a simple classification model (Naive Bayes)
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Predict on test data
    y_pred = model.predict(X_test)

    return y_test, y_pred

# 🔹 Compute Evaluation Metrics
def evaluate_model():
    y_test, y_pred = prepare_evaluation_data()

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')  # Weighted for multi-class
    recall = recall_score(y_test, y_pred, average='weighted')

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall
    }

# 🔹 API to Run Model Evaluation (Only in Jupyter Notebook)
@app.get("/evaluate_model")
def get_model_evaluation():
    metrics = evaluate_model()
    return {"evaluation": metrics}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8899)