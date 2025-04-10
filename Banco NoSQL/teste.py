from pymongo import MongoClient
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações de conexão MongoDB
mongo_uri = "mongodb://localhost:27017/"
mongo_db = "clinica_medica"
mongo_collection = "consultas"

# Configurações de conexão Neo4j
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "PASSWORD"

# Função para conectar e transferir dados
def transferir_dados_mongo_para_neo4j():
    # Conectar ao MongoDB
    mongo_client = MongoClient(f"mongodb+srv://{os.getenv('USER_DB')}:{os.getenv('SENHA_DB')}@cluster0.ynjn4.mongodb.net/?retryWrites=true&w=majority")
    db = mongo_client[mongo_db]
    collection = db[mongo_collection]
    
    # Conectar ao Neo4j
    neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    
    # Buscar documentos do MongoDB
    documentos = collection.find()
    
    # Transferir cada documento para o Neo4j
    with neo4j_driver.session() as session:
        for documento in documentos:
            # Exemplo de criação de nós baseados em documentos do MongoDB
            # Adapte conforme sua estrutura de dados
            session.run(
                """
                CREATE (n:Documento {
                    id: $id,
                    titulo: $titulo,
                    descricao: $descricao
                })
                """,
                id=str(documento.get("_id")),
                titulo=documento.get("titulo", ""),
                descricao=documento.get("descricao", "")
            )
            
            # Exemplo de criação de relacionamentos
            # Se seu documento tiver referências a outros documentos
            if "referencias" in documento:
                for ref_id in documento["referencias"]:
                    session.run(
                        """
                        MATCH (a:Documento {id: $doc_id})
                        MATCH (b:Documento {id: $ref_id})
                        CREATE (a)-[:RELACIONA_COM]->(b)
                        """,
                        doc_id=str(documento.get("_id")),
                        ref_id=str(ref_id)
                    )
    
    # Fechar conexões
    neo4j_driver.close()
    mongo_client.close()
    
    print("Transferência de dados concluída!")

# Executar a função de transferência
if __name__ == "__main__":
    transferir_dados_mongo_para_neo4j()

