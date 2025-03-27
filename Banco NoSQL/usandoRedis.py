import redis
import json

# Conectar ao Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Função para cadastrar pacientes
def cadastrar_paciente():
    cpf = input("Digite o CPF do paciente: ")
    nome = input("Digite o nome do paciente: ")
    telefone = input("Digite o telefone do paciente: ")

    paciente = {"nome": nome, "telefone": telefone}
    
    r.set(f"paciente:{cpf}", json.dumps(paciente))  # Salva no Redis
    print("✅ Paciente cadastrado com sucesso!")

# Função para listar pacientes
def listar_pacientes():
    keys = r.keys("paciente:*")  # Pega todas as chaves de pacientes
    if not keys:
        print("❌ Nenhum paciente cadastrado.")
        return

    for key in keys:
        paciente = json.loads(r.get(key))
        print(f"CPF: {key.split(':')[1]}, Nome: {paciente['nome']}, Telefone: {paciente['telefone']}")

# Função para cadastrar médicos
def cadastrar_medico():
    crm = input("Digite o CRM do médico: ")
    nome = input("Digite o nome do médico: ")
    especialidade = input("Digite a especialidade do médico: ")

    medico = {"nome": nome, "especialidade": especialidade}
    
    r.set(f"medico:{crm}", json.dumps(medico))
    print("✅ Médico cadastrado com sucesso!")

# Função para listar médicos
def listar_medicos():
    keys = r.keys("medico:*")
    if not keys:
        print("❌ Nenhum médico cadastrado.")
        return

    for key in keys:
        medico = json.loads(r.get(key))
        print(f"CRM: {key.split(':')[1]}, Nome: {medico['nome']}, Especialidade: {medico['especialidade']}")

# Função para agendar consultas
def agendar_consulta():
    cpf_paciente = input("Digite o CPF do paciente: ")
    paciente = r.get(f"paciente:{cpf_paciente}")

    if not paciente:
        print("❌ Paciente não encontrado!")
        return

    crm_medico = input("Digite o CRM do médico: ")
    medico = r.get(f"medico:{crm_medico}")

    if not medico:
        print("❌ Médico não encontrado!")
        return

    data = input("Digite a data da consulta (YYYY-MM-DD): ")
    hora = input("Digite o horário da consulta (HH:MM): ")

    consulta = {
        "paciente": json.loads(paciente)["nome"],
        "medico": json.loads(medico)["nome"],
        "especialidade": json.loads(medico)["especialidade"],
        "data": data,
        "hora": hora
    }

    r.lpush("consultas", json.dumps(consulta))  # Adiciona na lista de consultas
    print("✅ Consulta agendada com sucesso!")

# Função para listar consultas
def listar_consultas():
    consultas = r.lrange("consultas", 0, -1)  # Pega todas as consultas
    if not consultas:
        print("❌ Nenhuma consulta agendada.")
        return

    for consulta in consultas:
        c = json.loads(consulta)
        print(f"Paciente: {c['paciente']}, Médico: {c['medico']}, Especialidade: {c['especialidade']}, Data: {c['data']}, Hora: {c['hora']}")

# Menu principal
def menu():
    while True:
        print("\n📋 **MENU PRINCIPAL**")
        print("1️⃣ Cadastrar Paciente")
        print("2️⃣ Listar Pacientes")
        print("3️⃣ Cadastrar Médico")
        print("4️⃣ Listar Médicos")
        print("5️⃣ Agendar Consulta")
        print("6️⃣ Listar Consultas")
        print("0️⃣ Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_paciente()
        elif opcao == "2":
            listar_pacientes()
        elif opcao == "3":
            cadastrar_medico()
        elif opcao == "4":
            listar_medicos()
        elif opcao == "5":
            agendar_consulta()
        elif opcao == "6":
            listar_consultas()
        elif opcao == "0":
            print("👋 Encerrando o sistema. Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

# Iniciar sistema
if __name__ == "__main__":
    menu()

