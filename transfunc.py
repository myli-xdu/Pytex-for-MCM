from pytex import MathDocument
from pytex.utils import md2tex
import uuid
import os
import shutil
import zipfile


def un_zip(file_name, dir_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    os.mkdir(dir_name)
    for names in zip_file.namelist():
        zip_file.extract(names, dir_name)
    zip_file.close()


def fun_trans(filename, path):
    '''解压上传文件'''
    dir_path = os.path.join(path, uuid.uuid4().hex)  # 随机生成文件名
    un_zip(filename, dir_path)
    '''移动cumcmthesis.cls'''
    argetfile_path = os.path.join(path, "cumcmthesis.cls")
    Targetfile_path = os.path.join(dir_path, "cumcmthesis.cls")
    shutil.copyfile(argetfile_path, Targetfile_path)
    '''生成latex/pdf'''
    doc = MathDocument('数学建模',
                       packages=["amsmath", "graphicx", "amssymb", "cite", "hyperref", "pythonhighlight"],
                       standard="GJS", preface=False)
    doc.set_information()
    doc.add_title()
    doc.add_abstract(md2tex(os.path.join(dir_path, "abstract.md")))
    doc.add_toc()  # 目录
    doc.add_section(title="符号说明", content=doc.var_table)  # 添加变量表
    doc.add_section(path=os.path.join(dir_path, "body.md"))  # 模型的改进与推广
    try:
        doc.generate_pdf(os.path.join(dir_path, "result"), compiler='XeLatex', clean_tex=False, clean=False)
    except:
        pass  # 有时生成成果也会提示失败，所以忽略报错，以是否生成pdf/tex为准
    url_pdf = os.path.join(dir_path, "result.pdf")
    url_tex = os.path.join(dir_path, "result.tex")
    if (not os.path.exists(url_pdf)) or (not os.path.exists(url_tex)):
        raise Exception('生成失败！')
    url_pdf = os.path.join("results", os.path.relpath(url_pdf, path))  # 获取以网页根目录开头的相对路径
    url_tex = os.path.join("results", os.path.relpath(url_tex, path))  # 获取以网页根目录开头的相对路径
    return url_pdf, url_tex
