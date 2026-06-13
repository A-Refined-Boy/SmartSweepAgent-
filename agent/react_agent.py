"""
创建agent智能体
"""
from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_text_loader import load_system_prompts
from agent.tools.agent_tools import (rag_summarize,get_weather,get_user_id,get_user_location,get_current_month,
                                     fetch_external_data,fill_context_for_report)
from agent.tools.middleware import  monitor_tool,log_before_model,report_prompt_switch

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            #大模型
            model = chat_model,
            #提示词模板
            system_prompt=load_system_prompts(),
            #工具
            tools=[rag_summarize,get_weather,get_user_id,get_user_location,get_current_month,
                   fetch_external_data,fill_context_for_report],
            #中间体
            middleware=[monitor_tool,log_before_model,report_prompt_switch],

        )

    #调用agent，返回流式对象
    def execute_stream(self,query:str):
        #设置输入
        input_dict = {
            "messages": [
                {"role":"user","content":query},
            ]
        }
        # 调用agent，返回流式对象
        #context={"report": False} 设置上下文信息中的"report"为False，即默认调用system_prompt提示词模板
        for chunk in self.agent.stream(input = input_dict,stream_mode="values",context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:    #如果有回复，则以流式返回
                yield latest_message.content.strip() + "\n"



