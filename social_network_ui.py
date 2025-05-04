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
    outputProfileName = userName.strip("@")

    with driver.session() as session:
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
            RETURN u.id AS newUserId
        """, userName=userName, fullName=fullName, email=email, password=password, bio=bio, outputProfileName=outputProfileName)

        record = result.single()
        if record:
            print(f"✅ Registration successful! User ID: {record['newUserId']}")
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

        if result.single():
            print("✅ Login successful!")
            user_dashboard(userName)
        else:
            print("❌ Login failed.")

def user_dashboard(userName):
    while True:
        print("\n=== User Dashboard ===")
        print("1. View Profile")
        print("2. Edit Profile")
        print("3. Logout")
        print("5. Follow a User")
        print("6. Unfollow a User")
        print("7. View My Connections")
        print("8. Find Mutual Connections")
        print("9. Find Recommended Friends")
        choice = input("Choose an option: ")

        if choice == "1":
            view_profile(userName)
        elif choice == "2":
            edit_profile(userName)
        elif choice == "3":
            print("👋 Logged out.")
            break
        elif choice == "5":
            follow_user(userName)
        elif choice == "6":
            unfollow_user(userName)
        elif choice == "7":
            view_connections(userName)
        elif choice == "8":
            find_mutuals(userName)
        elif choice == "9":
            find_recommended(userName)
        else:
            print("Invalid choice.")

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
                session.run("MATCH (u:User {userName: $userName}) SET u.fullName = $newName", userName=userName, newName=newName)
            print("✅ Full Name updated.")
        elif choice == "2":
            newBio = input("Enter new bio: ")
            with driver.session() as session:
                session.run("MATCH (u:User {userName: $userName}) SET u.bio = $newBio", userName=userName, newBio=newBio)
            print("✅ Bio updated.")
        elif choice == "3":
            newEmail = input("Enter new email: ")
            with driver.session() as session:
                session.run("MATCH (u:User {userName: $userName}) SET u.email = $newEmail", userName=userName, newEmail=newEmail)
            print("✅ Email updated.")
        elif choice == "4":
            newPassword = input("Enter new password: ")
            with driver.session() as session:
                session.run("MATCH (u:User {userName: $userName}) SET u.password = $newPassword", userName=userName, newPassword=newPassword)
            print("✅ Password updated.")
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def follow_user(userName):
    target = input("Enter the username to follow: ")
    with driver.session() as session:
        result = session.run("""
            MATCH (a:User {userName: $userName}), (b:User {userName: $target})
            WHERE a <> b
            MERGE (a)-[:FOLLOWS]->(b)
            RETURN b.fullName AS fullName
        """, userName=userName, target=target)
        record = result.single()
        if record:
            print(f"✅ Now following {record['fullName']} (@{target})")
        else:
            print("❌ Could not follow user.")

def unfollow_user(userName):
    target = input("Enter the username to unfollow: ")
    with driver.session() as session:
        result = session.run("""
            MATCH (a:User {userName: $userName})-[f:FOLLOWS]->(b:User {userName: $target})
            DELETE f
            RETURN b.fullName AS fullName
        """, userName=userName, target=target)
        record = result.single()
        if record:
            print(f"❌ Unfollowed {record['fullName']} (@{target})")
        else:
            print("⚠️ Not following or user does not exist.")

def view_connections(userName):
    with driver.session() as session:
        following = session.run("""
            MATCH (:User {userName: $userName})-[:FOLLOWS]->(u:User)
            RETURN u.userName AS userName, u.fullName AS fullName
        """, userName=userName)
        followers = session.run("""
            MATCH (u:User)-[:FOLLOWS]->(:User {userName: $userName})
            RETURN u.userName AS userName, u.fullName AS fullName
        """, userName=userName)

        print("\n--- Following ---")
        following_list = list(following)
        if not following_list:
            print("You’re not following anyone.")
        else:
            for i, user in enumerate(following_list, 1):
                print(f"{i}. {user['fullName']} (@{user['userName']})")

        print("\n--- Followers ---")
        followers_list = list(followers)
        if not followers_list:
            print("No one follows you.")
        else:
            for i, user in enumerate(followers_list, 1):
                print(f"{i}. {user['fullName']} (@{user['userName']})")

def find_mutuals(userName):
    while True:
        friendName = input("Enter username to find mutuals with: ")
        with driver.session() as session:
            result = session.run("""
                MATCH (u1:User {userName: $userName})-[:FOLLOWS]->(m:User),
                      (u2:User {userName: $friendName})-[:FOLLOWS]->(m)
                RETURN m.userName AS username
            """, userName=userName, friendName=friendName)
            mutuals = list(result)
            if not mutuals:
                print("No mutual connections.")
            else:
                print(f"\n{len(mutuals)} mutuals:")
                for i, m in enumerate(mutuals, 1):
                    print(f"{i}. @{m['username']}")
        again = input("Find more? (y/n): ")
        if again.lower() != 'y':
            break

def find_recommended(userName):
    print(f"\nFinding recommendations for {userName}...")
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {userName: $userName})-[:FOLLOWS]->(:User)-[:FOLLOWS]->(rec:User)
            WHERE NOT (u)-[:FOLLOWS]->(rec) AND rec.userName <> $userName
            WITH rec, COUNT(*) AS score
            ORDER BY score DESC
            RETURN rec.userName AS username, rec.fullName AS fullName, rec.bio AS bio, score
            LIMIT 10
        """, userName=userName)
        recommendations = list(result)
        if not recommendations:
            print("No recommendations found.")
        else:
            print("\nTop Recommendations:")
            for i, r in enumerate(recommendations, 1):
                print(f"{i}. @{r['username']} - {r['fullName']} (Bio: {r['bio']}) — Common Links: {r['score']}")

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
            print("Invalid option.")

if __name__ == "__main__":
    main()
