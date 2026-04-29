from PIL import Image
import sys

def invert_image_colors(input_path, output_path):
    try:
        # Open the image
        image = Image.open(input_path)

        # Convert to RGB if not already (handles grayscale, black/white, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Invert the colors
        inverted_image = Image.eval(image, lambda x: 255 - x)

        # Save the inverted image
        inverted_image.save(output_path)
        print(f"Inverted image saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python invert_colors.py <input_image_path> <output_image_path>")
    else:
        invert_image_colors(sys.argv[1], sys.argv[2])