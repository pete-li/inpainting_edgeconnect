import os
import torch
import cv2
from PIL import Image
# import random
# import numpy as np
from .src.config import Config
from .src.edge_connect import EdgeConnect


def inpaintingImg(upload_name,img_type,mask_path,masked_name,edge_name,result_name):
    print('图片类型：',img_type)
    if img_type == 1:
        checkpoints = './Inpainting/edgeConnect/checkpoints/celeba'
    else:
        checkpoints = './Inpainting/edgeConnect/checkpoints/places2'
        
    input_path = './static/media/userStorage/' + upload_name
    output_path = './static/media/userStorage/'

    
    L_image=Image.open(input_path)
    out = L_image.convert("RGB")
    out.save(input_path)

    config_path = os.path.join(checkpoints, 'config.yml')

    # load config file
    config = Config(config_path)

    config.INPUT_SIZE = 256

    config.TEST_FLIST = input_path
    config.TEST_MASK_FLIST = mask_path
    config.RESULTS = output_path
    config.RESULT_NAME = result_name
    config.MASKED_NAME = masked_name
    config.EDGE_NAME = edge_name


    # cuda visble devices
    os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(str(e) for e in config.GPU)

    # init device
    if torch.cuda.is_available():
        config.DEVICE = torch.device("cuda")
        torch.backends.cudnn.benchmark = True   # cudnn auto-tuner
    else:
        config.DEVICE = torch.device("cpu")
    # set cv2 running threads to 1 (prevents deadlocks with pytorch dataloader)
    cv2.setNumThreads(0)

    model = EdgeConnect(config)

    model.load()
    model.inpainting()

# if __name__ == "__main__":
#     inpaintingImg()
