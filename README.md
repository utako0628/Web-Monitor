# 基于python的智能监控平台

刘家维-2016013246-软61                                                        

山本宇多子-2016080045-软62



## 目的
以python开发一个网站服务，对有权限的用户提供服务器端摄像头的监控画面，使用人工智能技术对监控画面做处理，将分析结果显示到网页上。



## 环境

* Language: `python 3`

* OS: Server 可运行于`Windows`, `Linux`(要确保操作系统能打开本机的0号摄像头即可)

* Database: `sqlite3`


## 框架与依赖项

* 网页: `Django`
* 深度学习: `python-opencv`
* 摄像头: `imutils`(基于opencv)

详情、安装`venv`请依照`./requirements`



## 使用说明

#### /web/

创建管理员和普通用户。

- 在所在文件终端首先输入 `python manage.py makemigrations`，`python manage.py migrate`这两句命令。然后输入命令`python manage.py createsuperuser`开始创建管理员。
- 在浏览器中输入`127.0.0.1:8000/admin/`，输入管理员账号进入后台管理创建普通用户。

进入主页面`url`：`127.0.0.1:8000/web/`

- 点击登陆，进入登陆页面，可输入用户名和密码，输入正确即可进入`/monitor/`页面。
- 登入成功后记录`cookie`记录用户名，重复访问会自动跳转到`monitor`，不必重新登入。10分钟内有效。
- 点击修改密码，进入修改密码界面，输入正确后，点击确定按钮返回到主页面。
- 若未登入而直接访问`/monitor/`，会因为无`cookie`而被跳转回`/web/`


#### /monitor/

进入页面后，所见如图。

* 最上方显示用户名
* 点击Logout可登出，同时清除`cookie`
* 点击Turn on camera，则令服务器开启摄像头，同时向前端推送串流画面，前端页面显示画面。画面中已含监控信息。
* 画面中会自动将一些生活见常见的物体识别后框出，并写出自信程度。种类有人、椅子、车子、火车、沙发、等等。详细识别列表可参见`videoCamera.py`中成员变量`CLASSES`。
* 点击Turn off camera，则令服务器关闭摄像头、停止串流、前端页面关闭画面


​		



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

    * 物体识别:

       * 使用的预训练模型提供检测生活中经典常见的类别，如人、椅子、车子、火车、沙发、等等。详细识别列表可参见`videoCamera.py`中成员变量`CLASSES`。

       * 识别的自信度高于设定值后(默认20%，可在`VideoCamera`构造函数中传参指定)，会框选标识出来。

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

  - `forms.py`

    创建`user_form`类，是对于用户登陆有用户名和密码输入，对用户提交数据进行处理。创建`change_form`类，是对于用户修改密码时提交用户名、原密码和新密码时进行数据处理。

  - `models.py`

    后台处理存储用户信息，创建数据库模型，建立一个`User`表，存储用户的名字、密码和邮箱。在用户信息中，输入的字符有最大限制`max_length`，用户名及邮箱不能出现重复。

  - `/templates/`

    - `index.html`

      `url`：`127.0.0.1:8000/web/`

      主页面，页面中有标题和两个链接，点击每个链接就会进入相应`url`的页面。

    - `login_page.html`

      `url`：`/web/login_page/`

      登陆页面，用户在此页面输入用户名和密码，点击登陆按钮，使用`POST`方式将输入的数据发送到服务器，服务器通将接收处理请求。

    - `change_password_page.html`

      `url`：`/web/change_password_page/`

      修改密码界面，用户输入用户名、原密码和新密码，点击确定按钮，使用`POST`方式将输入的数据发送到服务器，服务器接收处理请求。

  - `views.py`

    - `login()`

      用户在前端页面输入的数据`POST`方式发送到服务器，服务器通过此函数接收处理发来的请求，`is_valid()`验证数据，验证后会从`cleaned_data`得到form中的值。数据会和数据库中相匹配，在输入的数据有错误时会有提示`message`。登陆验证成功则给予`cookie`，跳转到`/monitor/`。

    - `change_password()`

      服务器通过此函数接受处理前端页面发来的请求，和`login()`同理，输入的原密码正确之后才会`update`为新密码，然后跳转到`/web/`。

    - `logout()`

      `cookie`校验用户权限，删除`cookie`，登出之后跳转到`/web/`。





## 参考、引用

* ###### OpenCv深度学习与物体识别: 

  Rosebrock, A. (2018, February 25). Face detection with OpenCV and deep learning. Retrieved from https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/

* ###### MobileNet-SSD model configs from https://github.com/chuanqi305/MobileNet-SSD with MIT license.

* ###### `imutils` module from https://github.com/jrosebr1/imutils with MIT license.




