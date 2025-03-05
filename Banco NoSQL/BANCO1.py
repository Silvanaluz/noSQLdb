

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

USER_DB = os.getenv('USER_DB')
SENHA_DB = os.getenv('SENHA_DB')

uri = "mongodb+srv://"+USER_DB+":"+SENHA_DB+"@cluster0.ynjn4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["clinica_medica"]

consultas = db["consultas"]

consultas.insert_one({
    "paciente": {
        "nome": "Carlos Silva",
        "email": "carlos.silva@email.com",
        "telefone": "(11) 99999-0000",
        "data_cadastro": "2025-02-20T10:00:00Z",
    },
    "especialista": {
        "nome": "Dra. Juliana Souza",
        "especialidade": "Dermatologia",
        "crm": "SP-123456",
        "telefone": "(11) 98888-1111",
        "email": "juliana.souza@email.com",
    },
    "data_consulta": "05/03/2025",
    "preco_consulta": 300,
    "hora_consulta": "16:00",
    "exames_pedidos": [{
        "cid": "M1030"
    },
    {
        "cid": "M1040"
    }
    ]
})

print("Documentos inseridos com sucesso!")