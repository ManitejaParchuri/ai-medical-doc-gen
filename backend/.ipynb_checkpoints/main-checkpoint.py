import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle

# Create a FastAPI instance
app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The origin of your React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML model and vectorizer using absolute paths
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
vectorizer_path = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

# Define a request model using Pydantic
class NotesInput(BaseModel):
    nurse_notes: str
    dentist_notes: str

# Simple GET endpoint to test the server
@app.get("/")
async def read_root():
    return {"message": "FastAPI backend is running successfully!"}

# POST endpoint to receive notes from the frontend and process with ML model
@app.post("/process-notes")
async def process_notes(input_data: NotesInput):
    # Combine the input notes
    combined_text = f"{input_data.nurse_notes} {input_data.dentist_notes}"
    
    # Preprocess the text using the vectorizer
    text_vector = vectorizer.transform([combined_text])
    
    # Make a prediction using the ML model
    prediction = model.predict(text_vector)
    
    # Prepare the AI output based on the prediction
    ai_output = f"The AI model predicts the sentiment as: {prediction[0]}"
    
    return {"ai_output": ai_output}
