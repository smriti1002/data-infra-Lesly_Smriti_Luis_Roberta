# 🧩 Group Exercise — Image Processing Pipeline with Git and Python

## 🎯 Objective
In this exercise, you will work in a **group of three students** to build a simple **data processing pipeline** using Python and GitHub.  
Each student will be responsible for one part of the workflow — from reading an image and converting it to JSON, to extracting features, and finally visualizing results.

---

## 🧑‍🤝‍🧑 Group Setup

1. **Create a GitHub repository** for your group project.  
   - The repository name should follow this format:  
     ```
     data-infra-name-of-the-group
     ``` 

2. They push the cloned content to their group repo:

   - git remote remove origin
   - git remote add origin https://github.com/...../data-infra-name-of-the-group.git
   - git push -u origin main

3. Each student should:
   - **Clone** the repository.
   - **Create and work on their own branch**, named according to their assigned task:
     - `metadata_extractor_module`
     - `json_cleaner_module`
     - `visualizer_module`

---

## 🧠 Tasks

### 🧩 Task 1 — Metadata Extractor Module

**Responsible student:** Branch `metadata_extractor_module`

1. Update semmeta/metadata_extractor_module.py in order to define a **Python class** that:
   - Reads the `name_of_image.tif` image from imgs folder, extracts the image metadata and save a json file into the repository (e.g., `output/name_of_image_raw.json`).
   - The images given are from electron microscopy in a specific format. Since this task is highly specific, the metadata_extractor_module is already partially given, and the student has to fill uncompomplete functions as indicated


---

### 🧩 Task 2 — Json Cleaner Module

**Responsible student:** Branch `json_cleaner_module`

1. Update the semmeta/json_cleaner_module.py in order to write a **Python class** that:
  
   - Reads the `output/name_of_image_raw.json` file created in Task 1.
   - Filters out all features whose values are `"null"` or `None`.
   - Saves the new cleaned JSON file as `output/name_of_image_cleaned.json`.

2. Test your code with output/image_raw_test.josn and check that the output is a text with keys and values

**Suggested libraries:** `json`, `pandas`

---

### 🧩 Task 3 — Extraction and Visualization

**Responsible student:** Branch `visualizer_module`

1. Update semmeta/visualizer_module.py  in order to write **Python script or class** that:
   - From `output/name_of_image_cleaned.json` extract the following features: AP_WD; AP_BEAM_TIME; AP_IMAGE_PIXEL_SIZE; AP_HOLDER_HEIGHT, AP_BEAM_CURRENT, AP_HOLDER_DIAMETER
   - Plots the original `.tif` image.
   - Displays a table (or printed DataFrame) showing the **keys and values** of the extracted features in three columns corresponding to: variables, values, units.
  
2. Test yout code using output/images_cleaned_test.json
  
**Suggested libraries:** `matplotlib`, `pandas`, `Pillow`
  
### 🧩 Final Task (Collective) — Execution



1. Write a main.py file to write a function that allows executing the program by: 
   - asking for the name of the `name_of_image.tif` file** as input (e.g., via `input()` or a command-line argument).
   - calling all modules from previous tasks.

2. Merge all the branches in the main branch and test the exuction



---

## 🔄 Collaboration and Integration

- Each student works independently on their branch.
- After finishing, open a **Pull Request** to merge your branch into the main branch.
- Review each other’s code before merging.
- Ensure that the final main branch contains a **complete, working pipeline**.

---



