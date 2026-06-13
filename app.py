import time
import streamlit as st
from agent.react_agent import ReactAgent

# 设置页面的标题
st.title("智扫通机器人智能客服")
st.divider()

#刚进入页面，客服自动发送的消息
#并且保存用户与客服的历史对话
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"assistant","content":"你好！请问有什么需要帮助的吗？"}]

#创建AI Agent智能体对象
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

#打印输出用户与客服的历史对话信息
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 4. 设置输入栏为用户提问
prompt = st.chat_input("在这里发消息...")

if prompt:          # 如果输入非空

    #保存用户的提问
    st.session_state["messages"].append({"role":"user", "content": prompt})
    #打印输出用户的提问
    st.chat_message("user").write(prompt)

    #获取流式输出的回复
    res_stream = st.session_state["agent"].execute_stream(prompt)

    # 定义一个str来存储流式输出中的内容
    str_list = []


    # 设置一个函数把流式输出的内容提取到list中
    def capture_str(generator, str_list):
        for chunk in generator:
            str_list.append(chunk)

            #让输出更加流水化
            for char in chunk:
                #设置流水输出的速度
                time.sleep(0.01)
                yield char

    with st.spinner("客服输入中....."):
        # 打印输出客服的回复
        st.chat_message("assistant").write(capture_str(res_stream, str_list))

    # 保存客服的回复，注意：只保留最后一条，不保留客服的思考过程
    st.session_state["messages"].append({"role": "assistant", "content": str_list[-1]})

    # 重新运行以更新界面
    st.rerun()

