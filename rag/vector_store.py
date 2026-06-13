import os
from langchain_chroma import Chroma
from utils.config_handler import  chroma_config
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import  get_abs_path
from utils.file_handler import  pdf_loader,txt_loader,listdir_with_allowed_type,get_file_md5
from utils.logger_handler import logger
from langchain_core.documents import Document

class VectorStoreService(object):

    #初始化
    def __init__(self):
        #向量数据库
        self.vector_store = Chroma(
            # 向量数据库的表名
            collection_name=chroma_config["collection_name"],
            #嵌入模型
            embedding_function=embed_model,
            # 向量数据库的存放文件夹
            persist_directory=chroma_config["persist_directory"],
        )

        #字符分割器
        self.spliter = RecursiveCharacterTextSplitter(
            # 每段的最大字数
            chunk_size=chroma_config["chunk_size"],
            # 段与段之间可以重复的最大字数
            chunk_overlap= chroma_config["chunk_overlap"],
            # 分隔符
            separators= chroma_config["separators"],
            #设置统计字数的函数
            # length_function= chroma_config["length_function"],
            length_function= len,
        )

    # 获取检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})

    # 从数据文件夹中读取数据文件，转为向量形式后存入向量库
    def read_file_load_document(self):

        # 要计算md5值，并通过md5值进行去重化处理
        # (1)通过md5值判断文件是否已经加载过向量数据库的函数
        def check_md5_hex(md5_hex: str):
            # 如果md5.text不存在,说明向量数据库没有存入给任何文件，即刚开始向向量数据库中存数据
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                # 创建md5.text文件
                open(get_abs_path(chroma_config["md5_hex_store"]), "w", encoding="utf-8").close()
                return False
            # 遍历md5.text，判断文件是否已经加载过向量数据库
            with open(get_abs_path(chroma_config["md5_hex_store"]),"r",encoding="utf-8") as f:
                for line in f.readlines():
                    # 去掉空格和回车符
                    line = line.strip()
                    if line == md5_hex:  # 已经加载过向量数据库
                        return True

                return False  # 没有加载过向量数据库

        # (2)保存md5值到md5.text文件中
        def save_md5_hex(md5_hex: str):
            # 以追加的形式写入md5.text
            with open(get_abs_path(chroma_config["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_hex + "\n")

        # (3)生成md5值，在file_handler中实现了get_file_md5函数用于获取文件的md5值

        # 加载文件
        def get_file_document(read_path: str):
            # 如果读取到是txt文件
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            # 读取到是pdf文件
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []  # 没有txt文件和pdf文件

        # 开始从数据文件夹中加载并读取数据文件，转为向量形式后存入向量库
        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            # 获取文件的md5值
            md5_hex = get_file_md5(path)

            # 判断文件是否已经加载过向量数据库
            if check_md5_hex(md5_hex):
                logger.info(f"[加载数据库]{path}内容已经存在向量数据库内，跳过")
                continue

            try:
                # 加载文件
                documents: list[Document] = get_file_document(path)

                if not documents:
                    logger.warning(f"[加载数据库]{path}内没有有效的文本内容，跳过")
                    continue

                # 使用分割器
                split_document = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载数据库]{path}分段后没有有效的文本内容，跳过")
                    continue

                # 将数据存入向量数据库
                self.vector_store.add_documents(split_document)

                # 保存md5到md5.text文件中
                save_md5_hex(md5_hex)

                logger.info(f"[加载数据库]{path}内容成功加载入向量数据库")
            except Exception as e:
                # exc_info=True会详细指出错误
                logger.error(f"[加载数据库]{path}内容加载失败！{str(e)}", exc_info=True)


