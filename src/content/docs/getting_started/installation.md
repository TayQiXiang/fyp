---
title: Installation Guide
description: The guide for Vitrox AI Similarity Search
---

We recommend to start in a new conda environment or a new PyTorch docker container.

1. Clone the repository
```sh
git clone <url>
cd FIRe
```

2. Create new conda environment
```sh
conda deactivate
conda create -n image python=3.8 -y
conda activate fast-image-retrieval
```

3. Install the required packages
```sh
pip install -r requirements.txt
# faiss gpu version, or `faiss-cpu` for cpu-only version
./init.sh
conda install -c pytorch faiss-gpu -y
```