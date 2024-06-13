---
title : "W&B logging"
sidebar:
  order: 7
---

To enable model logging using [Weight and Bias](https://wandb.ai/), it can be enabled by the command line argument 
`--wandb`. You should also login your account first by `wandb login` if you haven't.
Besides, you can also use `wandb init`.
```bash
python train.py ... --wandb
```