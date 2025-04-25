import json


with open('data.json', 'r', encoding='utf-8') as f:
    users = json.load(f)


for user in users:
    user["userName"] = user["userName"].lstrip('@')  


with open('updated_data.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, indent=2, ensure_ascii=False)
