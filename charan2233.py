from PIL import Image
import os


def process_image(image_path, mode, key):
    """
    Encrypts or decrypts an image using XOR with the given key.
    Because XOR is symmetric, the SAME function is used for both
    encryption and decryption: (A ^ key) ^ key = A.
    """

    try:
        print(f"\nOpening image from: {image_path}")
        image = Image.open(image_path)

        # Convert image to RGB (standard pixel format)
        image = image.convert("RGB")

        # Load pixel data
        pixels = image.load()
        width, height = image.size

        print("Processing pixels...")

        # Keep key in 0–255 range (one byte)
        k = key & 0xFF

        # Iterate over every pixel in the image
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]

                # XOR with key
                new_r = r ^ k
                new_g = g ^ k
                new_b = b ^ k

                pixels[i, j] = (new_r, new_g, new_b)

        # Prepare autosave filename
        directory, filename = os.path.split(image_path)
        name, ext = os.path.splitext(filename)

        if mode == 1:
            action = "encrypted"
        else:
            action = "decrypted"

        new_filename = f"{name}_{action}.png"
        save_path = os.path.join(directory, new_filename)

        # Autosave the image
        image.save(save_path)
        print(f"\nSuccess! Image saved automatically as: {save_path}")

    except FileNotFoundError:
        print("\nError: The file path you entered could not be found. Please check and try again.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


def main():
    print("=" * 50)
    print("    --- Simple Image Encryption Tool ---")
    print("=" * 50)

    # 1. Take user input for image
    raw_path = input("Enter the path of the image: ").strip()
    image_path = raw_path.replace('"', '').replace("'", "")

    # Check if path exists before proceeding
    if not os.path.exists(image_path):
        print("Error: File does not exist.")
        return

    # 2. Ask user to encrypt or decrypt
    print("\nChoose Operation:")
    print("1. Encrypt")
    print("2. Decrypt")

    try:
        mode_input = input("Enter choice (1 or 2): ").strip()
        mode = int(mode_input)
        if mode not in [1, 2]:
            print("Invalid choice. Please enter 1 or 2.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # 3. Ask user to input the swapping pixel value (key)
    try:
        key_input = input("Enter the swapping pixel value (integer key, e.g., 125): ").strip()
        key = int(key_input)

        if key < 0 or key > 255:
            print("Note: A value between 0 and 255 is recommended for standard 8-bit images.")
    except ValueError:
        print("Invalid input. The value must be an integer.")
        return

    # 4. Run the process
    process_image(image_path, mode, key)


if __name__ == "__main__":
    main()
