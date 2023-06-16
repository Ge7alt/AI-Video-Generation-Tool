import os
import requests
import time



def nepali_tts(text, output_path):

    # API endpoint URLs
    convert_url = "https://play.ht/api/v1/convert"
    status_url = "https://play.ht/api/v1/articleStatus"

    # Folder path containing text data files
    # text_data_folder = "D:\Fuse Intershio\TTS_API\Text_data_2"  # Folder path relative to your project's root directory

    # Authentication headers
    headers = {
        "accept": "application/json",
        "AUTHORIZATION": "03739481295a41a89599c4544431de3b",
        "X-USER-ID": "7xqx3xESXNcE9rRmm202wu43hj92"
    }

    # Create the output directory if it doesn't exist
    # output_dir = "D:/Fuse Intershio/TTS_API/audio_results"  # Directory path relative to your project's root directory




    # #Iterate over the text files in the folder
    with open(text, "r", encoding="utf-8") as file:
        content = file.read().strip()

    # Payload for the POST request
    payload = {
        "content": [content],
        "voice": "ne-NP-SagarNeural",
        #"globalSpeed": "80%"
    }

    # Send the POST request to convert text to audio
    response = requests.post(convert_url, json=payload, headers=headers)
    print(response.text)

    response.raise_for_status()

    # Extract the transcription ID from the response
    response_data = response.json()
    transcription_id = response_data["transcriptionId"]
    print(transcription_id)

    # Construct the URL for the GET request to check the status
    status_request_url = f"{status_url}?transcriptionId={transcription_id}"

    # Check the status periodically until audio is ready
    audio_url = None
    while audio_url is None:
        response = requests.get(status_request_url, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        message = response_data["message"]

        if message == "Transcription completed":
            audio_url = response_data["audioUrl"]
        # elif status == "ERROR":
        #     print(f"Error occurred for transcription ID: {transcription_id}")
        #     break
        else:
            print("Transcription still in progress. Waiting...")
            time.sleep(5)  # Wait for 5 seconds before checking again

    if audio_url:
        # Download the audio file
        audio_response = requests.get(audio_url)
        audio_response.raise_for_status()

        
        # Save the audio file
        # output_path = os.path.join(output_dir, f"{file_name}.mp3")
        with open(output_path, "wb") as file:
            file.write(audio_response.content)

        # print(f"Audio file downloaded and saved: {output_path}")
        
        return output_path