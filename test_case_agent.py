from typing import Dict, List, TypedDict, Annotated
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import Graph, StateGraph
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import JsonData
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the state type
class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    test_cases: List[str]
    current_stage: str

# Initialize Qdrant client for memory
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Create collection if it doesn't exist
try:
    qdrant_client.create_collection(
        collection_name="testkesar",
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )
except Exception:
    pass

# Initialize OpenAI model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Define the prompt templates
positive_test_case_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a test case generation expert. Generate positive test cases based on the acceptance criteria."),
    ("human", "{input}")
])

negative_test_case_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a test case generation expert. Generate negative test cases based on the acceptance criteria and previous positive test cases."),
    ("human", "{input}")
])

# Define the nodes
def create_positive_test_cases(state: AgentState) -> AgentState:
    """Node 1: Create positive test cases"""
    messages = state["messages"]
    last_message = messages[-1]["content"]
    
    # Generate positive test cases
    chain = positive_test_case_prompt | llm
    response = chain.invoke({"input": last_message})
    
    # Update state
    state["test_cases"].append(response.content)
    state["current_stage"] = "positive_test_cases"
    
    return state

def create_negative_test_cases(state: AgentState) -> AgentState:
    """Node 2: Create negative test cases"""
    messages = state["messages"]
    last_message = messages[-1]["content"]
    positive_cases = state["test_cases"][-1]
    
    # Generate negative test cases
    chain = negative_test_case_prompt | llm
    response = chain.invoke({"input": f"{last_message}\n\nPrevious positive test cases:\n{positive_cases}"})
    
    # Update state
    state["test_cases"].append(response.content)
    state["current_stage"] = "negative_test_cases"
    
    return state

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("create_positive_test_cases", create_positive_test_cases)
workflow.add_node("create_negative_test_cases", create_negative_test_cases)
workflow.add_node("end", lambda x: x)  # Add end node with identity function

# Add edges
workflow.add_edge("create_positive_test_cases", "create_negative_test_cases")
workflow.add_edge("create_negative_test_cases", "end")

# Set entry point
workflow.set_entry_point("create_positive_test_cases")

# Set finish point
workflow.set_finish_point("end")

# Compile the graph
app = workflow.compile()

def process_input(pbi: str, additional_details: str = "", positive_test_cases: str = "", negative_test_cases: str = "") -> Dict:
    """Process the input and generate test cases"""
    # Initialize state
    state = {
        "messages": [{"role": "user", "content": f"PBI:\n{pbi}\n\nAdditional Details:\n{additional_details}\n\nPositive Test Cases:\n{positive_test_cases}\n\nNegative Test Cases:\n{negative_test_cases}"}],
        "test_cases": [],
        "current_stage": "start"
    }
    
    # Run the workflow
    result = app.invoke(state)
    
    return {
        "positive_test_cases": result["test_cases"][0],
        "negative_test_cases": result["test_cases"][1]
    } 