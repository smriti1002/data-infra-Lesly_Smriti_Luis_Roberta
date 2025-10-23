from semmeta.metadata_extractor_module import SEMMetaData
import os
import json
def main():
    # Create object
    sem_reader = SEMMetaData()
    # Example image
    image_path = "/home/ubuntu/data-infra-Lesly_Smriti_Luis_Roberta/imgs/LIL test_defect02.tif"
    # Open the image
    img = sem_reader.OpenCheckImage(image_path)
    print("Image opened successfully.")

    # Extract metadata
    image_metadata, tags = sem_reader.ImageMetadata(img)
    #print("Extracted metadata tags:", tags)
    print("Extracted metadata tags:", image_metadata)
  
    # === 6️⃣ Extract EXIF tag mappings and metadata ===
    exif_keys, exif_numbers = sem_reader.SEMEXIF()
    found_exif, missing_exif = sem_reader.GetExifMetadata(img, exif_keys, exif_numbers)
    exif_dict = sem_reader.ExifMetaDict(found_exif, missing_exif)

    # === 7️⃣ Extract SEM instrument-specific metadata ===
    ins_metadata_list = sem_reader.GetInsMetadata()
    ins_metadata_dict = sem_reader.InsMetaDict(ins_metadata_list)

    # === 8️⃣ Merge EXIF and Instrument Metadata ===
    combined_metadata = {
        "FileName": os.path.basename(image_path),
        "EXIF_Metadata": exif_dict,
        "Instrument_Metadata": ins_metadata_dict,
    }

    # === 9 Print summary to console ===
    print("\n🔬 Extracted Instrument Metadata:")
    for k, v in ins_metadata_dict.items():
        print(f"  {k}: {v}")

    # === 10 Write combined metadata to JSON ===
    output_json = os.path.splitext(image_path)[0] + "_metadata.json"
    with open(output_json, "w") as f:
        json.dump(combined_metadata, f, indent=4)
    print(f"\n Metadata successfully saved to: {output_json}")

if __name__ == "__main__":
    main()



