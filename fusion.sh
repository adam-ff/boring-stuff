#!/bin/bash
apt install git-all curl ffmpeg -y

# Install Miniconda
curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p "${HOME}/miniconda3"

# Add conda to PATH for this session
export PATH="${HOME}/miniconda3/bin:$PATH"

# Initialize conda for future sessions
"${HOME}/miniconda3/bin/conda" init --all

# Create and activate environment using full paths
"${HOME}/miniconda3/bin/conda" create --name facefusion python=3.12 pip=25.0 -y
source "${HOME}/miniconda3/bin/activate" facefusion

# Install dependencies
conda install conda-forge::cuda-runtime=12.8.1 conda-forge::cudnn=9.8.0.87 -y

# Clone and setup facefusion
git clone https://github.com/facefusion/facefusion
cd facefusion
python install.py --onnxruntime cuda

# Download file and run
wget "$S_URL" -O "${S_FILE}"
python facefusion.py run
