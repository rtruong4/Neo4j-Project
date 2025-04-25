import json
from neo4j import GraphDatabase


with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_users_and_relationships(tx, user):
    
    tx.run(
        """
        MERGE (u:User {id: $id})
        SET u.userName = $userName, u.bio = $bio, 
            u.outputProfileName = $outputProfileName, u.fullName = $fullName, 
            u.password = $password, u.email = $email
        """,
        id=user["id"],
        userName=user["userName"],
        bio=user["bio"],
        outputProfileName=user["outputProfileName"],
        fullName=user["fullName"],
        password=user["password"],
        email=user["email"]
    )
    
    for follow_id in user.get("following", []):
        tx.run(
            """
            MERGE (f:User {id: $follow_id})
            MERGE (u:User {id: $id})
            MERGE (u)-[:FOLLOWS]->(f)
            """,
            id=user["id"],
            follow_id=follow_id
        )


with driver.session() as session:
    print("Loading data...")
    for user in data:
        session.execute_write(create_users_and_relationships, user)
    print("Finished loading data")
driver.close()
