#write python class that read a .tif file
#write python class that read a .tif file
import os, sys, glob
import matplotlib.pyplot as plt
import glob 
import numpy as np
from PIL import Image, ExifTags #Image processing and metadata
import json
import pathlib
# Class Initialization

class SEMMetaData:
    def __init__(self, image_metadata={}, semext=('tif','TIF'), semInsTag=[34118]):
        # semext is a tuple corresponding to the valid extension
        # 34118 is a TIFF tag often used by SEM instruments to store extra data
        self.semext = semext
        self.image_metadata = image_metadata
        self.semInsTag = semInsTag
        self.image_tags = np.array([])

    def OpenCheckImage(self,image):
        """
        Opens an image file with PILLOW library (Image.open()) and verifies accessibility and format (.tif or .TIF)
        return the opened image object if succesful
        """
        img = Image.open(image)
        return img



    def ImageMetadata(self, img):
        """
        Extracts raw metadata from image,
        including tag identifiers 34118
        tip: use img.tag
        """

        self.image_metadata = img.tag
        self.image_tags = np.array(self.image_metadata)
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
        tag_id = 34118  # instrument-specific SEM metadata tag

        # Check if tag 34118 exists
        if tag_id not in self.image_metadata:
            print(" Tag 34118 not found in this image.")
            return []

        # Extract raw metadata bytes
        raw_data = self.image_metadata[tag_id]

        # Convert to string safely (SEM metadata often stored as bytes)
        if isinstance(raw_data, (bytes, bytearray)):
            try:
                text_data = raw_data.decode("utf-8", errors="replace")
            except Exception:
                text_data = str(raw_data)
        else:
            text_data = str(raw_data)

        # Clean up the text
        text_data = text_data.replace("\r", "").replace("\x00", "").strip()

        # Split into lines if metadata has multiple entries
        metadata_lines = [line.strip() for line in text_data.splitlines() if line.strip()]

        return metadata_lines
        

    def InsMetaDict(self, meta_list):
        """
        Converts a flat list of instrument metadata (from tag 34118)
        into a structured dictionary.

        Returns:
            - dict: Parsed instrument metadata key-value pairs.
            - Empty dict if parsing fails or list is invalid.
        """
        if not meta_list or not isinstance(meta_list, list):
            print("Invalid or empty metadata list provided to InsMetaDict().")
            return {}

        meta_dict = {}

        try:
            for item in meta_list:
                # Clean line: remove nulls, extra spaces, etc.
                clean_line = item.strip().replace("\x00", "")
                if not clean_line:
                    continue

                # Try splitting on common separators
                if "=" in clean_line:
                    key, value = clean_line.split("=", 1)
                elif ":" in clean_line:
                    key, value = clean_line.split(":", 1)
                else:
                    # If no separator, skip or store as 'Unknown_n'
                    key, value = f"Unknown_{len(meta_dict)+1}", clean_line

                # Clean key and value strings
                key = key.strip().strip(";")
                value = value.strip().strip(";")

                meta_dict[key] = value

        except Exception as e:
            print(f"Error parsing instrument metadata: {e}")
            return {}

        return meta_dict


    # Open file in write mode and Export SEM Metadata to JSON Format with json.dump
    def WriteSEMJson(self,file, semdict):
        with open(file, "w") as semoutfile:
            json.dump(semdict, semoutfile)
            return
