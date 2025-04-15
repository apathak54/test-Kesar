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
    model="gpt-4o",
    temperature=0
)

# Define the prompt templates
positive_test_case_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a test case generation expert. Generate positive test cases based on the acceptance criteria. Here are some example positive test cases for reference:\n" + JsonData.POSITIVE_TEST_CASES_EXAMPLE),
    ("human", "{input}")
])

negative_test_case_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a test case generation expert. Generate negative test cases based on the acceptance criteria and previous positive test cases. Here are some example negative test cases for reference:\n" + JsonData.NEGATIVE_TEST_CASES_EXAMPLE),
    ("human", "{input}")
])

def fetch_relevant_context(query: str, collection_name: str = "testkesar", limit: int = 3) -> str:
    """Fetch relevant context from Qdrant based on the query"""
    try:
        # Convert query to embedding using OpenAI
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
        query_embedding = embeddings.embed_query(query)
        
        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        
        # Combine relevant contexts
        contexts = []
        for result in search_results:
            if hasattr(result, 'payload') and 'content' in result.payload:
                contexts.append(result.payload['content'])
        
        return "\n\n".join(contexts) if contexts else ""
    except Exception as e:
        print(f"Error fetching context from Qdrant: {e}")
        return ""

def create_positive_test_cases(state: AgentState) -> AgentState:
    """Node 1: Create positive test cases"""
    messages = state["messages"]
    last_message = messages[-1]["content"]
    
    # Fetch relevant context from Qdrant
    context = fetch_relevant_context(last_message)
    
    # Generate positive test cases with context
    chain = positive_test_case_prompt | llm
    response = chain.invoke({
        "input": f"Context from similar test cases:\n{context}\n\nCurrent PBI and Acceptance Criteria:\n{last_message}"
    })
    
    # Update state
    state["test_cases"].append(response.content)
    state["current_stage"] = "positive_test_cases"
    
    return state

def verify_positive_test_cases(state: AgentState) -> AgentState:
    """Node 2: Verify positive test cases"""
    messages = state["messages"]
    last_message = messages[-1]["content"]
    positive_cases = state["test_cases"][-1]
    
    # Fetch relevant context from Qdrant
    context = fetch_relevant_context(f"{last_message}\n{positive_cases}")
    
    # Create verification prompt
    verification_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a test case verification expert. Review the positive test cases and ensure they are complete, accurate, and cover all acceptance criteria. If there are issues, provide corrected test cases. Here are some example positive test cases for reference:\n" + JsonData.POSITIVE_TEST_CASES_EXAMPLE),
        ("human", f"Context from similar test cases:\n{context}\n\nPBI and Acceptance Criteria:\n{last_message}\n\nGenerated Positive Test Cases:\n{positive_cases}\n\nPlease verify and provide corrected test cases if needed.")
    ])
    
    # Verify test cases
    chain = verification_prompt | llm
    response = chain.invoke({})
    
    # Update state with verified test cases
    state["test_cases"][-1] = response.content
    state["current_stage"] = "verified_positive_test_cases"
    
    return state

def create_negative_test_cases(state: AgentState) -> AgentState:
    """Node 3: Create negative test cases"""
    messages = state["messages"]
    last_message = messages[-1]["content"]
    positive_cases = state["test_cases"][-1]
    
    # Fetch relevant context from Qdrant
    context = fetch_relevant_context(f"{last_message}\n{positive_cases}")
    
    # Generate negative test cases with context
    chain = negative_test_case_prompt | llm
    response = chain.invoke({
        "input": f"Context from similar test cases:\n{context}\n\nPBI and Acceptance Criteria:\n{last_message}\n\nPrevious positive test cases:\n{positive_cases}"
    })
    
    # Update state
    state["test_cases"].append(response.content)
    state["current_stage"] = "negative_test_cases"
    
    return state

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("create_positive_test_cases", create_positive_test_cases)
workflow.add_node("verify_positive_test_cases", verify_positive_test_cases)
workflow.add_node("create_negative_test_cases", create_negative_test_cases)
workflow.add_node("end", lambda x: x)  # Add end node with identity function

# Add edges
workflow.add_edge("create_positive_test_cases", "verify_positive_test_cases")
workflow.add_edge("verify_positive_test_cases", "create_negative_test_cases")
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
    
    # Store the input in Qdrant for future reference
    try:
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
        input_embedding = embeddings.embed_query(state["messages"][-1]["content"])
        
        qdrant_client.upsert(
            collection_name="testkesar",
            points=[
                models.PointStruct(
                    id=hash(state["messages"][-1]["content"]),  # Simple hash as ID
                    vector=input_embedding,
                    payload={"content": state["messages"][-1]["content"]}
                )
            ]
        )
    except Exception as e:
        print(f"Error storing input in Qdrant: {e}")
    
    # Run the workflow
    result = app.invoke(state)
    
    return {
        "positive_test_cases": result["test_cases"][0],
        "negative_test_cases": result["test_cases"][1]
    } 