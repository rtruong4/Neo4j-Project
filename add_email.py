import json


with open('data.json', 'r', encoding='utf-8') as f:
    users = json.load(f)


for user in users:
    
    username_clean = user["userName"].lstrip('@')
    user["email"] = f"{username_clean}@email.com"


with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, indent=2, ensure_ascii=False)
