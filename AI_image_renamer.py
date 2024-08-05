"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""
import os
import pathlib
from re import T
import shutil
import sys
import time
import google.generativeai as genai
import keyboard


# Initialize Google Generative AI client
genai.configure(api_key='TODO: INSERT YOUR API KEY')

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Prime the session
chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "I have large number of images in a folder some I have already renamed. Please see attached for the filename format."\
        "The  filename is formatted as '<category> - <short Description>' where <category> is 1 to 2 words and <short Description> is upto 5 words\n"\
        "This make it easier to find similar images in the directory."\
        "I would like to rename the remaining images in the same format.\n\n"\
        "Once you understand the format, I will start to give you the image file please suggest only the filename.\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please provide me with:\n\n1. **The existing image filenames** (at least a few examples) so I can understand the pattern"\
        "of '<category> - <short Description>' you're using.\n2. **The new image files** you want me to suggest filenames for. \n\n"\
        "With this information, I can help you maintain consistency and make it easier to find your images! \n",
      ],
    },
    {
      "role": "user",
      "parts": [
            "Thank you, Here are existing image filenames:\n\n"\
            "TODO: <insert your sample here>",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I see the pattern you're using. Now, please provide the new image files you'd like me to suggest names for.  I'm ready to help you categorize them! \n",
      ],
    },
  ]
)

#response = chat_session.send_message("INSERT_INPUT_HERE")
#print(response.text)

# ANSI escape sequences for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
GREY = "\033[37m"
RESET = "\033[0m"


def check_spacebar():
    paused = False
    if keyboard.is_pressed('space'):
            print(f"{YELLOW}*****   Paused  - press ENTER to resume{RESET}")
            while keyboard.wait('enter'):
                pass  # Wait until spacebar is pressed again
            print(f"{YELLOW}*****   Resumed - hold SPACEBAR to pause again{RESET}")
            return


def suggest_filename(image_path):
    try:
        # Open the image file
        image_data =  {
        'mime_type': 'image/jpeg',
        'data': pathlib.Path(image_path).read_bytes()
    }       
        start_time = time.time()
        # Use Google Generative AI to suggest a filename based on the image
        #response = model.generate_content(["Suggest a filename for this image. Please output only the file name", image_data])
        aifile = genai.upload_file(image_path)
        response = chat_session.send_message(["Please suggest a filename for this image.\n"\
                                              "1) Please keep it as '<category> - <short Description>' where <category> is 1 to 2 words and <short Description> is upto 5 words\n"\
                                              "2) Please reuse the same <category> as much as possible as per the sample filenames provided or new <category> you create to make the files easy to find in the directory"\
                                              "3) Please output only the file name and nothing else", aifile])


        #print(f"Response '{image_path}': {response}'")
        # Print the current time
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        ai_status = f"    {GREY}AI Response ({response_time} ms): suggest_filename: {response.text}  |  Usage: {response.usage_metadata}{RESET}"
        ai_status = ai_status.replace("\n", " ; ")
        print(ai_status)

        return response.text
    except Exception as e:
        print(f"    {RED}AI Error occurred: {e}{RESET}")




def process_images(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print()
            print("---------------------------------------------------------")
            print(f"{CYAN}{current_time}: Processing file: {filename}{RESET}")
            image_path = os.path.join(directory, filename)
            try:
                suggested_name = suggest_filename(image_path) # Call GenAi to get suggested name
                suggested_name = suggested_name.replace("\n", '')
                if suggested_name:
                    suggested_name = os.path.splitext(suggested_name)[0]  # Remove file extension

                    file_extension = os.path.splitext(filename)[1] # Find the original file extension
                    new_filename = f"{suggested_name}{file_extension}" # Append the original file extension to the suggested name

                    new_path = os.path.join(directory, new_filename)
                    move_path = os.path.join(f"{directory}\\AutoNamed", new_filename)

                    # Rename and move the file to a subdirectory
                    os.rename(image_path, new_path)
            
                    shutil.move(new_path, move_path)
                    print(f"    {GREEN}Renamed '{filename}' to '{new_filename}'{RESET}")
                    check_spacebar()
                    time.sleep(4)
                    check_spacebar()

                else:
                    print(f"    {RED}Skipping renaming for '{filename}' due to an error in filename suggestion.{RESET}")

            except FileNotFoundError:
                print(f"    {RED}Error: The file {image_path} was not found.{RESET}")
            except PermissionError:
                print(f"    {RED}Error: Permission denied while renaming '{filename}'.{RESET}")
            except Exception as e:
                print(f"    {RED}An error occurred while processing '{filename}': {e}{RESET}")    
            print("---------------------------------------------------------")

# Directory containing the images
image_directory = 'TODO <insert your image folder path here>; use \\'

print(f"{YELLOW}*****   Processing images in {image_directory}   *****{RESET}")
print(f"{YELLOW}Hold SPACEBAR to pause...{RESET}")

process_images(image_directory)
print()
print(f"{YELLOW}*****   DONE!   *****{RESET}")

# Wait for ENTER key to be pressed
sys.stdin.readline()
