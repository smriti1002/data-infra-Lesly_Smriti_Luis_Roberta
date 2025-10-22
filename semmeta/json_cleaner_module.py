#write a python class that read a json file and clean it
import json
import os

class JsonCleaner:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = input_file.replace("_raw.json", "_cleaned.json")

    def clean_json(self):
        # Load the raw JSON file
        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Keep only keys where value is not None or "null"
        cleaned_data = {}
        for key, value in data.items():
            if value is not None and value != "null":
                cleaned_data[key] = value

        # Save the cleaned JSON file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

        print(f"Cleaned JSON saved to: {self.output_file}")

