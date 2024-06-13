---
title: "Custom Dataset Configuration"
---


1. One hot encoding 
   
   Image path - one hot encoded label

   Example:
   ```txt
    data/imagenet/image/image1.png 0 0 0 0 1
    data/imagenet/image/image2.png 0 0 0 1 0
    data/imagenet/image/image3.png 1 0 0 0 0
    data/imagenet/image/image4.png 0 0 0 0 1

   ```
2. Multi label encoding

   Image path - multi label encoded label

   Example:
   ```txt
    data/imagenet/image/image1.png 0 1 0 1 0
    data/imagenet/image/image2.png 1 0 0 1 0
    data/imagenet/image/image3.png 1 0 0 0 1
    data/imagenet/image/image4.png 0 1 0 1 0

   ```

:::note
Make sure the dataset is stored in the `data/` folder. You should follow the format below

```sh
data/<dataset_name>/image/<image_name>.png <one_hot encoding>
```