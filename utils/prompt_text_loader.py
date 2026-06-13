from utils.config_handler import prompts_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

#加载主提示词
def load_system_prompts():
    try:
        #获取存放主提示词的文件的相对路径
        relative_system_prompt_path = prompts_config['main_prompt_path']
        #获取绝对路径
        system_prompt_path = get_abs_path(relative_system_prompt_path)
    except KeyError as e:
        logger.error(f"[load_system_prompts]在prompts.yml中没有main_prompt_path配置项")
        raise e

    #读取主提示词的文件
    try:
        return open(system_prompt_path,"r",encoding="utf-8").read()
    except  Exception as e:
        logger.error(f"[load_system_prompts]解析主提示词出错")
        raise e


#加载RAG总结提示词
def load_rag_prompts():
    try:
        #获取存放主提示词的文件的相对路径
        relative_rag_prompt_path = prompts_config['rag_summarize_prompt_path']
        #获取绝对路径
        system_rag_prompt_path = get_abs_path(relative_rag_prompt_path)
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在prompts.yml中没有rag_summarize_prompt_path配置项")
        raise e

    #读取主提示词的文件
    try:
        return open(system_rag_prompt_path,"r",encoding="utf-8").read()
    except  Exception as e:
        logger.error(f"[load_rag_prompts]解析RAG总结提示词出错")

#加载生成报告提示词
def load_report_prompts():
    try:
        #获取存放主提示词的文件的相对路径
        relative_report_prompt_path = prompts_config['report_prompt_path']
        #获取绝对路径
        report_prompt_path = get_abs_path(relative_report_prompt_path)
    except KeyError as e:
        logger.error(f"[load_report_prompts]在prompts.yml中没有report_prompt_path配置项")
        raise e

    #读取主提示词的文件
    try:
        return open(report_prompt_path,"r",encoding="utf-8").read()
    except  Exception as e:
        logger.error(f"[load_report_prompts]解析主提示词出错")
