import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader

#计算获得文件的md5值
def get_file_md5(file_path:str):

    #判断文件是否存在
    if not os.path.exists(file_path):
        logger.error(f'[计算md5]File{file_path} not exist')
        return

    #判断文件是否属于文件
    if not os.path.isfile(file_path):
        logger.error(f'[计算md5]File{file_path} is not file')

    md5_obj = hashlib.md5()

    # 不能直接读取保存文件的所有内容，文件可能过大
    #4kb分片，避免文件过大爆内存
    chunk_size = 4096

    try:
        with open(file_path, 'rb') as f:    #想要计算文件内容的md5值，必须二进制读取
            while True:
                 chunk = f.read(chunk_size)
                 if not chunk:     #读到文件的末尾，退出循环
                     break
                 md5_obj.update(chunk)

            #计算md5值
            md5_hex = md5_obj.hexdigest()
            return md5_hex

    except Exception as e:   #如果有异常
        logger.error(f'计算文件{file_path}md5值失败，{str(e)}')
        return None

#返回文件夹内的文件列表
def listdir_with_allowed_type(path:str, allowed_types:tuple[str]):
    files=[]

    #判断文件夹是否存在
    if not os.path.isdir(path):
        logger.error(f"[获取文件夹内的文件]{path}不是文件夹")
        return allowed_types

    for f in os.listdir(path):
        #文件夹内的文件符合要求的文件类型
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))

    #返回，设置为只读
    return tuple(files)


#加载PDF文件的函数
def pdf_loader(file_path:str,passwd=None)->list[Document]:
    return PyPDFLoader(file_path,passwd).load()

#加载txt文件的函数
def txt_loader(file_path:str)->list[Document]:
    return TextLoader(file_path,encoding="utf-8").load()




