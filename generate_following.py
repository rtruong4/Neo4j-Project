import json
import random

with open("combined_output.json", "r", encoding="utf-8") as f:
    users = json.load(f)

all_ids = [user["id"] for user in users]

for user in users:
    user_id = user["id"]
    

    possible_ids = [i for i in all_ids if i != user_id]
    
   
    num_to_follow = random.randint(5, 10)
    following = random.sample(possible_ids, min(num_to_follow, len(possible_ids)))
    
   
    user["following"] = following


with open("updated_users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2, ensure_ascii=False)