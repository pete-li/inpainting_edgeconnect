import os
from torch.utils.data import DataLoader
from .dataset import Dataset
from .models import EdgeModel, InpaintingModel
from .utils import  create_dir, imsave
from .metrics import PSNR, EdgeAccuracy


class EdgeConnect():
    def __init__(self, config):
        self.config = config
        model_name = 'joint'
        self.model_name = model_name
        self.edge_model = EdgeModel(config).to(config.DEVICE)
        self.inpaint_model = InpaintingModel(config).to(config.DEVICE)

        self.psnr = PSNR(255.0).to(config.DEVICE)
        self.edgeacc = EdgeAccuracy(config.EDGE_THRESHOLD).to(config.DEVICE)

        # test mode
        self.test_dataset = Dataset(config, config.TEST_FLIST, config.TEST_EDGE_FLIST, config.TEST_MASK_FLIST, augment=False, training=False)

        self.samples_path = os.path.join(config.PATH, 'samples')
        self.results_path = os.path.join(config.PATH, 'results')

        self.results_path = os.path.join(config.RESULTS)
        self.results_name = os.path.join(config.RESULT_NAME)
        self.masked_name = os.path.join(config.MASKED_NAME)
        self.edge_name = os.path.join(config.EDGE_NAME)

            
        self.log_file = os.path.join(config.PATH, 'log_' + model_name + '.dat')

    def load(self):
        self.edge_model.load()
        self.inpaint_model.load()

    def save(self):
        self.edge_model.save()
        self.inpaint_model.save()
            

    def inpainting(self):
        self.edge_model.eval()  # 评估模式 batchNorm层，dropout层等用于优化训练而添加的网络层会被关闭，从而使得评估时不会发生偏移。
        self.inpaint_model.eval()

        create_dir(self.results_path)

        test_loader = DataLoader(
            dataset=self.test_dataset,
            batch_size=1,
        )

        index = 0
        for items in test_loader:
            # name = self.test_dataset.load_name(index)
            images, images_gray, edges, masks = self.cuda(*items)
            index += 1

            #join mode
            edges = self.edge_model(images_gray, edges, masks).detach()
            outputs = self.inpaint_model(images, edges, masks)
            outputs_merged = (outputs * masks) + (images * (1 - masks))
                

            output = self.postprocess(outputs_merged)[0]
            # fname, fext = self.results_path.split('.')
            imsave(output, os.path.join(self.results_path, self.results_name))

            edges = self.postprocess(1 - edges)[0]
            masked = self.postprocess(images * (1 - masks) + masks)[0]
            imsave(edges, os.path.join(self.results_path, self.edge_name))
            imsave(masked, os.path.join(self.results_path, self.masked_name))

        print('\nEnd inpainting....')


    def log(self, logs):
        with open(self.log_file, 'a') as f:
            f.write('%s\n' % ' '.join([str(item[1]) for item in logs]))

    def cuda(self, *args):
        return (item.to(self.config.DEVICE) for item in args)

    def postprocess(self, img):
        # [0, 1] => [0, 255]
        img = img * 255.0
        img = img.permute(0, 2, 3, 1)
        return img.int()
