import os
import random
from langchain_core.tools import tool
from rag.rag_service import  RagSummarizeService
from utils.config_handler import  agent_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

rag = RagSummarizeService()

user_ids = ["1001","1002","1003","1004","1005","1006","1007","1008","1009","1010",]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

external_data = {}

#获取模型对检索结果结合提示词模板做出的rag提示词内容的总结
@tool(description="从向量存储中检索参考资料")
def rag_summarize(query:str)->str:
    return rag.rag_summarize(query)

#获取天气等信息
@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city:str)->str:
    return f"城市{city}天气为晴天，气温为26摄氏度，空气湿度50%，南风1级，AQI21，最近6小时降雨概率极低"

#获取用户所在城市的名称
@tool(description="获取用户所在城市的名称,并以字符串的形式返回")
def get_user_location()->str:
    return random.choice(["深圳","广州","湛江"])

#获取用户的id
@tool(description="获取用户的ID，以字符串的形式返回")
def get_user_id()->str:
    return random.choice(user_ids)


#获取当前月份
@tool(description="获取当前月份，以字符串的形式返回")
def get_current_month()->list:
    return random.choice(month_arr)


#从文件中读取指定用户在指定月份的使用记录
#并以下面字典的格式保存下来
"""
{
    "user_id": {
        "month" : {"特征": xxx, "效率": xxx, ...}
        "month" : {"特征": xxx, "效率": xxx, ...}
        "month" : {"特征": xxx, "效率": xxx, ...}
        ...
    },
    "user_id": {
        "month" : {"特征": xxx, "效率": xxx, ...}
        "month" : {"特征": xxx, "效率": xxx, ...}
        "month" : {"特征": xxx, "效率": xxx, ...}
        ...
    },
    ...
}"""
def generate_external_data():
    if not external_data:
        external_data_path=get_abs_path(agent_config["external_data_path"])
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, 'r', encoding='utf-8') as f:
            for line in f.readlines()[1:]:         #[1:]表示不要第一行
                #对每一行使用分割器，以”，“作为分割符
                arr: list[str] = line.strip().split(",")

                #replace('"',"")表示符号"替换成空格符
                user_id: str = arr[0].replace('"',"")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    # 创建一个external_data[user_id]的字典
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }

#获取指定用户在指定月份的使用记录
@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以字符串的形式返回，如果未检索到返回空字符串")
def fetch_external_data(user_id:str,month:str)->str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户")
        return ""

#当用户问题为报告，会调用该工具
@tool(description="调用后会触发中间件自动为上下文信息注入report信息，为后续提示词切换做准备")
def fill_context_for_report():
    return "fill_context_for_report已调用"









