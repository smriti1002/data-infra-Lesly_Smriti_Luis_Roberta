# write a python class for extraction and visualization
import json
from PIL import Image
import re

FEATURES_TO_EXTRACT = [
    "AP_WD",
    "AP_BEAM_TIME",
    "AP_IMAGE_PIXEL_SIZE",
    "AP_HOLDER_HEIGHT",
    "AP_BEAM_CURRENT",
    "AP_HOLDER_DIAMETER",
]

def _extract_features(image_metadata_file):
    """Extract specific features from the metadata file"""
    image_features = {}
    
    try:
        with open(image_metadata_file, "r") as file:
            image_metadata = json.load(file)
            for key, value in image_metadata.items():
                if key in FEATURES_TO_EXTRACT:
                    image_features[key] = value
    except FileNotFoundError:
        print(f"Error: File '{image_metadata_file}' not found")
        return {}
    
    return image_features


def _parse_value_unit(value_string):
    """Extract numeric value and unit from strings like 'Beam Current = 80.0 µA'"""
    # Match number (with optional decimal) and unit
    match = re.search(r"([\d.]+)\s*([a-zA-Zµ]+)", value_string)
    if match:
        return match.group(1), match.group(2)  # (numeric_value, unit)
    return value_string, ""  # Return original if no match


def _print_image_metadata(image_metadata):
    """Print the image metadata in a table format"""
    
    print(f"{'-'*30} | {'-'*15} | {'-'*10}")
    print(f"{'Variable':<30} | {'Value':<15} | {'Unit':<10}")
    print(f"{'-'*30} | {'-'*15} | {'-'*10}")
    
    for key, dict_value in image_metadata.items():
        value, unit = _parse_value_unit(dict_value)
        print(f"{key:<30} | {value:<15} | {unit:<10}")
    print(f"{'-'*30} | {'-'*15} | {'-'*10}")
    return

def visualize_features(image_metadata_file, image_file):
    """Visualize the image in another window and the metadata in the terminal"""
    extracted_image_features = _extract_features(image_metadata_file)
    try:
        img = Image.open(image_file)
    except FileNotFoundError:
        print(f"Error: Image file '{image_file}' not found")
        return
    img.show()
    if extracted_image_features:
        _print_image_metadata(extracted_image_features)
    else:
        print("No features found in the provided metadata file")
    return