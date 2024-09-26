from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from config import ModelType


def extract_function_params(prompt, function):
    function_name = function[0]["function"]["name"]
    arg_name = list(function[0]["function"]["parameters"]['properties'].keys())[0]

    model = ChatOpenAI(
        model=ModelType.gpt4o,
    )

    model = model.bind_tools(function, tool_choice=function_name)

    messages = [SystemMessage(prompt)]
    tool_call = model.invoke(messages).tool_calls
    prop = tool_call[0]['args'][arg_name]

    return prop


def summarize_content(content):
    prompt = (
        "Below is the website content, I want to get useful content from here. However, the website content is confusing, messy, and disorganized.\n"
        "To help me, please remove any unnecessary information and return the cleaned content in an organized manner in English.\n"
        f"Please return within 300 words.\n###\n{content}\n###\n"
    )

    model = ChatOpenAI(
        model="gpt-4o-mini",
    )
    messages = [SystemMessage(prompt)]
    summarized_content = model.invoke(messages).content

    return summarized_content
