import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter credenciais do MongoDB
USER_DB = os.getenv('USER_DB')
SENHA_DB = os.getenv('SENHA_DB')

# Construção da URI de conexão
uri = f"mongodb+srv://{USER_DB}:{SENHA_DB}@cluster0.ynjn4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Criar cliente e conectar ao servidor
client = MongoClient(uri, server_api=ServerApi('1'))

# Verificar conexão
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Erro de conexão: {e}")

# Selecionar banco de dados e coleção
db = client["clinica_medica"]
consultas = db["consultas"]
medicos = db["medicos"]
pacientes = db["pacientes"]

# Inserir documentos na coleção "pacientes"
pacientes.insert_one({
    "nome": "João Silva",
    "data_nascimento": "1990-05-15",
    "cpf": "123.456.789-00",
    "telefone": "+55 11 98765-4321",
    "email": "joao.silva@email.com",
    "endereco": {
        "rua": "Av. Paulista",
        "numero": 1000,
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01310-100"
    },
    "historico_medico": [
        {
            "doenca": "Hipertensão",
            "tratamento": "Uso contínuo de Losartana",
            "data_diagnostico": "2018-10-01"
        }
    ]
})

# Inserir documentos na coleção "medicos"
medicos.insert_one({
    "nome": "Dra. Maria Oliveira",
    "crm": "123456-SP",
    "especialidade": "Cardiologia",
    "telefone": "+55 11 98765-4322",
    "email": "maria.oliveira@email.com",
    "horarios_disponiveis": [
        { "dia": "segunda-feira", "horario": "09:00 - 12:00" },
        { "dia": "quarta-feira", "horario": "14:00 - 18:00" }
    ]
})

# Inserir documentos na coleção "consultas"
consultas.insert_one({
    "paciente_id": ObjectId("65f12c34a12b4e001e234567"),
    "medico_id": ObjectId("65f12d78b12b4e001e345678"),
    "data_consulta": "2025-03-20T10:00:00Z",
    "status": "agendada",
    "observacoes": "Paciente precisa levar exames recentes."
})

# Consultas para projetar apenas alguns campos
dados_medicos = list(medicos.aggregate([
    {
        "$project": {
            "_id": 0,
            "nome": 1,
            "especialidade": 1,
            "horarios_disponiveis": 1
        }
    }
]))
print("Médicos:", dados_medicos)

# Consultas para agrupar e contar consultas por status
estatisticas_consultas = list(consultas.aggregate([
    { "$group": { "_id": "$status", "quantidade": { "$sum": 1 } } }
]))
print("Estatísticas de Consultas:", estatisticas_consultas)
