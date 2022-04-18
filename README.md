# conv-shape-tool  
计算卷积网络输出尺寸的小工具。  
A tool help cumputing the shape of convolution layers.   

<p><img src="/python.png"" /></p>  
  
## 功能(Function): 
  填写输入尺寸，配置网络，计算输出尺寸。  
  目前仅支持卷积层。  
  Set input shape and neural network, compute output shape.  
  At present, only convolution layer is supported.  
  
## 系统要求(System required)：
  Python  
  
## 安装(Install)：
  点击上方“code”下载,运行“main.py”启动程序。  
  press *code* to download, run *main.py* to start up
  
## 使用说明(How to use)：
  1. 点击“+”添加网络层，下拉框选择网络类型；
  2. 填写输入尺寸及网络参数；
  3. 点击“Input”计算输出尺寸。
  1. press **+** to add a layer, use combobox to select the type of layers.
  2. set parameter of input shape and layers.
  3. press *Input* to compute the ouput shape.
  
## 更新计划：  
- 添加全连接层
- 部分参数自动配置
- 无环结构支持，类似U-Net Res-Net
