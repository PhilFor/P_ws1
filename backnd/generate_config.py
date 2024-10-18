import os
import json
from PIL import Image
from PIL.ExifTags import TAGS


def format_shutter_speed(shutter_speed_value):
    """Format the shutter speed as a fraction, e.g., 1/32, 1/128."""
    try:
        if isinstance(shutter_speed_value, tuple):
            # Shutter speed is given as a (numerator, denominator) tuple
            numerator, denominator = shutter_speed_value
            return (
                f"1/{int(denominator/numerator)}"
                if numerator != 0
                else "Unknown Shutter Speed"
            )
        else:
            # If the value is a float, convert it to a fraction
            return (
                f"1/{int(1/shutter_speed_value)}"
                if shutter_speed_value != 0
                else "Unknown Shutter Speed"
            )
    except Exception as e:
        return "Unknown Shutter Speed"


def ifd_rational_to_string(value):
    """Convert IFDRational to a string representation."""
    if isinstance(value, tuple):
        numerator, denominator = value
        return f"{numerator}/{denominator}" if denominator != 0 else "Unknown"
    return str(value)


def get_exif_data(image_path):
    """Extract EXIF data from an image."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif() or {}
        exif_info = {}

        # Mapping EXIF tags to their readable names
        for tag, value in exif_data.items():
            decoded_tag = TAGS.get(tag, tag)
            exif_info[decoded_tag] = value

        # Extract specific EXIF data
        camera = exif_info.get("Model", None)
        aperture = exif_info.get("FNumber", None)
        shutter_speed = format_shutter_speed(exif_info.get("ExposureTime", None))

        # Convert values to JSON serializable format
        if aperture is not None:
            aperture = ifd_rational_to_string(aperture)

        return {
            "camera": camera,
            "aperture": aperture,
            "shutter_speed": shutter_speed,
        }

    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
        return None


def generate_config(image_directory, config_file):
    """Generate a config.json file with image data from the specified directory."""
    # Get a list of image files from the specified directory
    image_files = [
        os.path.join(image_directory, f)
        for f in os.listdir(image_directory)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".avif"))
    ]

    # Prepare a list to hold image data
    images_data = []

    # Extract EXIF data from each image
    for image_file in image_files:
        # Get EXIF data for each image
        exif_data = get_exif_data(image_file)

        # Append image data for JSON
        relative_src = os.path.join("\\assets\\photos", os.path.basename(image_file))
        if exif_data:
            images_data.append(
                {
                    "src": relative_src,
                    "camera": (
                        exif_data["camera"] if exif_data["camera"] else "Unknown Camera"
                    ),
                    "aperture": (
                        exif_data["aperture"]
                        if exif_data["aperture"]
                        else "Unknown Aperture"
                    ),
                    "shutter_speed": exif_data["shutter_speed"],
                }
            )
        else:
            images_data.append(
                {
                    "src": relative_src,
                    "camera": "Unknown Camera",
                    "aperture": "Unknown Aperture",
                    "shutter_speed": "Unknown Shutter Speed",
                }
            )

    # Write the image data to the config.json file
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump({"images": images_data}, f, indent=4)

    print(f"Config JSON generated successfully in {config_file}")


# Usage
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_directory = os.path.join(
    root_dir, "assets", "photos"
)  # Directory containing the photos
config_file = "config.json"  # Output config file

generate_config(image_directory, config_file)
