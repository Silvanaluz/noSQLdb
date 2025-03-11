import os
from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional
from pymongo.server_api import ServerApi

from dotenv import load_dotenv # type: ignore

load_dotenv()

USER_DB = os.getenv('USER_DB')
SENHA_DB = os.getenv('SENHA_DB')

uri = "mongodb+srv://"+USER_DB+":"+SENHA_DB+"@cluster0.ynjn4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Configuração do banco de dados MongoDB
db = client.medical_appointments
patients_collection = db.patients
doctors_collection = db.doctors
appointments_collection = db.appointments

# Inicializa a aplicação FastAPI
app = FastAPI()

# Modelos Pydantic para validação de dados
class Patient(BaseModel):
    name: str
    age: int
    email: str
    phone: str

class Doctor(BaseModel):
    name: str
    specialty: str
    email: str
    phone: str

class Appointment(BaseModel):
    patient_id: str
    doctor_id: str
    date: str
    time: str

# Rotas para Pacientes
@app.post("/patients/", response_model=dict)
def create_patient(patient: Patient):
    new_patient = patients_collection.insert_one(patient.dict())
    return {"id": str(new_patient.inserted_id)}

@app.get("/patients/", response_model=List[dict])
def get_patients():
    patients = list(patients_collection.find())
    for patient in patients:
        patient["id"] = str(patient["_id"])
        del patient["_id"]
    return patients

# Rotas para Médicos
@app.post("/doctors/", response_model=dict)
def create_doctor(doctor: Doctor):
    new_doctor = doctors_collection.insert_one(doctor.dict())
    return {"id": str(new_doctor.inserted_id)}

@app.get("/doctors/", response_model=List[dict])
def get_doctors():
    doctors = list(doctors_collection.find())
    for doctor in doctors:
        doctor["id"] = str(doctor["_id"])
        del doctor["_id"]
    return doctors

# Rotas para Consultas
@app.post("/appointments/", response_model=dict)
def create_appointment(appointment: Appointment):
    if not patients_collection.find_one({"_id": ObjectId(appointment.patient_id)}):
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if not doctors_collection.find_one({"_id": ObjectId(appointment.doctor_id)}):
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    new_appointment = appointments_collection.insert_one(appointment.dict())
    return {"id": str(new_appointment.inserted_id)}

@app.get("/appointments/", response_model=List[dict])
def get_appointments():
    appointments = list(appointments_collection.find())
    for appointment in appointments:
        appointment["id"] = str(appointment["_id"])
        del appointment["_id"]
    return appointments

@app.delete("/appointments/{appointment_id}", response_model=dict)
def delete_appointment(appointment_id: str):
    result = appointments_collection.delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return {"message": "Consulta cancelada com sucesso"}


