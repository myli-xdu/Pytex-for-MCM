from flask import Flask, render_template, request, flash, redirect, send_from_directory, json
from transfunc import fun_trans
import os

app = Flask(__name__)
app.config['APP_FOLDER'] = 'D:\\准备面试\\pytex相关\\前后端'  # 项目所在地址
app.config['UPLOAD_FOLDER'] = os.path.join(app.config['APP_FOLDER'], 'upload/')
app.config['RESULTS_FOLDER'] = os.path.join(app.config['APP_FOLDER'], 'results/')
app.config['EXAMPLE_FOLDER'] = os.path.join(app.config['APP_FOLDER'], 'example/')
app.secret_key = '12345678'


# 设置首页重定向
@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index.html')


# 上传请求地址
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file_md5 = request.form['file_md5']
        if 'file_data' not in request.files:
            flash('No file part')
            return redirect('/')
        f = request.files['file_data']
        name = file_md5 + ".zip"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        f.save(file_path)
        try:
            url_pdf, url_tex = fun_trans(file_path, app.config['RESULTS_FOLDER'])
        except Exception as ex:
            res = {"status": 0, "message": "生成失败,原因:" + str(ex), "url_pdf": "", "url_tex": ""}
        else:
            res = {"status": 2, "message": "生成成功", "url_pdf": url_pdf, "url_tex": url_tex}
        return json.dumps(res)


@app.route('/results/<path:sub_dir>/<filename>')
def download_file(sub_dir, filename):
    dir_name = os.path.join(app.config['RESULTS_FOLDER'], sub_dir)
    return send_from_directory(dir_name, filename)


@app.route('/example/<filename>')
def download_example(filename):
    return send_from_directory(app.config['EXAMPLE_FOLDER'], filename)


if __name__ == '__main__':
    app.run()
