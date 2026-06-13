"""
总结服务类：将用户提问，搜索参考的资料，结合rag总结模板，生成一个rag总结提示词提交给模型，让模型总结回复
"""
from rag.vector_store import VectorStoreService
from utils.prompt_text_loader import  load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

class RagSummarizeService(object):
    #初始化
    def __init__(self):
        #向量数据库管理器
        self.vector_store = VectorStoreService()
        #检索器
        self.retriever = self.vector_store.get_retriever()
        #提示词文本
        self.prompt_text = load_rag_prompts()
        #提示词模块:将提示词文本填入提示词模块
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        #大模型
        self.model = chat_model
        #chain链
        self.chain = self.init_chain()

    #自定义chain链
    def init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    #获取检索器的检索结果
    def retriever_docs(self,query:str)->list[Document]:
        return self.retriever.invoke(query)

    #返回chain链的执行结果，即为大模型对rag提示词内容的总结
    def rag_summarize(self,query:str)->str:

        #获取检索结果
        content_docs = self.retriever_docs(query)

        #提取检索结果中的内容
        content = ""
        count = 0
        for doc in content_docs:
            count += 1
            content += f'【参考资料{count}】：内容：{doc.page_content} | 参考资料的元数据：{doc.metadata}\n'

        #返回大模型对rag提示词内容的总结
        return self.chain.invoke(
            {
                "input":query,
                "context":content,
            }
        )


