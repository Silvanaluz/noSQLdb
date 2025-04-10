from neo4j import GraphDatabase

# Define a class to handle the connection
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()

    def insert_data(self, query, parameters=None):
        with self.driver.session() as session:
            session.run(query, parameters)

    def get_data(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]

# Connect to Neo4j
uri = "bolt://localhost:7687/neo4j"  # Update with your Neo4j connection URI
user = "neo4j"                 # Update with your username
password = "sls37361370"          # Update with your password

connection = Neo4jConnection(uri, user, password)

# Action 1: Insert data
insert_query = """
CREATE (p:Person {name: $name, age: $age})
"""
connection.insert_data(insert_query, {"name": "Selvana", "age": 87})

# Action 2: Retrieve data
retrieve_query = """
MATCH (p:Person)
RETURN p.name AS name, p.age AS age
"""
data = connection.get_data(retrieve_query)
print("Retrieved Data:", data)

# Close connection
connection.close()