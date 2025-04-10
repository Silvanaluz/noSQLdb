from neo4j import GraphDatabase

class ClinicDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_entities(self):
        with self.driver.session() as session:
            # Batch creation for entities using a single transaction
            session.run("""
            CREATE
                (d1:Doctor {id: 'D1', name: 'Dr. Ana', specialty: 'Cardiology', location: 'Uberlândia'}),
                (d2:Doctor {id: 'D2', name: 'Dr. Pedro', specialty: 'Orthopedics', location: 'São Paulo'}),
                (p1:Patient {id: 'P1', name: 'Carla', age: 35, location: 'Uberlândia'}),
                (p2:Patient {id: 'P2', name: 'Lucas', age: 50, location: 'São Paulo'}),
                (c1:Consultation {id: 'C1', date: '2025-04-10', location: 'Uberlândia'}),
                (c2:Consultation {id: 'C2', date: '2025-05-15', location: 'São Paulo'}),
                (d1)-[:PERFORMS]->(c1),
                (c1)-[:ATTENDED_BY]->(p1),
                (d2)-[:PERFORMS]->(c2),
                (c2)-[:ATTENDED_BY]->(p2)
            """)

    def query_graph(self):
        with self.driver.session() as session:
            # Projecting the graph for use with GDS
            session.run("""
            CALL gds.graph.project(
                'clinicGraph',
                ['Doctor', 'Patient', 'Consultation'],
                {
                    PERFORMS: {type: 'PERFORMS', orientation: 'UNDIRECTED'},
                    ATTENDED_BY: {type: 'ATTENDED_BY', orientation: 'UNDIRECTED'}
                }
            )
            """)

            # Run Degree Centrality algorithm on the graph
            query = """
            CALL gds.degree.stream('clinicGraph')
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).name AS name, score
            ORDER BY score DESC
            LIMIT 5
            """
            result = session.run(query)
            
            # Output results
            print("Degree Centrality Results:")
            for record in result:
                print(f"Name: {record['name']}, Centrality Score: {record['score']}")

            # Drop the graph projection to avoid conflicts
            session.run("CALL gds.graph.drop('clinicGraph')")

# Connect to Neo4j
uri = "bolt://localhost:7687/neo4j"
user = "neo4j"
password = "sls37361370"

db = ClinicDatabase(uri, user, password)

# Create entities and relationships
db.create_entities()

# Perform advanced graph analysis
db.query_graph()

# Close connection
db.close()

