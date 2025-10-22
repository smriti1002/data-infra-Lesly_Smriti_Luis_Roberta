#write python class that read a .tif file
#write python class that read a .tif file
import os, sys, glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ExifTags #Image processing and metadata
import json

# Class Initialization

class SEMMetaData:
    def __init__(self, image_metadata={}, semext=('tif','TIF'), semInsTag=[34118]):
        #semext is a tuple corresponding to the valid extension, 34118 is a TIFF tag ofte used by SEM instruments to store extra data
        #define  the following attributes: semext, image_megadata, semInsTag, images_tags (array to store image tag values)



    def OpenCheckImage(self, image):
        """
        Opens an image file with PILLOW library (Image.open()) and verifies accessibility and format (.tif or .TIF)
        return the opened image object if succesful
        """


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


    def InsMetaDict(self, list):   

        '''
        write  function that converts a flat list of instrument metadata into a structured dictionary.
        Returns:
            - dict: of all the information contained in the 34118 tag  
            - and an empty dictionary if parsing fails.  
     
        '''

    # Open file in write mode and Export SEM Metadata to JSON Format with json.dump
    def WriteSEMJson(self,file, semdict):
        with open(file, "w") as semoutfile:
            json.dump(semdict, semoutfile)
        return
