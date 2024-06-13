---
title : "Inference trained model"
sidebar:
# Set a custom order for the link (lower numbers are displayed higher up)
  order: 2
---
We provide simple Web Interface for Inference that can be a good showcase or demo for trained model. 
This interface allows making simple inference on trained image retrieval model. 
By uploading a query image, it will return top k the nearest image from the database index.
This web interface is created with Flask framework and is very easy to use.

To start with this inference
1. Run the following command on the root of project:
    ```shell
    python inference.py --dir logs/orthocos_alexnet_orthohash_128_imagenet100_100_0.0001_adam/002_test_0 --device cuda:0 --k 10 --ip 0.0.0.0 --port 8000
    ```
   Note that `--dir` is required field, `--device`, `--k`, `--ip` and `--port` is optional.
    ```{note}
    First run will be slow, this is because we had to create index for all images in database, and is recommend to run with GPU. A decent GPU took less than 10 minutes. After that, the index will be stored in the log directory for future use.
    ```
2. Head to `http://<your ip address>:<port>`. By default, it is at http://localhost:8000/
3. Drag an image to the white box area and click on `Upload File`.
4. Here you go.
   