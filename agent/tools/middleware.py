from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import  logger
from utils.prompt_text_loader import load_report_prompts, load_system_prompts


#工具执行时的监控
@wrap_tool_call
def monitor_tool(
        #请求的数据封装
        request: ToolCallRequest,
        #执行的函数
        handler: Callable[[ToolCallRequest],ToolMessage | Command],
)->ToolMessage | Command:
    #添加日志监控
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        #添加日志监控
        logger.info(f"[tool monitor]工具：{request.tool_call['name']}调用成功")

        #监控fill_context_for_report工具是否被调用
        #如果被调用了，这里会自动为上下文信息注入report信息，为后续提示词切换做准备
        if request.tool_call['name'] == "fill_context_for_report":
            #request.runtime.context["report"]平时都是False
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.info(f"[tool monitor]工具：{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e

#模型监控
@before_model
def log_before_model(
        #整个Agent智能体的状态记录
        state: AgentState,
        #记录了整个执行过程中的上下文信息
        runtime:Runtime,
):
    #添加日志监控
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")
    logger.info(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content}")

    return None


#动态切换提示词
@dynamic_prompt       #在每一次调用提示词模板生成提示词之前，都会调用
def report_prompt_switch(request: ModelRequest):

    #上下文中如果有report，则返回True,否则返回False
    is_report = request.runtime.context.get("report", False)
    if is_report:   #有report,则加载report提示词模板
        return load_report_prompts()

    return load_system_prompts()      #没有report,则加载system提示词模板,说明默认都是加载system提示词模板



