import os
import time

folder = r"E:\others\Music\Piano_Keys"
x = 1
for filename in os.listdir(folder):
    name, ext = os.path.splitext(filename)
    new_name = f"{name.upper()}{ext.lower()}"
    
    old_path = os.path.join(folder, filename)
    temp_path = os.path.join(folder, f"temp_{x}.tmp")
    new_path = os.path.join(folder, new_name)

    if old_path != new_path:
        try:
            os.rename(old_path, temp_path)   # Rename to temp first
            os.rename(temp_path, new_path)   # Then to final
            print(f"Renamed {x}/227 to {new_name}")
        except Exception as e:
            print(f"[!] Failed on {filename}: {e}")
        time.sleep(0.05)
    
    x += 1

print("Renaming complete!")
