#!/bin/bash
#initialise enviroment
source activate fast-image-retrieval

#install dependencies
sudo apt-get install ffmpeg libsm6 libxext6  -y
sudo apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
sudo apt-get install libgl1 -y
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok