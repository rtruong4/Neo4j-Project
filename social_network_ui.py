from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

def register_user():
    print("=== User Registration ===")
    fullName = input("Enter full name: ")
    userName = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    bio = input("Enter bio: ")
    outputProfileName = userName.strip("@")  # Automatically generate outputProfileName
    
    with driver.session() as session:
        # First find the maximum ID and add 1 using COALESCE
        result = session.run("""
            MATCH (u:User)
            WITH COALESCE(MAX(u.id), 0) + 1 AS next_id
            
            CREATE (u:User {
                id: next_id,
                userName: $userName,
                fullName: $fullName,
                email: $email,
                password: $password,
                bio: $bio,
                outputProfileName: $outputProfileName
            })
            RETURN u.id AS newUserId, u.userName AS newUserName
        """, userName=userName, fullName=fullName, email=email, 
             password=password, bio=bio, outputProfileName=outputProfileName)
        
        record = result.single()
        if record:
            print(f"✅ Registration successful! Created user with ID: {record['newUserId']}")
        else:
            print("⚠️ Registration may have failed")


def login_user():
    print("=== User Login ===")
    userName = input("Enter username: ")
    password = input("Enter password: ")

    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {userName: $userName, password: $password})
            RETURN u
        """, userName=userName, password=password)

        record = result.single()
        if record:
            print("✅ Login successful!")
            user_dashboard(userName)
        else:
            print("❌ Login failed. Try again.")

def user_dashboard(userName):
    while True:
        print("\n=== User Dashboard ===")
        print("1. View Profile")
        print("2. Edit Profile")
        print("8. Find Mutual Connections")
        print("9. Find Recommended Friends")
        print("3. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            view_profile(userName)
        elif choice == "2":
            edit_profile(userName)
        elif choice == "3":
            print("👋 Logged out.")
            break
        elif choice == "8":
            find_mutuals(userName)
        elif choice == "9":
            find_recommended(userName)
        else:
            print("Invalid choice.")

def find_mutuals(userName):
    while True:
        print("\n")
        friendName = input("Enter the username of the person you would like to find the mutuals of: ")
        with driver.session() as session:
            result = session.run("""MATCH (user1:User {userName: $userName})-[:FOLLOWS]->(mutual:User),
                (user2:User {userName: $friendName})-[:FOLLOWS]->(mutual:User)
            RETURN mutual.userName AS username
                """, userName = userName, friendName = friendName)
            
            record = list(result)

            if not record:
                print("No mutual followings found")
            else:
                print(f"\nFound {len(record)} mutual followings between {userName} and {friendName}:")
                print("-" * 80)

                for i, user in enumerate(record, 1):
                    print(str(i) + "." + user['username'])
        print("-" * 80)
        choice = input("Would you like to find mutuals with another user? (y/n): ")
        if choice != "y":
            break
    
def find_recommended(userName):
    print(f"\nFinding friend recommendations for {userName}...")
    
    with driver.session() as session:
        result = session.run("""
            MATCH (user:User {userName: $userName})-[:FOLLOWS]->(:User)-[:FOLLOWS]->(potentialFriend:User)
            WHERE NOT (user)-[:FOLLOWS]->(potentialFriend) 
              AND user <> potentialFriend
              AND NOT potentialFriend.userName = $userName
            WITH potentialFriend, COUNT(*) AS commonConnections
            ORDER BY commonConnections DESC
            RETURN potentialFriend.userName AS username,
                   potentialFriend.fullName AS fullname,
                   potentialFriend.id AS id,
                   potentialFriend.bio AS bio,
                   commonConnections
            LIMIT 10
            """, userName=userName)
        
        recommendations = list(result)
        
        if not recommendations:
            print(f"No recommendations found for {userName}.")
        else:
            print(f"\nFound {len(recommendations)} friend recommendations for {userName}:")
            print("-" * 80)
            
            for i, record in enumerate(recommendations, 1):
                print(f"Recommendation #{i}:")
                print(f"Username: {record['username']}")
                print(f"Full Name: {record['fullname']}")
                print(f"User ID: {record['id']}")
                print(f"Bio: {record['bio']}")
                print(f"Common Connections: {record['commonConnections']}")
                print("-" * 80)
                
def view_profile(userName):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {userName: $userName})
            RETURN u.fullName AS fullName, u.email AS email, u.bio AS bio, u.outputProfileName AS outputProfileName
        """, userName=userName)

        record = result.single()
        if record:
            print("\n--- Profile ---")
            print(f"Name: {record['fullName']}")
            print(f"Email: {record['email']}")
            print(f"Bio: {record['bio']}")
            print(f"Profile Name: {record['outputProfileName']}")
        else:
            print("❌ Profile not found.")

def edit_profile(userName):
    while True:
        print("\n=== Edit Profile ===")
        print("1. Edit Full Name")
        print("2. Edit Bio")
        print("3. Edit Email")
        print("4. Edit Password")
        print("5. Go Back")
        choice = input("Choose an option: ")

        if choice == "1":
            newName = input("Enter new full name: ")
            with driver.session() as session:
                session.run("""
                    MATCH (u:User {userName: $userName})
                    SET u.fullName = $newName
                """, userName=userName, newName=newName)
            print("✅ Full Name updated successfully!")

        elif choice == "2":
            newBio = input("Enter new bio: ")
            with driver.session() as session:
                session.run("""
                    MATCH (u:User {userName: $userName})
                    SET u.bio = $newBio
                """, userName=userName, newBio=newBio)
            print("✅ Bio updated successfully!")

        elif choice == "3":
            newEmail = input("Enter new email: ")
            with driver.session() as session:
                session.run("""
                    MATCH (u:User {userName: $userName})
                    SET u.email = $newEmail
                """, userName=userName, newEmail=newEmail)
            print("✅ Email updated successfully!")

        elif choice == "4":
            newPassword = input("Enter new password: ")
            with driver.session() as session:
                session.run("""
                    MATCH (u:User {userName: $userName})
                    SET u.password = $newPassword
                """, userName=userName, newPassword=newPassword)
            print("✅ Password updated successfully!")

        elif choice == "5":
            break  # Go back to user dashboard

        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("\n=== Welcome to the Social Network ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
