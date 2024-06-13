---
title : "Custom Dataset"
sidebar:
# Set a custom order for the link (lower numbers are displayed higher up)
  order: 3
---

In `utils/datasets.py`, create a Dataset class for your custom dataset. Make sure return `image, class_id, and index_id` for each item.
```python
from torch.utils.data.dataset import Dataset


class ImageDataset(Dataset):
    def __init__(self, ...):
        self.data = ..
        pass
    def __getitem__(self, index):
        return image, class_id, index
    def __len__(self):
        return len(data)
```
In the same file, create a dataset-specific method for your custom dataset. For example:
```python
def new_dataset(**kwargs):
    transform = kwargs['transform']
    filename = kwargs['filename']
    suffix = kwargs.get('dataset_name_suffix', '')

    d = ImageDataset(f'data/imagenet{suffix}', transform=transform, filename=filename, ratio=kwargs.get('ratio', 1))
    return d
```
In `configs.py:289`, specify your dataset name and link it to the dataset method you have created, for example:
```python
datafunc = {
    'imagenet100': datasets.imagenet100,
    .
    .
    'new_dataset': datasets.new_dataset  # new dataset
}[dataset_name]
```
In the same `configs.py` file, at line `configs.py:53` specify the image size to resize. For example:
```python
r = {
    'imagenet100': 256,
    .
    .
    'new_dataset': 512 # new dataset resize size
}
```
At line `configs.py:80`, specify the crop size. For example:
```python
r = {
    'imagenet100': 224,
    .
    .
    'new_dataset': 486 # new dataset crop size
}
```
```{note}
The image is first resize then only crop. However, it could depends on how you specify the augmentation for your dataset, which will be introduct later in this section.
```
At line `configs.py:108`, specify the number of class for your dataset. For example:
```python
r = {
    'imagenet100': 100,
    .
    .
    'new_dataset': 10 # new dataset number of class
}
```
At line `configs.py:129`, specify the default number of image to retrieve per query (R). For example:
```python
r = {
    'imagenet100': 100,
    .
    .
    'new_dataset': 10 # new dataset default R
}
```
At line `configs.py:281`, add the dataset name to the conditon as follow:
```python
if dataset_name in ['imagenet100', 'nuswide', 'new_dataset']:
```
In `constants.py:datasets`, add the dataset name, for example:
```python
datasets = {
    'class': ['imagenet100', 'new_dataset'],
    'multiclass': ['nuswide'],
}
```
Lastly, in the another file at line `utils/augmentations.py:19`, in the method `get_train_transform`, specify the augmentation. For example:
```python
'nuswide': [
    transforms.Resize(resize),
    transforms.RandomCrop(crop),
    transforms.RandomHorizontalFlip()
],
'new_dataset': [
    transforms.RandomResizedCrop(crop),
    transforms.RandomHorizontalFlip()
],
```