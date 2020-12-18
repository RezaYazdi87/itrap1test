import sys
import PIL
from PIL import Image
import torch
input_img=str(sys.argv[1])
################################################
from torchvision import models
resnet = models.resnet101()
################################################
from torchvision import transforms
preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )])

################################################
img = Image.open(input_img)
img_t = preprocess(img)
batch_t = torch.unsqueeze(img_t, 0)
################################################
model_path = 'mymodels/resnet101.tar'
model_data = torch.load(model_path)
resnet.load_state_dict(model_data)
resnet.eval()
###############################################
out = resnet(batch_t)
###############################################
with open('mymodels/imagenet_classes.txt') as f:
    labels = [line.strip() for line in f.readlines()]

_, index = torch.max(out, 1)
percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
print(labels[index[0]], percentage[index[0]].item())
