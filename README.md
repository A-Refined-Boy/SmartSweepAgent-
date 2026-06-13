# SmartSweepAgent 🤖

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SmartSweepAgent** 是一个基于 ReAct 架构的智能客服 Agent，具备工具调用、RAG 检索增强和动态提示词切换能力。

## ✨ 核心特性

- 🧠 **ReAct 架构**：推理与行动结合的智能体设计
- 🔧 **工具调用系统**：自动调用天气、用户信息、数据检索等外部工具
- 📚 **RAG 检索增强**：从向量数据库中检索相关知识，提升回答质量
- 🔄 **动态提示词切换**：根据上下文自动切换普通对话/报告生成模式
- 💬 **流式对话**：实时输出回复，提升用户体验
- 📊 **外部数据集成**：支持读取用户使用记录（效率、耗材等）

## 🏗️ 系统架构
用户输入 → Agent调度 → 工具调用/RAG检索 → 模型推理 → 流式输出
↓
动态提示词切换
↓
中间件监控与日志
## 📁 项目结构
SmartSweepAgent/
├── agent/
│ ├── react_agent.py # Agent 核心创建
│ └── tools/
│ ├── agent_tools.py # 工具定义
│ └── middleware.py # 中间件（监控、日志、提示词切换）
├── rag/
│ ├── rag_service.py # RAG 总结服务
│ └── vector_store.py # 向量数据库管理
├── model/
│ └── factory.py # 大模型工厂
├── utils/
│ ├── config_handler.py # 配置管理
│ ├── file_handler.py # 文件处理
│ ├── logger_handler.py # 日志管理
│ ├── path_tool.py # 路径工具
│ └── prompt_text_loader.py # 提示词加载
├── config/
│ ├── agent.yml # Agent 配置
│ ├── chroma.yml # 向量库配置
│ ├── prompts.yml # 提示词路径
│ └── rag.yml # 模型配置
├── prompts/
│ ├── main_prompt.txt # 主提示词
│ ├── rag_summarize.txt # RAG 总结提示词
│ └── report_prompt.txt # 报告生成提示词
├── data/ # 知识库数据
├── logs/ # 日志文件
├── app.py # Streamlit 界面
└── requirements.txt # 依赖清单

📊 使用示例
①普通对话模式
用户：我今天适合洗地吗？
Agent：根据您所在的深圳天气（晴天，26℃），今天非常适合洗地作业。

②报告生成模式
用户：帮我生成用户1001在2025-03的使用报告
Agent：生成包含特征、效率、耗材对比的详细报告...
📄 License
MIT License

👤 作者
A-Refined-Boy

⭐ 如果这个项目对你有帮助，欢迎 Star！
