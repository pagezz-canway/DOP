## 本地环境前端部署指南

### 1 安装node.js

DOP前端是用 vue 框架开发的，在本地开发时需要先安装 node.js，直接去官网下载软件并安装即可，地址为：https://nodejs.org/en/ 。

### 2 安装依赖包

进入项目中frontend/bkx/，执行以下命令安装。

```
npm install
```

### 3 填写后端地址

- 1: 进入项目中frontend/bkx，修改index-dev.html 文件
 `window.AJAX_URL_PREFIX = 'appdev.{BK_PAAS_HOST}：8000'`

- 2: 进入项目中frontend/bkx/build，修改dev.env.js 文件
 `LOCAL_DEV_URL: JSON.stringify('appdev.{BK_PAAS_HOST}')`

### 4 启动前端工程
进入项目中frontend/bkx/ 执行以下命令运行前端工程。默认启动的是 5000 端口，然后通过 http://appdev.{BK_PAAS_HOST}:5000  访问前端应用，此时后端请求会自动转发到你启动的 django 工程，即 8000 端口。
```
npm run dev
```