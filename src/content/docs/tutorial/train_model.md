---
title : "Train a model"
sidebar:
# Set a custom order for the link (lower numbers are displayed higher up)
  order: 1
---

To train a model, the config(`--config`), dataset(`--ds`), and other parameters(see the usage below) has to be specified, or otherwise the default value will be used. We have included config file for most supported model in `configs/templates`.
```sh
usage: train.py [-h] [--config CONFIG] [--backbone BACKBONE]
                [--ds {imagenet100,nuswide,cifar10,imagenet50a,imagenet50b,cars,cifar10_II,landmark,landmark200,landmark500,gldv2delgembed,roxford5kdelgembed,descriptor,sop,sop_instance,food101,nuswide,coco,mirflickr}]
                [--dfolder DFOLDER] [--c10-ep {1,2}] [--ds-reset] [--usedb] [--train-ratio TRAIN_RATIO] [--nbit NBIT] [--bs BS] [--maxbs MAXBS] [--epochs EPOCHS]
                [--arch ARCH] [--gpu-transform] [--gpu-mean-transform] [--no-aug] [--resize-size RESIZE_SIZE] [--crop-size CROP_SIZE] [--R R]
                [--distance-func {hamming,cosine,euclidean}] [--zero-mean-eval] [--num-worker NUM_WORKER] [--rand-aug]
                [--loss {greedyhash,jmlh,dpn,orthocos,ce,bihalf-supervised,orthoarc,sdhc,csq,adsh,hashnet,dbdh,dpsh,mihash,sdh,dfh,dtsh,greedyhash-unsupervised,bihalf,ssdh,tbh,itq,pca,lsh,sh,imh,cibhash}]
                [--tag TAG] [--seed SEED] [--optim {sgd,adam,rmsprop,adan}] [--loss-params LOSS_PARAMS] [--device DEVICE] [--eval EVAL] [--lr LR] [--wd WD]
                [--step-size STEP_SIZE] [--lr-decay-rate LR_DECAY_RATE] [--scheduler SCHEDULER] [--backbone-lr-scale BACKBONE_LR_SCALE] [--resume]
                [--resume-dir RESUME_DIR] [--enable-checkpoint] [--save-model] [--save-best-model-only] [--discard-hash-outputs] [--load-from LOAD_FROM]
                [--benchmark] [--disable-tqdm] [--hash-bias] [--shuffle-database] [--workers WORKERS] [--train-skip-preprocess] [--db-skip-preprocess]
                [--test-skip-preprocess] [--dataset-name-suffix DATASET_NAME_SUFFIX] [--accimage] [--pin-memory] [--wandb]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       configuration file *.yml
  --backbone BACKBONE   the backbone feature extractor
  --ds {imagenet100,nuswide,cifar10,imagenet50a,imagenet50b,cars,cifar10_II,landmark,landmark200,landmark500,gldv2delgembed,roxford5kdelgembed,descriptor,sop,sop_instance,food101,nuswide,coco,mirflickr}
                        dataset
  --dfolder DFOLDER     data folder
  --c10-ep {1,2}        cifar10 evaluation protocol
  --ds-reset            whether to reset cifar10 txt
  --usedb               make all database images as training data
  --train-ratio TRAIN_RATIO
                        training ratio (useful when usedb is activated)
  --nbit NBIT           number of bits for hash codes
  --bs BS               batch size
  --maxbs MAXBS         maximum batch size for testing, by default it is max(bs * 4, maxbs)
  --epochs EPOCHS       training epochs
  --arch ARCH           architecture for the hash function
  --gpu-transform
  --gpu-mean-transform
  --no-aug              whether to skip augmentation
  --resize-size RESIZE_SIZE
                        Image Resize size before crop
  --crop-size CROP_SIZE
                        Image Crop size. Final image size.
  --R R                 if 0, using default R for specific dataset; -1 for mAP@All
  --distance-func {hamming,cosine,euclidean}
  --zero-mean-eval
  --num-worker NUM_WORKER
                        number of worker for dataloader
  --rand-aug            use random augmentation
  --loss {greedyhash,jmlh,dpn,orthocos,ce,bihalf-supervised,orthoarc,sdhc,csq,adsh,hashnet,dbdh,dpsh,mihash,sdh,dfh,dtsh,greedyhash-unsupervised,bihalf,ssdh,tbh,itq,pca,lsh,sh,imh,cibhash}
  --tag TAG
  --seed SEED
  --optim {sgd,adam,rmsprop,adan}
  --loss-params LOSS_PARAMS
  --device DEVICE       torch.device('?') cpu, cuda:x
  --eval EVAL           total evaluations throughout the training
  --lr LR               learning rate
  --wd WD               weight decay
  --step-size STEP_SIZE
                        relative step size (0~1)
  --lr-decay-rate LR_DECAY_RATE
                        decay rate for lr
  --scheduler SCHEDULER
                        LR Scheduler
  --backbone-lr-scale BACKBONE_LR_SCALE
                        Scale the learning rate of CNN backbone
  --resume
  --resume-dir RESUME_DIR
                        resume dir
  --enable-checkpoint
  --save-model
  --save-best-model-only
  --discard-hash-outputs
  --load-from LOAD_FROM
                        whether to load from a model
  --benchmark           Benchmark mode, determinitic, and no loss
  --disable-tqdm        disable tqdm for less verbose stderr
  --hash-bias           add bias to hash_fc
  --shuffle-database    shuffle database during mAP evaluation
  --workers WORKERS     number of workers
  --train-skip-preprocess
  --db-skip-preprocess
  --test-skip-preprocess
  --dataset-name-suffix DATASET_NAME_SUFFIX
  --accimage            use accimage as backend
  --pin-memory          pin memory
  --wandb               enable wandb logging

```
## Use the config file
You can create a new config file from the provided template. To specify argument(s), you may add `argument_key: argument_value` in the yaml config file. For loss parameters, you may add under the `loss_param` list. For example:
```yaml
loss: orthocos
loss_param:
  loss_param1: value
  loss_param2: value
new_argument: new_argument_value
```
:::caution
Missing of loss params will cause error.
:::


To start the training, you may run the training script at `train.py` with specify the config file and any additional arguments or otherwise the default value will be used. Do note that, the argument specify on the command line will override the value in config file.
```bash
python train.py --config configs/templates/orthocos.yaml --ds cifar10 --nbit 64 --epoch 100
```
:::tip
The priority of arguments is as follow: cli arguments > config file > default value.
:::
Differ from the typical argument, to override the loss parameters, one must specify the argument `--loss-param` with their specific value seperated by colon and semicolon `"key1:value1;key2:value2"` to override the loss parameters(usually the hyper-parameters). For example:
```sh
--loss-param "m:0.4;s:8.0;cent_init:B"
```
```note
Some dataloader problem might occur when `--num-worker` is not set to 0 in Windows and macOS BigSur.
```
When the training task is launched, a log directory will be created. All the trained model(if`--save-model` specified), training loss, database and query codes, checkpoints(if enabled), etc will be stored in this directory. The directory will be created under `logs` directory with `<loss>_<backbone>_<arch>_<nbit>_<ds>_<epoch>_<lr>_<optim>/<order>_<tag>_<seed>` format, for example: 
```yaml
"logs/orthocos_alexnet_orthohash_64_cifar10_100_0.0001_adam/002_test_19084"
```