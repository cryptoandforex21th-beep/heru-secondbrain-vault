import requests
import json
import os

with open("d:\\SecondBrain\\00_system\\sketchfab_dl.json", "r") as f:
    dl_data = json.load(f)

glb_url = dl_data["glb"]["url"]
target_dir = r"d:\SecondBrain\01_knowledge\projects\virtual_ai_office\public\models"
os.makedirs(target_dir, exist_ok=True)
target_path = os.path.join(target_dir, "mario_kart_ac_spring.glb")

print(f"Downloading Mario Kart 8 AC Spring GLB ({dl_data['glb']['size'] / 1024 / 1024:.2f} MB)...")
print("Target:", target_path)

resp = requests.get(glb_url, stream=True)
if resp.status_code == 200:
    total_downloaded = 0
    with open(target_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                total_downloaded += len(chunk)
                print(f"Downloaded: {total_downloaded / 1024 / 1024:.2f} MB", end="\r")
    print("\nSUCCESS! Downloaded completely.")
else:
    print("Download failed with status:", resp.status_code)
