from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import requests  # ✅ Make sure this is imported

# Load CSV Files
patients_df = pd.read_csv("patients_data.csv")
examinations_df = pd.read_csv("examinations_data.csv")
treatments_df = pd.read_csv("treatments_data.csv")

# Enable CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define input model for processing new notes
class NotesInput(BaseModel):
    nurse_notes: str
    doctor_notes: str

# Send Notes to Jupyter Notebook for Processing
@app.post("/process-notes")
async def process_notes(input_data: NotesInput):
    notebook_url = "http://127.0.0.1:8899/process_notes"  # Ensure correct port

    try:
        response = requests.post(notebook_url, json=input_data.dict())  # ✅ Forward request to Jupyter Notebook
        response_data = response.json()  # ✅ Get response from Jupyter Notebook API

        return {
            "summary": response_data.get("summary", "No summary generated."),
            "similar_cases": response_data.get("similar_cases", [])
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Jupyter Notebook: {str(e)}")



# Data Extraction Functions
def get_patient_details(patient_id):
    patient_record = patients_df[patients_df['patient_id'] == patient_id]
    return patient_record.to_dict('records')[0] if not patient_record.empty else {}

def get_examination_details(patient_id):
    exam_records = examinations_df[examinations_df['patient_id'] == patient_id]
    return exam_records.to_dict('records')

def get_treatment_details(patient_id):
    merged_df = treatments_df.merge(examinations_df[['exam_id', 'patient_id']], on='exam_id', how='left')
    treatment_records = merged_df[merged_df['patient_id'] == patient_id]
    return treatment_records.to_dict('records')

# Generate Medical Document
def generate_medical_document(patient_id, nurse_notes, doctor_notes):
    patient_info = get_patient_details(patient_id)
    exam_info = get_examination_details(patient_id)
    treatment_info = get_treatment_details(patient_id)

    document = f"---\n📝 Medical Document for Patient ID: {patient_id}\n---\n\n"

    document += "🔹 Patient Details:\n"
    for key, value in patient_info.items():
        document += f"  - {key.replace('_', ' ').title()}: {value}\n"

    document += "\n🔍 Examination Details:\n"
    for exam in exam_info:
        for key, value in exam.items():
            if key != "patient_id":
                document += f"  - {key.replace('_', ' ').title()}: {value}\n"

    document += "\n💉 Treatment Details:\n"
    for treatment in treatment_info:
        for key, value in treatment.items():
            if key not in ["exam_id", "patient_id"]:
                document += f"  - {key.replace('_', ' ').title()}: {value}\n"

    document += "\n📝 Observations from Medical Staff:\n"
    document += f"  - Nurse's Notes: {nurse_notes}\n"
    document += f"  - Doctor's Notes: {doctor_notes}\n"  # Changed from dentist_notes to doctor_notes

    return document

# # Update API Endpoint
# @app.post("/process-notes")
# async def process_notes(input_data: NotesInput):
#     ai_output = generate_medical_document(input_data.patient_id, input_data.nurse_notes, input_data.doctor_notes)
#     return {"ai_output": ai_output}

    


def get_patient_details(patient_id):
    """
    Retrieve patient details by ensuring case insensitivity and trimming spaces.
    """
    # Normalize the patient ID column in the dataframe
    patients_df["patient_id"] = patients_df["patient_id"].astype(str).str.strip().str.upper()
    
    # Normalize the input patient ID
    patient_id = patient_id.strip().upper()

    patient_record = patients_df[patients_df["patient_id"] == patient_id]
    
    return patient_record.to_dict("records")[0] if not patient_record.empty else {}


def get_examination_details(patient_id):
    """
    Retrieve examination records for a given patient.
    """
    # Normalize the patient ID column in the dataframe
    examinations_df["patient_id"] = examinations_df["patient_id"].astype(str).str.strip().str.upper()
    
    # Normalize the input patient ID
    patient_id = patient_id.strip().upper()

    exam_records = examinations_df[examinations_df["patient_id"] == patient_id]
    
    return exam_records.to_dict("records") if not exam_records.empty else []


def get_treatment_details(patient_id):
    """
    Retrieve treatment records by linking exams with patient ID.
    """
    # Normalize the patient ID column in the examinations dataframe
    examinations_df["patient_id"] = examinations_df["patient_id"].astype(str).str.strip().str.upper()
    
    # Normalize the exam ID column in the treatments dataframe
    treatments_df["exam_id"] = treatments_df["exam_id"].astype(str).str.strip()

    # Normalize the input patient ID
    patient_id = patient_id.strip().upper()

    # Merge treatments with examinations to link patient_id
    merged_df = treatments_df.merge(
        examinations_df[["exam_id", "patient_id"]],
        on="exam_id",
        how="left"
    )
    
    treatment_records = merged_df[merged_df["patient_id"] == patient_id]
    
    return treatment_records.to_dict("records") if not treatment_records.empty else []


@app.get("/get-patient-records/{patient_id}")
async def get_patient_records(patient_id: str):
    """
    Fetch all past medical records for the given patient and return them in structured document format.
    """
    print(f"Fetching records for patient_id: {patient_id}")

    # Retrieve patient details, exams, and treatments
    patient_info = get_patient_details(patient_id)
    exam_info = get_examination_details(patient_id)
    treatment_info = get_treatment_details(patient_id)

    # 🔍 Debugging: Print extracted data before document generation
    print("\n✅ Extracted Patient Info:", patient_info if patient_info else "❌ No patient details found!")
    print("\n✅ Extracted Examination Info:", exam_info if exam_info else "❌ No examination records found!")
    print("\n✅ Extracted Treatment Info:", treatment_info if treatment_info else "❌ No treatment records found!")

    # If no data is found, return an error
    if not patient_info and not exam_info and not treatment_info:
        return {"error": "No records found for this patient ID."}

    # Generate the document
    medical_record = generate_medical_document(patient_id, "", "")

    return {"medical_record": medical_record}

@app.get("/get-patient-ids")
async def get_patient_ids():
    """
    Fetch all unique patient IDs for frontend dropdown selection.
    """
    patient_ids = patients_df["patient_id"].astype(str).unique().tolist()
    return {"patient_ids": patient_ids}
