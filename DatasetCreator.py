import torch
from torchvision import transforms
from torch.utils.data import Dataset
import pandas as pd
import requests
import numpy as np
import PIL 

class MyDataset(Dataset):
    def __init__(self, image_paths, labels, transforms=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transforms = transforms

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        image_url = self.image_paths[index]
        label = self.labels[index]
        try:
            response = requests.get(image_url,stream=True)
            response.raise_for_status()
            #convert image to PIL format
            image = PIL.Image.open(response.raw).convert('RGB')

            #apply transformation if provided
            if self.transforms:
                image = self.transforms(image)

            #convert to Tensor
            image = torch.from_numpy(np.array(image))
            return image, label
        except Exception as e:
            print(f"Error downloading image {image_url}: {e}")
            return None, None
            

df = pd.read_excel("Diwali Outfits.xlsx")

image_paths = df.iloc[:,0]
labels = ["Diwali" for i in range(len(image_paths))]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# print(len(image_paths))
dataset = MyDataset(image_paths, labels, transform)
# Create dataloader
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
# print(len(dataloader))
# for i, l in dataloader:
    # print(i, l)
# Use your dataset in your training loop
# for images, labels in dataloader:
    # Your training logic here
    # ...

