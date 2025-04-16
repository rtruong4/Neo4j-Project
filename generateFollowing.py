import json
import random

# Load your input file
with open("combined_output.json", "r", encoding="utf-8") as f:
    users = json.load(f)

# Get all user IDs
all_ids = [user["id"] for user in users]

# Add following list to each user
for user in users:
    user_id = user["id"]
    
    # Possible IDs to follow (exclude self)
    possible_ids = [i for i in all_ids if i != user_id]
    
    # Choose 5–10 random users to follow
    num_to_follow = random.randint(5, 10)
    following = random.sample(possible_ids, min(num_to_follow, len(possible_ids)))
    
    # Add the 'following' field
    user["following"] = following

# Save the updated file
with open("updated_users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2, ensure_ascii=False)