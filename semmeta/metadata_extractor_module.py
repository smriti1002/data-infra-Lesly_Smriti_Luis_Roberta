#write python class that read a .tif file
from PIL import Image, ExifTags #Image processing and metadata
import json

# Class Initialization

class SEMMetaData:
    def __init__(self, image_metadata={}, semext=('tif','TIF'), semInsTag=[34118]):
        #semext is a tuple corresponding to the valid extension, 34118 is a TIFF tag often used by SEM instruments to store extra data
        #define  the following attributes: semext, image_megadata, semInsTag, images_tags (array to store image tag values)
        self.semext = semext 
        self.image_metadata = image_metadata
        self.semInsTag = semInsTag 

    def OpenCheckImage(self, image):
        """
        Opens an image file with PILLOW library (Image.open()) and verifies accessibility and format (.tif or .TIF)
        return the opened image object if succesful
        """
        img=Image.open(image)
        return img
        

    def ImageMetadata(self, img):
        """
        Extracts raw metadata from image,
        including tag identifiers 34118
        tip: use img.tag
        """

        self.image_metadata = img.tag
        # Store tags as a list for membership testing
        self.image_tags = list(self.image_metadata.keys())
        return self.image_metadata, self.image_tags


    def SEMEXIF(self):

        """
        Provides access to standard EXIF tag mappings from PIL.

        Returns:
            - exif_keys (list): Human-readable EXIF tag names
            - exif_number (list): Corresponding numeric tag identifiers used in image metadata.
        """
        # Get the PIL EXIF tag dictionary to map names to numeric keys
        exif_dict = {k: v for v, k in ExifTags.TAGS.items()}
        # or
        #exif_dict = dict([ (k, v) for v, k in ExifTags.TAGS.items() ])

        # Extract all tag names (keys) from the reversed dictionary
        exif_keys = [key for key in exif_dict]

        # Extract corresponding numeric identifiers for each tag name
        exif_number = [exif_dict[k] for k in exif_keys]
        return exif_keys, exif_number

    # Extract Standard EXIF Metadata from SEM Image


    def GetExifMetadata(self, img, exif_keys, exif_number):

        """
        Extracts standard EXIF metadata from a SEM image.
        """

        # based on std EXIF TAGS (from PIL), we store exif metadata in found_exif_metadata variable
        found_exif_metadata=[(img.tag[idx][:], word) for idx, word in zip(exif_number, exif_keys) if idx in self.image_tags]

        # if the key is not available in the image save its value as none
        none_exif_metadata = [(word, None) for num, word in zip(exif_number, exif_keys)  if num not in self.image_tags]
        return found_exif_metadata, none_exif_metadata

    # Construct Unified EXIF Metadata Dictionary
    def ExifMetaDict(self, found_exif_metadata, none_exif_metadata):

        """
        Creates a unified dictionary from found and missing EXIF metadata entries.
        Returns:
            - dict: Combined dictionary of EXIF metadata, excluding 'ColorMap' entries.
        """

        found_metadict = dict((subl[1], subl[0][0]) for subl in found_exif_metadata if subl[1]!="ColorMap")
        none_metadict = dict((subl[0], subl[1]) for subl in none_exif_metadata if subl[0]!="ColorMap")
        allexif_metadict = {**found_metadict, **none_metadict}
        return allexif_metadict


    def GetInsMetadata(self):

        '''
        Extracts instrument-specific metadata from SEM image EXIF tag 34118.
        Returns:
            - list: a cleaned and escaped list of instrument metadata strings.
            - and an empty list if tag 34118 is not found.
        '''
        
        if not hasattr(self, "image_metadata") or not self.image_metadata:
            print("No metadata found. Run ImageMetadata(img) first.")
            return []
        
        tag_id = 34118
        if tag_id not in self.image_metadata:
            print(f"Tag {tag_id} not found.")
            return []

        data = self.image_metadata[tag_id]

        # Some PIL tags can be returned as tuples/lists (e.g., (b"...",)) or arrays.
        # Normalize to a single value first.
        if isinstance(data, (tuple, list)) and len(data) > 0:
            data = data[0]

        # If it's a bytes-like object, decode to string
        if isinstance(data, bytes):
            data = data.decode(errors="ignore")

        # If it's an object with tobytes method, try to decode that
        if hasattr(data, 'tobytes') and not isinstance(data, (str, bytes)):
            try:
                data = data.tobytes().decode(errors="ignore")
            except Exception:
                data = str(data)

        # As a final fallback, ensure we have a string
        if not isinstance(data, str):
            data = str(data)

        # Clean up unwanted characters and split into a list
        # Replace null bytes with spaces, then split by line breaks
        cleaned = data.replace("\x00", " ").strip()
        # Split by both \r\n and \n to handle different line ending formats
        metadata_list = [item.strip() for item in cleaned.replace("\r\n", "\n").split("\n") if item.strip()]
        return metadata_list

        



    def InsMetaDict(self, metadata_list):   
        '''
        Converts a flat list of instrument metadata into a structured dictionary.
        The metadata comes in pairs: tag identifier followed by "key = value" string.
        Returns:
            - dict: all information contained in the 34118 tag  
            - empty dictionary if parsing fails
        '''
        if not metadata_list or not isinstance(metadata_list, list):
            print("No valid metadata list provided.")
            return {}

        meta_dict = {}
        i = 0
        while i < len(metadata_list):
            current_line = metadata_list[i]
            
            # Check if this is a tag identifier (doesn't contain "=")
            if "=" not in current_line and i + 1 < len(metadata_list):
                # This is a tag identifier, next line should be the value
                tag_identifier = current_line.strip()
                value = metadata_list[i + 1].strip()
                meta_dict[tag_identifier] = value
                i += 2  # Skip both lines
            else:
                # Standalone line with "=" or last line without pair
                if "=" in current_line:
                    key, value = current_line.split("=", 1)
                    meta_dict[key.strip()] = value.strip()
                i += 1

        return meta_dict


    def WriteSEMJson(self, file, semdict):
        """
        Open file in write mode and export SEM metadata to JSON format
        """
        with open(file, "w") as semoutfile:
            json.dump(semdict, semoutfile, indent=4)  # indent per renderlo leggibile
        print(f"SEM metadata saved to {file}")
        return
