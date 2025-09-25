# 推荐组合（适配 BEVDet）
# 根据 BEVDet 的官方环境（commit 大约在 2022~2023），常见可行的版本组合是：
# cuda = 11.3
# torch == 1.11.0
# mmcv-full == 1.6.1
# mmdet == 2.25.0
# mmdet3d == BEVDet自带

# 基础镜像
FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
# ENV TORCH_CUDA_ARCH_LIST="5.2 6.0 6.1 7.0 7.5 8.0+PTX"

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
# torch 2.6 ---> mmcv >= 2.2 : conflicts with mmdet3d < 2.2
RUN pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113

RUN pip install pycuda \
    lyft_dataset_sdk \
    numpy==1.23.5 \
    nuscenes-devkit \
    plyfile \
    scikit-image \
    tensorboard -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install \
    networkx==2.2 \
    numba==0.53.0 \
    trimesh==2.35.39 -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install onnxruntime-gpu
# RUN pip install openmim
RUN pip install mmdet==2.25.1 mmsegmentation==0.30.0
# -i https://pypi.tuna.tsinghua.edu.cn/simple && \
#    cd ..
RUN pip install spconv-cu113

RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"

# 安装 mmcv
# RUN pip uninstall -y mmcv mmcv-full
# RUN pip install mmcv==1.6.1 -f https://download.openmmlab.com/mmcv/dist/cu113/torch1.11/index.html # it has mmcv-ext missing issue 
# 克隆MMCV源码
WORKDIR /opt/workspace/install
RUN git clone -b v1.6.1 https://github.com/open-mmlab/mmcv.git
WORKDIR /opt/workspace/install/mmcv
# 编译安装MMCV，启用C++/CUDA扩展
ENV MMCV_WITH_OPS=1
ENV CUDA_HOME=/usr/local/cuda

ENV pip3 install matplot jupyter ipykernel

# 设置 LD_LIBRARY_PATH（确保 PyTorch 动态库可用）
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/python3.8/site-packages/torch/lib

# 默认进入 bash
CMD ["/bin/bash"]


# 需要--gpu_all挂载docker后的准备工作:
# docker ps   # 找到容器 ID
# docker commit <container_id> bevdet:latest
# 1)
# RUN MMCV_WITH_OPS=1 pip install -e . -v
# 因为在docker build阶段，默认docker无法加载cuda runtime，编译出来的mmcv没有cuda ext。
# 当前解决方法是在run --gpus_all后再编译，然后docker commit
# 2)
# 修复 mmcv config.py 中 FormatCode 的 verify 参数, 把 MMCV 的 verify=True 自动去掉，避免训练报错
# RUN sed -i "s/verify=True//g" $(python3 -c "import mmcv; import os; print(os.path.join(os.path.dirname(mmcv.__file__), 'utils/config.py'))")