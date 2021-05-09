# ![](https://note.youdao.com/yws/public/resource/deabc23357bd1170b455d63089114edc/xmlnote/BF7F78B632994C2787A523F20E143990/29938)SftpBox（SFTP Box）

| [Enlish](https://github.com/firstboot/sftpbox) | [中文版](https://github.com/firstboot/sftpbox/blob/master/README_CN.md) |

###  1. Introduction

A NetDisk(Dropbox, Baidu-NetDisk)-like file manager that let you manage your data anywhere it is located: SFTP. There are a lot of tools, such as [Seafile](https://github.com/haiwen/seafile), eyebluecn, and so on, first of all they are great, suitable for complex scenarios, deployment needs additional databases. Why not just use the SFTP protocol? `SftpBox` is such a simple tool, deployed directly, a Linux file system itself is storage, no need for anything else.



#### 1.1 Features

- Manage your files from a browser
- Shared links
- User friendly
- Upload and download files
- List, move, rename and remove files



#### 1.2 Technical points

This program is a simple WEB SFTP client. It can be deployed simply and easily. It was developed by python3 (backend) and VUE（frontend）.



#### 1.3  UI Preview

![](https://note.youdao.com/yws/public/resource/deabc23357bd1170b455d63089114edc/xmlnote/562762EB724C47A79DA3F109CC97EA98/29942)



![](https://note.youdao.com/yws/public/resource/deabc23357bd1170b455d63089114edc/xmlnote/0E6C9FCA99484C93BEE6E18E66F5BA61/32573)



### 2. How to start?



#### 2.1 Run by windows（windows 10 64 bit）

- Download zip package

  ```
  https://github.com/firstboot/sftpbox/releases/download/1.0/sftpbox-windows-amd64-v1.0.zip
  ```

  

- Unzip and run

  double click `sftpbox.exe`

  

- Open URL by browser

  ```
  http://127.0.0.1:8000
  ```

  If non-localhost access is required, the `127.0.0.1` in the `config.json` and `static/static/project.project.config.json'`profiles needs to be modified to the server's real IP address.
  
  


#### 2.2 Run by Docker(in CentOS 7) -- recommend

- Install Docker

    ```shell
    yum update -y
    yum upgrade
    yum install docker -y
    systemctl enable docker
    systemctl start docker
    ```

    

- Pull docker image，and run

    ```shell
    docker pull linzhanggeorge/firstboot-sftpbox:latest
    
    docker run -d --name fbsftpbox --privileged=true -p 18000:8000 linzhanggeorge/firstboot-sftpbox:latest /bin/sh -c "echo 'hello' && exec /sftpbox/sftpbox/startup.sh '<your host ip>:18000'"
    ```

    

- Open URL by browser

    ```
    http://<your host ip>:18000
    ```






#### 2.3 Run by Linux(CentOS 7)

- Install Python3
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

- Get source code 

    ```
    # download code
    git clone https://github.com/firstboot/sftpbox.git
    cd sftpbox/sftpbox

    ```

- Modify config file

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

- Install python lib and running

    ```
    # install lib
    pip3 install -r requirements.txt

    # run
    python3 main.py
    ```

- Open URL by browser

    ```
    http://<your host ip>:8000
    ```



#### 2.4 Run by *Raspberry Pi*

...




