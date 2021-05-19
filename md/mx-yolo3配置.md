## 前言

首先感谢 Kelvin_927 老师提供的[MX-Yolo3](https://mc.dfrobot.com.cn/thread-308750-1-1.html);

其次感谢 xiaocaishu 提供的[MX_yolov3 部署在 k210 的环境搭建](https://cn.bbs.sipeed.com/d/516-mx-yolov3k210);

~~第三感谢自己抽出打游戏的时间来写这个帖子;~~

本贴主要帮助第一次接触`MX-Yolo`并且没有配置过 python 的萌新，旨在快速帮助大家入门。

完全图文教程，~~~因此会有大量图片，请注意自己的流量。~~放心食用。

## 软件下载

1. 下载[Anacoda](https://www.anaconda.com/products/individual)；
2. 下载[MX-Yolo3](https://mc.dfrobot.com.cn/thread-308750-1-1.html)，这里提供[个人分流网盘](https://cloud.189.cn/t/mYfYJnA73Uvi )。(访问码:m8ip)

## 软件配置

1. 打开下载的Anacoda，安装，next，如下图时选择ALL Users。继续安装，直到安装完毕。注意记住安装路径，后续会用到。

   [align=center][attachimg]122644[/attachimg][/align]

2. 运行Anacoda。点击Environment,点击Create，Name填入Mx_yolov3,python版本勾选3.7，点击Create创建。

![img](https://mc.dfrobot.com.cn/forum.php?mod=image&aid=122645&size=300x300&key=bf1bd1122ba51ae6&nocache=yes&type=fixnone)

3. 下载Tensorflow-GPU。在Environment中点击MX_yolov3，serch搜索Tensorfow-gpu，右键Tensorfow-gpu，点击Mark for specific version installation，勾选1.15.0，右下角apply。

   ![img](https://mc.dfrobot.com.cn/forum.php?mod=image&aid=122646&size=300x300&key=01453eb2afc1b630&nocache=yes&type=fixnone)

   

4. 安装MX_yolov3。下一步下一步下一步。注意安装路径。安装完毕后，打开安装路径，打开`1.环境配置`文件夹,打开data，找到pip.txt,记事本打开，删除Tensorflow的两行。结果如下：

   ```python
   imgaug==0.2.6
   opencv-python==4.0.0.21
   Pillow==6.2.0
   requests==2.24.0
   tqdm==4.48.2
   sklearn==0.0
   pytest-cov==2.10.0
   codecov==2.1.8
   matplotlib==3.0.3
   pascal_voc_writer==0.1.4
   PyQt5==5.15.0
   numpy==1.16.2
   keras==2.3.1
   scikit-learn==0.22.2
   seaborn==0.11.0
   alive-progress==1.6.1
   h5py==2.10.0
   pyecharts==1.9.0
   matplotlib==3.0.3
   ```

   保存到桌面。

5. 启动MX_yolov3虚拟环境。打开conda powershell，输入` conda activate Mx_yolov3`激活虚拟环境。每次启动MX_yolov3前，都要激活一次。

   ![img](https://mc.dfrobot.com.cn/forum.php?mod=image&aid=122647&size=300x300&key=250a0721abb91c48&nocache=yes&type=fixnone)

   输入`cd .\Desktop\`，回车，输入`pip install -r pip.txt -i https://pypi.douban.com/simple`,回车。

6. 验证结果。打开系统自带cmd，输入`pip list`,出现下图即为成功。

   ![img](https://mc.dfrobot.com.cn/forum.php?mod=image&aid=122648&size=300x300&key=7e1cb8c17f09c323&nocache=yes&type=fixnone)

7. 配置系统环境变量。打开系统属性，环境变量，找到系统变量中的path，右键编辑，将如下两行代码加入环境变量中。注意替换Anaconda安装路径，上文已经让你记下来了，记不住慢慢找。

   ```
   D:\ProgramData\Anaconda3\envs\Mx_yolov3\Scripts
   D:\ProgramData\Anaconda3\envs\Mx_yolov3
   ```

8. 安装cuda。打开4中的data文件夹，打开`CUDA+Cudnn`，安装CUDA。同样记住安装路径。安装完毕后，解压cudnn，将cuda中文件复制到CUDA中。CUDA文件夹在`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0`中，注意``C:\Program Files`指的是前面的安装路径。

   ![img](https://mc.dfrobot.com.cn/forum.php?mod=image&aid=122649&size=300x300&key=9e4189a7d9220ccc&nocache=yes&type=fixnone)

9. 修改预训练权重。打开data文件夹，复制`mobilenet.py`到`Anaconda3\envs\Mx_yolov3`中的`Lib\site-packages\keras\applications`中。
10. 放置模型。复制data的`.keras`文件夹，粘贴到`C:\Users\Lithromantic`,注意替换`Lithromantic`为你的用户名。

## 运行软件

打开MX-yolov3，尝试训练自带的模型。如果出现任何问题，请在下方回复以寻求帮助。