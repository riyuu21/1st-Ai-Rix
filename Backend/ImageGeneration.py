import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display images
def open_images(prompt):
    folder_path = r"Data"
    clean_prompt = prompt.replace(" ", "_")

    files = [f"{clean_prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            continue

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except Exception as e:
            print(f"Unable to open {image_path}: {e}")

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIkey')}"}

# Query HuggingFace API with retries
async def query(payload):
    for attempt in range(5):  # retry up to 5 times
        response = await asyncio.to_thread(
            requests.post,
            API_URL,
            headers=headers,
            json=payload
        )

        content_type = response.headers.get("content-type", "")

        if "image" in content_type:
            return response.content

        error_message = response.text
        print("API Response:", error_message)

        if "loading" in error_message.lower():
            print(f"Model loading... retrying in 1 seconds (attempt {attempt+1}/5)")
            await asyncio.sleep(1)  # async sleep so other tasks can run
        else:
            return None
    return None

# Generate images
async def generate_images(prompt: str):
    clean_prompt = prompt.replace(" ", "_")
    tasks = []

    for _ in range(1):
        payload = {"inputs": f"{prompt}, 4k, ultra detailed, high resolution, seed={randint(0,1000000)}"}
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes is None:
            print(f"Image {i+1} failed.")
            continue

        file_path = fr"Data\{clean_prompt}{i+1}.jpg"
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        print("Saved:", file_path)

# Wrapper
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Listener loop
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read().strip()

        if not Data:
            sleep(1)
            continue

        parts = Data.split()
        Status = parts[-1]
        prompt = " ".join(parts[:-1])

        if Status == "True":
            print("Generating Images...")
            GenerateImages(prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write(f"{prompt} False")

            break
        else:
            sleep(1)

    except Exception as e:
        print("Error:", e)
        sleep(1)
