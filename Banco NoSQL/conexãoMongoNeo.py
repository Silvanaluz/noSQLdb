from neo4j import GraphDatabase

# 🔐 Conexão com Neo4j Desktop
URI = "bolt://localhost:7687"
USER = "neo4j"  # ou seu usuário
PASSWORD = "sua_senha_aqui"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def inserir_dados(tx):
    # Pacientes
    tx.run("""
        CREATE (:Paciente {nome: "Carlos Silva", cpf: "12345678900", email: "carlos@email.com"});
        CREATE (:Paciente {nome: "Fernanda Lima", cpf: "98765432100", email: "fernanda@email.com"});
        CREATE (:Paciente {nome: "João Almeida", cpf: "11122233344", email: "joao@email.com"});
    """)
    
    # Médicos
    tx.run("""
        CREATE (:Medico {nome: "Dra. Juliana Souza", crm: "SP123456", especialidade: "Dermatologia"});
        CREATE (:Medico {nome: "Dr. Ricardo Gomes", crm: "RJ654321", especialidade: "Cardiologia"});
    """)

    # Consultas com localização
    tx.run("""
        CREATE (:Consulta {
            id: "c1",
            data: date("2025-05-01"),
            hora: "09:00",
            preco: 300,
            localizacao: point({latitude: -23.550520, longitude: -46.633308})
        });

        CREATE (:Consulta {
            id: "c2",
            data: date("2025-05-02"),
            hora: "14:30",
            preco: 450,
            localizacao: point({latitude: -22.906847, longitude: -43.172896})
        });

        CREATE (:Consulta {
            id: "c3",
            data: date("2025-05-03"),
            hora: "11:00",
            preco: 250,
            localizacao: point({latitude: -19.916681, longitude: -43.934493})
        });
    """)

    # Relacionamentos
    tx.run("""
        MATCH (p:Paciente {nome: "Carlos Silva"}), 
              (m:Medico {nome: "Dra. Juliana Souza"}), 
              (c:Consulta {id: "c1"})
        MERGE (p)-[:REALIZOU]->(c)
        MERGE (m)-[:REALIZOU]->(c);

        MATCH (p:Paciente {nome: "Fernanda Lima"}), 
              (m:Medico {nome: "Dr. Ricardo Gomes"}), 
              (c:Consulta {id: "c2"})
        MERGE (p)-[:REALIZOU]->(c)
        MERGE (m)-[:REALIZOU]->(c);

        MATCH (p:Paciente {nome: "João Almeida"}), 
              (m:Medico {nome: "Dra. Juliana Souza"}), 
              (c:Consulta {id: "c3"})
        MERGE (p)-[:REALIZOU]->(c)
        MERGE (m)-[:REALIZOU]->(c);
    """)

with driver.session() as session:
    session.execute_write(inserir_dados)
    print("✅ Dados inseridos com sucesso no Neo4j!")

driver.close()
