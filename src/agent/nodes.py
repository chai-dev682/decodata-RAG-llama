from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from config import ModelType, get_prompt_template, PromptTemplate
from src.models.graph_state import GraphState
from src.utils.str_utils import messages_to_text

model = ChatOpenAI(
    model=ModelType.gpt4o,
)

def query_transformation_node(state: GraphState) -> GraphState:
    prompt = get_prompt_template(PromptTemplate.QUERY_TRANSFER).format(conversation=messages_to_text(state.messages))
    messages = [SystemMessage(prompt)]
    summarized_content = model.invoke(messages).content
    state.query = summarized_content

    return state

def data_retrieval_node(state: GraphState) -> GraphState:
    return state