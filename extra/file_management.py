import os

def create_directories(base_path):
    try:
        print(base_path)
        # Create main folders
        sub_paths = ["captures", "logs", "dupes", "detected"]
        for sub_path in sub_paths:
            os.makedirs(os.path.join(base_path,"deer", sub_path), exist_ok=True)
        
        # Create animal-specific subfolders inside 'detected'
        folder_names = ["class", "no_class"]
        detected_path = os.path.join(base_path, "deer/detected")
        for folders in folder_names:
            os.makedirs(os.path.join(detected_path, folders), exist_ok=True)
            
    except Exception as e:
        print(f"Failed to create directories: {e}")
        raise RuntimeError(f"Failed to create directories: {e}") from e

if __name__ == "__main__":
    base_dir = "/home/rpi3/Downloads/deer_deterrant"
    create_directories(base_dir)
