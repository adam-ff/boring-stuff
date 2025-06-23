#!/bin/sh
apt install git-all curl ffmpeg -y;
curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh;
bash Miniconda3-latest-Linux-x86_64.sh -b -p "${HOME}/miniconda3";
source "${HOME}/miniconda3/bin/activate";
conda init --all;
source "${HOME}/.bashrc";
conda create --name facefusion python=3.12 pip=25.0 -y;
source "${HOME}/miniconda3/bin/activate facefusion";
conda install conda-forge::cuda-runtime=12.8.1 conda-forge::cudnn=9.8.0.87 -y;
git clone https://github.com/facefusion/facefusion;
cd facefusion;
python install.py --onnxruntime cuda;
conda deactivate;
source $HOME/miniconda3/bin/activate facefusion;
wget $S_URL -O "/workspace/facefusion/facefusion/${S_FILE}";
python facefusion.py run;
