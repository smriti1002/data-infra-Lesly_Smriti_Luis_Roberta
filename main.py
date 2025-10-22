from semmeta.visualizer_module import visualize_features
from semmeta.metadata_extractor_module import SEMMetaData
from semmeta.json_cleaner_module import JsonCleaner


def main():
    
    # Request the name of the image from the user
    image_name = input("Enter the name of the image, no path (e.g., 12_50_vero_09): ").strip()
    
    # Initialize variable for image and output paths and populate them
    image_file = None
    output_file = None
    if not image_name.endswith(".tif"):
        image_file = f"imgs/{image_name}.tif"
        output_file = f"output/{image_name}_raw.json"
    else:
        image_file = f"imgs/{image_name}"
        output_file = f"output/{image_name}".replace('.tif', '_raw.json')

    # Process image metadata and save it into a json file in the output folder
    # Initialize SEMMetaData object
    SEM_metadata = SEMMetaData()

    # Process image
    img = SEM_metadata.OpenCheckImage(image_file)
    SEM_metadata.ImageMetadata(img)

    # Extract SEM instrument metadata
    metadata_list = SEM_metadata.GetInsMetadata()
    metadata_dict = SEM_metadata.InsMetaDict(metadata_list)

    # Save to JSON
    SEM_metadata.WriteSEMJson(output_file, metadata_dict)
    print(f"Metadata saved to {output_file}")
    
    # Clean the json file
    # !Smirti
    # todo: use the class correctly
    # the steps below assumes that the JsonCleaner creates directly the cleaned json file in the output folder
    json_cleaner = JsonCleaner()
    json_cleaner.clean_json(output_file)
    output_file = output_file.replace('raw', 'cleaned')
    # ...
    
    # Visualize the features
    # !Luis
    # it is already working
    visualize_features(output_file, image_file)

if __name__ == "__main__":
    main()