# 基于python的智能监控平台

刘家维-2016013246-软61                                                        

山本宇多子-2016080045-软62

## 目的
以python开发一个网站服务，对有权限的用户提供服务器端摄像头的监控画面，使用人工智能技术对监控画面做处理，将分析结果显示到网页上。

## 环境

* Language: `python 3`
* OS: Server 可运行于`Windows`, `Linux`(要确保操作系统能打开本机的0号摄像头即可。
* Database: `sqlite3`

## 框架与依赖项

* 网页: `Django`
* 深度学习: `python-opencv`, `imutils`

详情、安装`venv`请依照`./requirements`

## 使用说明

#### /web/

#### /monitor/

进入页面后，所见如图。

* 最上方显示用户名

* 点击Logout可登出
* 点击Turn on camera，则令服务器开启摄像头，同时向前端推送串流画面，前端页面显示画面。画面中已含监控信息
* 点击Turn off camera，则令服务器关闭摄像头、停止串流、前端页面关闭画面



## 项目架构与实现方法

```shell
.  # 此处未列出部份自动生成文件
├── db.sqlite3
├── manage.py
├── monitor # monitor app
├── Project # Django settings, etc
├── README.md
└── web # web(user) app
```

#### app monitor

* 结构

```shell
./monitor/  # 此处未列出部份自动生成文件
├── MobileNetSSD  # Deep learning module
│   ├── deploy.prototxt  # config file
│   ├── MobileNetSSD_deploy.caffemodel  # config file
│   └── videoCamera.py  # Deep learning module
├── templates
│   └── monitor
│       └── index.html
├── urls.py
└── views.py
```

* 说明

  * `videoCamera.py`

    * `VideoCamera`

      创建`VideoCamera`实例对象时，即开启本机0号摄像头。每次执行`get_frame()`时，读取摄像头当前画面，进行物体识别(基于已经训练好的模型，由构造函数传入的文件名指定所使用的`prototxt`与`caffemodel`)，并回传以jpeg编码后的信息。

    * `gen()`

      给入`VideoCamera`对象，产生mjpeg流

  * `views.py`

    由于希望服务器的摄像头是可控制开或关，而永远处于开启状态，所以多写了几个函数来控制串流行为，与前端页面的Turn on/off camera相配合。

    * `start()`

      `url`: `/monitor/start/`

      创建`VideoCamera`实例`vc`，为全局变量，方便其他函数共同操作

    * `stop()`

      `url`: `/monitor/stop/`

      销毁`vc`

    * `stream()`

      `url`: `/monitor/stream/`

      调用`gen(vc)`，提供串流源，返回的是`StreamHttpResponse`，前端页面中`<img>`的`src`设为`/monitor/stream/`即可显示串流画面。由此`url`获取串流源时必须要先用`start()`创建`vc`实例

  * `/templates/index.html`

    `/monitor/`返回的页面，内含简单的`js`脚本，透过`ajax`实现背后发送请求而不刷新页面的效果。点击Turn on/off camera时，向服务器发送`/monitor/start/, /monitor/stop/`请求，同时设置前端`<img>`的`src`为`/monitor/stream/`，于是前端开始显示监控画面。



#### app web

* 结构

  ```shell
  ./web/   # 此处未列出部份自动生成文件
  ├── forms.py   # form class
  ├── models.py   # Self-defined User class
  ├── templates
  │   └── web
  │       ├── change_password_page.html
  │       ├── index.html
  │       └── login_page.html
  ├── urls.py
  └── views.py
  ```

* 说明

