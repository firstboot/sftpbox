# ![](https://note.youdao.com/yws/public/resource/deabc23357bd1170b455d63089114edc/xmlnote/BF7F78B632994C2787A523F20E143990/29938)网箱 SftpBox（SFTP Box）

| [Enlish](https://github.com/firstboot/sftpbox) | [中文版](https://github.com/firstboot/sftpbox/blob/master/README_CN.md) |

### 1. 介绍

有很多网盘软件，例如：[Seafile](https://github.com/haiwen/seafile)，eyebluecn等等，首先他们都很棒，适合复杂场景，部署都需要额外数据库。为什么不直接使用 SFTP 协议呢？SftpBox 就是这样一个简单的工具，直接部署，一台 Linux 本身的文件系统就是存储，不需要其他额外的东西。



#### 1.1 特点

- 通过浏览器管理您的文件
- 分享文件链接
- 操作方便，用户友好
- 可上传下载文件
- 增删改文件



#### 1.2 相关技术点

此程序是一个简单的 WEB SFTP 客户端。它可以简单易用地部署。它是由Python3（后端）和 VUE（前端）开发的。



#### 1.3  UI 预览

![](https://note.youdao.com/yws/public/resource/deabc23357bd1170b455d63089114edc/xmlnote/562762EB724C47A79DA3F109CC97EA98/29942)



![](https://note.youdao.com/yws/public/resource/deabc23357bd1170b455d63089114edc/xmlnote/0E6C9FCA99484C93BEE6E18E66F5BA61/32573)

### 2. 如何开始?



#### 2.1 在 Windows（windows 10 64bit） 上运行

- 下载压缩包

  ```
  https://github.com/firstboot/sftpbox/releases/download/1.0/sftpbox-windows-amd64-v1.0.zip
  ```

  

- 解压并运行

  双击 `sftpbox.exe`

  

- 通过浏览器打开 URL

  ```
  http://127.0.0.1:8000
  ```

  如果需要非本机访问，需要修改 `config.json` 和 `static/static/project.config.json` 配置文件中的 `127.0.0.1` 修改为机器的真实 IP 地址。
  
  

#### 2.2 在 CentOS 7 上通过  Docker运行（推荐方式）

- 安装 Docker

  ```shell
  yum update -y
  yum upgrade
  yum install docker -y
  systemctl enable docker
  systemctl start docker
  ```

  

- 拉去 Docker 镜像并运行

  ```shell
  docker pull linzhanggeorge/firstboot-sftpbox:latest
  
  docker run -d --name fbsftpbox --privileged=true -p 18000:8000 linzhanggeorge/firstboot-sftpbox:latest /bin/sh -c "echo 'hello' && exec /sftpbox/sftpbox/startup.sh '<your host ip>:18000'"
  ```

  

- 通过浏览器打开 URL

  ```
  http://<your host ip>:18000
  ```





#### 2.3 运行在 CentOS7 上

- 安装 Python3 (3.8.3) 或更高版本，CentOS7 YUM 默认安装的 Python3.x 版本（3.6.x）过低，必须安装更高版本（3.8.x+）

  ```
  yum update -y
  yum upgrade
  
  # install depency
  yum groupinstall 'Development Tools' -y
  yum install zlib-devel bzip2-devel  openssl-devel ncurses-devel -y
  yum install libffi-devel wget -y
  yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel wget gcc make -y
  
  # make python3
  cd /home
  wget https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz
  tar -xvf Python-3.8.3.tgz
  cd Python-3.8.3
  mkdir -p /opt/python3
  ./configure --prefix=/opt/python3 --enable-optimizations --with-ssl
  make
  make install
  
  # backup pure python3
  cd /opt
  tar -cvf python3.tar python3
  
  # build link
  ln -s /opt/python3/bin/python3.8 /usr/bin/python3
  ln -s /opt/python3/bin/pip3.8 /usr/bin/pip3
  
  ```

- 获取源码

  ```
  # download code
  git clone https://github.com/firstboot/sftpbox.git
  cd sftpbox/sftpbox
  
  ```

- 修改配置文件

  ```
  # vi config.json
  {
    "origins": [
      "http://localhost:8000",
      "http://127.0.0.1:8000"
    ],
    "tmp_path": "./dtmp/",
    "upload_tmp_path": "./utmp/",
    "share_path": "./share/",
    "port": "8000"
  }
  
  # modify to your host ip
  {
    "origins": [
      "http://localhost:8000",
      "http://<your host ip>:8000"
    ],
    "tmp_path": "./dtmp/",
    "upload_tmp_path": "./utmp/",
    "share_path": "./share/",
    "port": "8000"
  }
  
  # vi static/static/project.config.json
  {
      "debugMode": true,
      "baseUrl": "http://localhost:8000",
      "nav": {
      "initTab": {
              "editableTabsValue": "panelAllFiles",
              "editableTabs": [{"title": "panel.panelAllFiles.label", "name": "panelAllFiles", "content": "test"}]
          },
      "navMenus": [
              {
                  "icon": "fa fa-files-o",
                  "title": "panel.panelAllFiles.label",
                  "name": "panelAllFiles",
                  "type": "menu"
              },
              {
                  "icon": "fa fa-share-alt",
                  "title": "panel.panelShareFiles.label",
                  "name": "panelShareFiles",
                  "type": "menu"
              },
              {
                  "icon": "fa fa-share-square-o",
                  "title": "panel.panelHistory.label",
                  "name": "panelHistory",
                  "type": "menu"
              },
              {
                  "icon": "fa fa-info-circle",
                  "title": "panel.panelSysInfo.label",
                  "name": "panelSysInfo",
                  "type": "menu"
              }
      ]
      }
  }
  
  # modify to your host ip
  {
      "debugMode": true,
      "baseUrl": "http://<your host ip>:8000",
      "nav": {
      "initTab": {
              "editableTabsValue": "panelAllFiles",
              "editableTabs": [{"title": "panel.panelAllFiles.label", "name": "panelAllFiles", "content": "test"}]
          },
      "navMenus": [
              {
                  "icon": "fa fa-files-o",
                  "title": "panel.panelAllFiles.label",
                  "name": "panelAllFiles",
                  "type": "menu"
              },
              {
                  "icon": "fa fa-share-alt",
                  "title": "panel.panelShareFiles.label",
                  "name": "panelShareFiles",
                  "type": "menu"
              },
              {
                  "icon": "fa fa-share-square-o",
                  "title": "panel.panelHistory.label",
                  "name": "panelHistory",
                  "type": "menu"
              },
              {
                  "icon": "fa fa-info-circle",
                  "title": "panel.panelSysInfo.label",
                  "name": "panelSysInfo",
                  "type": "menu"
              }
      ]
      }
  }
  
  ```

- 安装 Python 相关库并运行

  ```
  # install lib
  pip3 install -r requirements.txt
  
  # run
  python3 main.py
  ```

- 通过浏览器打开 URL

  ```
  http://<your host ip>:8000
  ```



#### 2.4 在 树莓派 *Raspberry Pi* 上运行

...



