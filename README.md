# 学习《大模型工程化：AI驱动下的数据体系》
## 安装环境
1. 安装Python
````bash
conda create -n AI-data python=3.12.1
conda activate AI-data
````
2. 安装OpenAI依赖库
```bash
conda install openai
#验证是否安装成功
python -c "import openai;print('install openai success')"
```
3. 安装LangChain
```bash
pip install  langchain  langchain-experimental langchain-community langchain-core langchain_openai
# 验证是否安装成功
 python -c "from langchain_openai import OpenAI; chat=OpenAI();print('install LangChain success')"
```