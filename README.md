# 深度学习图像修复平台
 >&emsp;&emsp;忙了很久，毕业论文终于水完了:tada:！这是一个基于二阶段式GAN的图像修复网站，主要功能都比较简单，可以通过涂抹的方式对需要修复的图像进行修复。   
 >&emsp;&emsp;整体框架上采用Django，模型使用了[EdgeConnect](https://github.com/knazeri/edge-connect)，原本想再参考其他模型再对其改进，但由于时间比较短促，就选择了这个开源比较完整的模型直接拿来用了（时至今日看该模型多少有点旧了，但该论文还是有研究价值的（关于信息先验），想看其他更新的模型（截止2022年4月）请移步下方“文献分享”），代码没有弄得很完美，但最后感觉效果还不错，上传分享一下。  
 >&emsp;&emsp;假如源码对你有帮助，欢迎Star！🎁
 >&emsp;&emsp;(仅供参考，请勿作商业用途)
 >
 > ![image](https://user-images.githubusercontent.com/46208115/167092889-9f8d6420-5e0e-409f-a597-95aae2f21d3c.png)
---
## 文献分享  
 >&emsp;&emsp;在准备毕业论文过程中，本人整理了近年来关于inpainting的pdf文献（收集了16-22年计算机视觉三大顶会（CVPR、ICCV、ECCV）和（WACV、ACCV）等顶会大概50篇左右关于inpainting的论文，收寻的数量上重点在近三四年，早年主要寻求代表作），并且整理了表格（表格中整理了相关文献的摘要、介绍、结论等内容，中英对照），如果需要该资料，[请点击这里(Google云端)](https://drive.google.com/file/d/1nFDeJMDdcGJxqwqJ0MdTGMFpPS2uCUYZ/view?usp=sharing) 。([百度网盘](https://pan.baidu.com/s/1v__UUyWBSrjKyx3m9vg_Kw))提取码：`vjuj`
 >
 >![image](https://user-images.githubusercontent.com/46208115/167785715-fb623839-e08b-463a-a215-b59b77fc2f89.png)
 >![image](https://user-images.githubusercontent.com/46208115/167785823-091bc9b4-9ec8-4640-8a58-b24268edd9eb.png)
---
## 模型介绍
 >![image](https://user-images.githubusercontent.com/46208115/167091435-d5771bdd-052a-4a34-b61d-3b85738ee1a3.png)
## 数据集
> 该模型文件使用[Places2](http://places2.csail.mit.edu/)、[CelebA](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)和[Paris Street-View](https://github.com/pathak22/context-encoder)数据集训练而成。要在完整数据集上训练模型，请从官方网站下载数据集。
>>  注意：其中因模型权重文件大小限制，需要自行[命令行下载](https://github.com/knazeri/edge-connect)
## 平台展示
 >![image](https://user-images.githubusercontent.com/46208115/167090145-4fb215e9-577b-4b6f-aa94-20603faf44f7.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090202-5c938ec8-c2fd-4b9f-bca2-5c6428c6491f.png)
---
## 效果展示
 >![image](https://user-images.githubusercontent.com/46208115/167090267-c8ce0ebf-cadf-475b-85b3-944cc6c252a2.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090366-4355347f-4984-44bc-a55b-8d03ca11b29d.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090395-a9f32a13-af71-4ca0-ad2d-ee86b81a3262.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090428-83eafca1-f84c-40a6-8e2d-d4a5da4fa38e.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090460-6b2f8523-0775-4c4a-ae17-5b71e887a9ef.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090540-8da410db-44b0-4525-bf19-2ed86de02eda.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090561-59be0d35-66f9-4d4e-a8f3-861e176498b1.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090598-e076ed96-55e7-40ec-b8cd-13ab11a8c1da.png)
 >![image](https://user-images.githubusercontent.com/46208115/167090729-eb6fad14-23c3-4762-90ca-8f07ea4cbbf1.png)
---
## Ending
>  如果该源码对你有帮助，欢迎[Star](https://github.com/pete-li/inpainting_edgeconnect/#)！:gift:
