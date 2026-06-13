"""
用于生产模型，为Agent提供大模型
"""
from abc import ABC,abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import  rag_config

class BaseModelFactory(ABC):
    @abstractmethod
    #生产器
    def generator(self)->Optional[Embeddings | BaseChatModel]:
        pass

#生产聊天大模型
class ChatModelFactory(BaseModelFactory):
    def generator(self)->Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_config["chat_model_name"])

#生产嵌入模型
class EmbeddingsFactory(BaseModelFactory):
    def generator(self)->Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"])


#生产出具体的模型
chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()