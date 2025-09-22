# 推荐组合（适配 BEVDet）
# 根据 BEVDet 的官方环境（commit 大约在 2022~2023），常见可行的版本组合是：
# cuda = 11.3
# torch == 1.11.0
# mmcv-full == 1.6.1
# mmdet == 2.25.0
# mmdet3d == 1.0.0rc6

# 基础镜像
FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PATH=/opt/conda/bin:$PATH

# 安装基础依赖和 Python
RUN apt-get update && apt-get install -y \
    wget git curl vim build-essential python3-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 更新 pip
RUN pip3 install --upgrade pip

# 安装 PyTorch 
# RUN pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
# torch 2.6 ---> mmcv >= 2.2 : conflicts with mmdet3d < 2.2
RUN pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113

# 安装 mmcv 2.1 对应 CUDA 121
# RUN pip uninstall -y mmcv mmcv-full
# RUN pip index versions mmcv-full
# RUN pip install mmcv==1.6.1 -f https://download.openmmlab.com/mmcv/dist/cu113/torch1.11/index.html
# 设置工作目录
WORKDIR /workspace
# 克隆或COPY MMCV源码
RUN git clone -b v1.6.1 https://github.com/open-mmlab/mmcv.git
WORKDIR /workspace/mmcv
# 编译安装MMCV，启用C++/CUDA扩展
ENV MMCV_WITH_OPS=1
RUN pip install -e .

# 设置工作目录
WORKDIR /workspace

RUN pip install pycuda \
    lyft_dataset_sdk \
    numba \
    numpy \
    nuscenes-devkit \
    plyfile \
    scikit-image \
    tensorboard -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install \
    networkx \
    trimesh==2.35.39 -i https://pypi.tuna.tsinghua.edu.cn/simple


RUN pip install onnxruntime-gpu

RUN pip install openmim
RUN pip install mmdet==2.25.1 mmsegmentation==0.30.0
# -i https://pypi.tuna.tsinghua.edu.cn/simple && \
#    cd ..

RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"

# 复制 BEVDet 项目代码到容器（也可以在运行容器时挂载主机目录）
# COPY ./BEVDet /workspace/BEVDet
# WORKDIR /workspace/BEVDet

# 安装 BEVDet 依赖
# 如果 BEVDet 有 requirements.txt
# RUN pip install -r BEVDet/requirements.txt

# 安装 BEVDet 开发模式（可选）
# RUN pip install -e BEVDet

# 设置 LD_LIBRARY_PATH（确保 PyTorch 动态库可用）
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/python3.8/site-packages/torch/lib

# 默认进入 bash
CMD ["/bin/bash"]

