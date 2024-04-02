from pygoogle_image import image as pi
import csv

def download_images(query, limit):
    images = pi.download(query, limit=limit)
    return images

def save_to_csv(images, filename):
    if images is None:
        print("No images downloaded. Exiting.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Image URL', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for image in images:
            writer.writerow({'Image URL': image['image_url'], 'Description': image['description']})

def main():
    query = input("Outfit dataset: ")
    limit = int(input("dataset sample size: "))
    filename = "images.csv"

    # Download images
    images = download_images(query, limit)

    if images:
        filename = input("Enter the filename to save (or press Enter to use default 'images.csv'): ").strip()
        if not filename:
            filename = "images.csv"

        # Save to CSV
        save_to_csv(images, filename)
        print(f"Images downloaded and saved to {filename}.")
    else:
        print("No images downloaded. Exiting.")

if __name__ == "__main__":
    main()
