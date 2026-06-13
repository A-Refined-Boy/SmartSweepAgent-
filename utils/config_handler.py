"""
获取参数数据
"""
import yaml
from utils.path_tool import get_abs_path


#获取rag有关的参数
def lod_rag_config(config_path:str=get_abs_path('config/rag.yml'),encoding='utf-8'):
    with open(config_path,'r',encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)


#获取向量数据库有关的参数
def lod_chroma_config(config_path:str=get_abs_path('config/chroma.yml'),encoding='utf-8'):
    with open(config_path,'r',encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)


#获取存放提示词有关的参数的文件的相对路径
def lod_prompts_config(config_path:str=get_abs_path('config/prompts.yml'),encoding='utf-8'):
    with open(config_path,'r',encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)


#获取agent有关的参数
def lod_agent_config(config_path: str = get_abs_path('config/agent.yml'), encoding='utf-8'):
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


#快捷获取有关的参数
rag_config = lod_rag_config()
chroma_config = lod_chroma_config()
prompts_config = lod_prompts_config()
agent_config = lod_agent_config()

