import os
import glob
import json

data_dir = "./data"

output_json = "combined_output.json"

all_entries = []

fields_to_omit = {"bigrams", "pictureURL", "location", "externalUrl"}

for subfolder in os.listdir(data_dir):
    subfolder_path = os.path.join(data_dir, subfolder)

    if os.path.isdir(subfolder_path):
        json_files = glob.glob(os.path.join(subfolder_path, "*.json"))

        for json_file in json_files:
            if "twitter" in os.path.basename(json_file).lower():
                try:
                    with open(json_file, encoding='utf-8') as f:
                        data = json.load(f)

                        # Normalize structure to a list
                        if isinstance(data, dict):
                            data = [data]
                        elif not isinstance(data, list):
                            print(f"Skipping {json_file}: unexpected JSON format")
                            continue

                        for entry in data:
                            if isinstance(entry, dict):
                                # Remove unwanted fields
                                filtered_entry = {k: v for k, v in entry.items() if k not in fields_to_omit}
                                all_entries.append(filtered_entry)

                except json.JSONDecodeError as e:
                    print(f"Skipping {json_file}: invalid JSON - {e}")

# Write filtered data to file
with open(output_json, "w", encoding="utf-8") as out_file:
    json.dump(all_entries, out_file, indent=2, ensure_ascii=False)