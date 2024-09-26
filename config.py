from enum import Enum
from os.path import join
import json
from dotenv import load_dotenv

PROJECT_ROOT = ""
LOG_INI = join(PROJECT_ROOT, 'log.ini')
FIXTURES = join(PROJECT_ROOT, 'fixtures', 'hierarchies')
PROMPTS = join(PROJECT_ROOT, 'prompt_template')
FUNCTIONS = join(PROJECT_ROOT, 'function_template')


def load_env():
    load_dotenv()


class ModelType(str, Enum):
    gpt4o = 'gpt-4o'
    gpt4o_mini = 'gpt-4o-mini'
    embedding = "text-embedding-3-large"


class PromptTemplate(Enum):
    SYSTEM_PROMPT = 'system.txt'
    QUERY_TRANSFER = "query_transformation.txt"
    ANSWER = "answer.txt"


class FunctionTemplate(Enum):
    EXAMPLE_FUNCTION = "example_function.json"


def get_prompt_template(prompt_template: PromptTemplate):
    with open(join(PROMPTS, prompt_template.value), "rt") as f:
        return f.read()


def get_function_template(function_template: FunctionTemplate):
    with open(join(FUNCTIONS, function_template.value), "r") as f:
        return json.load(f)

load_env()