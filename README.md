# AI Image File Renamer

This Python script leverages the power of Google's Generative AI to automate the renaming of image files based on their content. It analyzes each image, suggests a relevant filename in the format `<category> - <short Description>`, and renames the file while maintaining consistency with existing filenames.

## Features

- **AI-Powered Renaming:** Uses Google Generative AI (`Gemini-1.5-Flash`) to analyze image content and suggest appropriate filenames.
- **Customization:** Easily tailor the filename format, and the initial chat instructions for the model to fit your preferences.
- **Organized:** Moves renamed images into a subdirectory (`AutoNamed`) for better organization.
- **Pause/Resume:** Use the SPACEBAR to pause and resume the renaming process.
- **Error Handling:** Includes mechanisms to handle common errors like missing files and permissions.

## Prerequisites

1. **Google Cloud Project:** Create a project in [Google AI Studio - API Keys](https://aistudio.google.com/app/apikey) and obtain the required API key.
2. **Python Environment:** Have preinstalled Python Environment
3. **Image Files:** The images you want to rename are in the specified directory.

## Installation

1. **Clone or download the script file.**
	`AI_image_renamer.py`

2. **Install dependencies:**
	```
	pip install google-generativeai keyboard
	```

## Usage
1. **Replace Placeholders:**
Open the script and replace the following:
- `TODO: INSERT YOUR API KEY` with your.
- Optional: `TODO: <insert your sample here>` with your sample file naming convention to train the model.
- `TODO <insert your image folder path here>` with the path to your images folder. You may need to Use `\\` instead of `\`.
   
2. **Run the script:**
	```
	python AI\image\renamer.py
	```

3. **Sit and watch the fun:**
- The script displays the AI-generated filenames and stats.
- Watch the renamed files in `AutoNamed` subfolder.
- Hold SPACEBAR to pause/resume.

> [!TIP]
> 1. Do you need different start prompts? Use [Google AI Studio - Prompt Builder]([https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/prompts/new_chat))  `Create new prompt` and `Get Code` and replace the `chat_session = model.start_chat(history=[])` history.
> 
> 2. Also you can customise the per image file prompt here: `response = chat_session.send_message()` 

## Configuration (Optional)

- **Model Parameters:** Adjust the `generation\config settings` (temperature, top\p, top\k, etc.) to influence the AI's suggestions. 
- **Safety Settings:** Enable/disable safety filters in the `safety\settings`.

## Disclaimer

- **API Usage:** This script will consume credits from your Google Cloud Project's API usage.
- **AI Limitations:** While the AI strives for accuracy, its suggestions might not always be perfect. Please review them carefully.

**Note:** Always keep a backup of your original images before running this script.

