{
    "filename": "image1.jpg",
    "description": "null",
    "tags": None,
    "width": 1920,
    "height": 1080
}

from json_cleaner_module import JsonCleaner

cleaner = JsonCleaner("output/image_raw_test.json")
cleaner.clean_json()
{
    "filename": "image1.jpg",
    "width": 1920,
    "height": 1080
}
