# Pytex-for-MCM
基于[Pytex](https://github.com/zrr1999/PyTex)的数学建模工具,实现将md文件转换成pdf/tex文档的前后端。
# 依赖
mistune应使用2.0.0a3版本。
```
$ pip install mistune==2.0.0a3
```
# 开始
1.git clone 或者 下载zip ,然后解压到运行目录。

3.在`webflask.py`中找到`app.config['APP_FOLDER']`,将其路径修改成运行目录。

5.运行`webflask.py`。

# 框架
前端:[fcup](https://github.com/lovefc/fcup)

后端:[flask](https://github.com/pallets/flask)
