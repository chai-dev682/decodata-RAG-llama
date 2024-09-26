from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph
from langchain_core.messages import SystemMessage
from typing import List
from logging import getLogger

from config import ModelType, get_prompt_template, PromptTemplate
from src.agent.nodes import query_transformation_node, data_retrieval_node
from scripts.query_pinecone import query_pinecone

from src.models.graph_state import GraphState
from src.models.models import Message
from src.utils.str_utils import messages_to_text

logger = getLogger('decodata')


class Agent:

    def __init__(self):
        self.data_retrieval_graph = self._build_data_retrieval_graph()
        logger.debug("Initializing Agent")
        self.system_prompt = get_prompt_template(PromptTemplate.SYSTEM_PROMPT)

    @staticmethod
    def _get_initial_state(messages: List[Message]) -> GraphState:
        return GraphState(messages=messages)

    @staticmethod
    def _build_data_retrieval_graph():
        workflow = StateGraph(state_schema=GraphState)
        workflow.add_node("query_transformation_node", query_transformation_node)
        workflow.add_node("data_retrieval_node", data_retrieval_node)

        workflow.add_edge("query_transformation_node", "data_retrieval_node")

        workflow.set_entry_point("query_transformation_node")
        workflow.set_finish_point("data_retrieval_node")
        workflow = workflow.compile()

        return workflow

    def generate_query(self, messages):
        init_state = self._get_initial_state(
            [Message(role=message["role"], content=message["content"]) for message in messages])

        result = self.data_retrieval_graph.invoke(init_state)
        return result

    def retrieve_data(self, model_type: ModelType, query, subdirectory_name, conversation):
        result = query_pinecone(query, subdirectory_name = subdirectory_name, top_k=1)
        prompt = get_prompt_template(PromptTemplate.ANSWER).format(content=result,
                                                                   conversation=messages_to_text(conversation))
        model = ChatOpenAI(model=model_type)
        answer = model.invoke([SystemMessage(prompt)]).content

        return answer

    def invoke(self, model_type: ModelType, messages, subdirectory_name):
        query_state = self.generate_query(messages)
        return self.retrieve_data(model_type, query_state["query"], subdirectory_name, query_state["messages"])