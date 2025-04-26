from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

def register_user():
    print("=== User Registration ===")
    fullName = input("Enter full name: ")
    userName = input("Enter username (@example): ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    bio = input("Enter bio: ")
    outputProfileName = userName.strip("@")  # Automatically generate outputProfileName

    with driver.session() as session:
        session.run("""
            CREATE (u:User {
                id: toInteger(rand() * 100000),
                userName: $userName,
                fullName: $fullName,
                email: $email,
                password: $password,
                bio: $bio,
                outputProfileName: $outputProfileName
            })
        """, userName=userName, fullName=fullName, email=email, password=password, bio=bio, outputProfileName=outputProfileName)

    print("✅ Registration successful!")

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
        print("3. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            view_profile(userName)
        elif choice == "2":
            edit_profile(userName)
        elif choice == "3":
            print("👋 Logged out.")
            break
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
