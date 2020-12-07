#视觉程序
## 说明
`里面存放视觉程序当前使用的一些主要功能，后续修改时会同步更新`
## 使用
安装requirements.txt里所有包终端运行  
`python main.py -vL videoLPath -vR videoRPath -COM ComPortPath`  

## 项目结构
* main.py 主函数  
* calibration 相机标定及其参数  
* communication 串口通信  
* detection 颜色与形状检测  
* order   指令创建与坐标变换  
* stitch  图像拼接  
* resource  资源目录


## 注意事项
1. 每个功能都可单独调试，可试运行看下效果  
3. 目前接受图像分辨率较低，基于特征拼接效果不是很好，可能更换方案

            
