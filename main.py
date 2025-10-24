from semmeta.visualizer_module import visualize_features
from semmeta.metadata_extractor_module import SEMMetaData
from semmeta.json_cleaner_module import JsonCleaner


def main():
    # Request the name of the image from the user
    image_name = input("Enter the name of the image, no path (e.g., 12_50_vero_09): ").strip()

    # Initialize variable for image and output paths and populate them
    if not image_name.endswith(".tif"):
        image_file = f"imgs/{image_name}.tif"
        output_file = f"output/{image_name}_raw.json"
    else:
        image_file = f"imgs/{image_name}"
        output_file = f"output/{image_name}".replace('.tif', '_raw.json')

    # --- Extract and save SEM metadata ---
    SEM_metadata = SEMMetaData()

    # Process image
    img = SEM_metadata.OpenCheckImage(image_file)
    SEM_metadata.ImageMetadata(img)

    # Extract standard EXIF metadata
    exif_keys, exif_number = SEM_metadata.SEMEXIF()
    found_exif_metadata, none_exif_metadata = SEM_metadata.GetExifMetadata(img, exif_keys, exif_number)
    exif_dict = SEM_metadata.ExifMetaDict(found_exif_metadata, none_exif_metadata)

    # Extract SEM instrument metadata (from tag 34118)
    metadata_list = SEM_metadata.GetInsMetadata()
    sem_inst_dict = SEM_metadata.InsMetaDict(metadata_list)

    # Combine both dictionaries (EXIF + SEM instrument metadata)
    complete_metadata_dict = {**exif_dict, **sem_inst_dict}

    # Save to JSON
    SEM_metadata.WriteSEMJson(output_file, complete_metadata_dict)
    print(f"Metadata saved to {output_file}")

    # --- Clean the JSON file ---
    json_cleaner = JsonCleaner(output_file)
    json_cleaner.clean_json()

    # Update the output file path to the cleaned version
    output_file = output_file.replace("_raw.json", "_cleaned.json")

    # --- Visualize the features ---
    visualize_features(output_file, image_file)


if __name__ == "__main__":
    main()
