# ai_ocr
OCR engines for AI agents

## Instructions Overview
After cloning this git folder, cd into folder and run each step below in sequence.

## 1. Installation For All Engines
### i. Install dependencies for all 3 OCR engines. Update system first.
sudo pacman -Syu
sudo pacman -S base-devel poppler cmake git python openblas libglvnd openmp libsm libxrender  openblas--needed

### ii. Install Tesseract + English data
sudo pacman -S tesseract tesseract-data-eng


## 2. create models directory, to store models for easyocr and nanonets engine (tesseract no engine).
mkdir -p models/nanonets
mkdir -p models/easyocr

### i. nanonets: download the brain for nanonets
wget -P models/nanonets https://huggingface.co/mradermacher/Nanonets-OCR2-1.5B-exp-i1-GGUF/resolve/main/Nanonets-OCR2-1.5B-exp.i1-Q4_K_M.gguf

### ii. nanonets: download the eyes for nanonets
wget -P models/nanonets https://huggingface.co/mradermacher/Nanonets-OCR2-1.5B-exp-GGUF/resolve/main/Nanonets-OCR2-1.5B-exp.mmproj-Q8_0.gguf


## 3. Setup python environment
### i. Create venv
python -m venv venv
source venv/bin/activate

### ii. Upgrade pip and install pips
pip install --upgrade pip wheel setuptools scikit-build-core

### iii. Install pytorch cpu version to avoid accidentally grabbing gpu version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

### iv. Install EasyOCR but tell it to respect existing torch/torchvision
pip install easyocr

### iv. Setup EasyOCR models (will download models into /models/easyocr)
python setup_easyocr.py

### v. Install LlamaCpp. We can pip install the binary or build from source for better performance. Choose 1 of the 2 following options:
#### a. pip install binary
pip install llama-cpp-python

#### b. build-from-source
CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" \
pip install llama-cpp-python \
  --no-binary llama-cpp-python \
  --force-reinstall \
  --upgrade \
  -v

### vi. After all above steps, pip install remaining packages from requirements.txt
pip install -r requirements.txt


# To-Do-list
## Create a bash file to run most of above steps automatically