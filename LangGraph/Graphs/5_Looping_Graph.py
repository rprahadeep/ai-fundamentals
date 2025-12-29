from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
import random


# -----------------------------
# 1. Define the shared graph state
# -----------------------------
class AgentState(TypedDict):
    name: str            # Stores the greeting message
    number: List[int]    # Accumulates random numbers
    counter: int         # Controls the loop


# -----------------------------
# 2. Create the graph with this state schema
# -----------------------------
graph = StateGraph(AgentState)


# -----------------------------
# 3. First node: initializes / modifies the state
# -----------------------------
def greeting_node(state: AgentState) -> AgentState:
    """
    Initializes the workflow:
    - Updates the name with a greeting
    - Initializes the loop counter
    """
    return {
        "name": f"hi there {state['name']}",
        "counter": 0
        # 'number' is intentionally not returned here;
        # LangGraph will merge this with the existing state
    }


# -----------------------------
# 4. Looping node: adds random numbers
# -----------------------------
def random_node(state: AgentState) -> AgentState:
    """
    Appends a random integer (0-10) to the list
    and increments the counter.
    """
    return {
        "number": state["number"] + [random.randint(0, 10)],
        "counter": state["counter"] + 1
    }


# -----------------------------
# 5. Conditional function for looping
# -----------------------------
def should_continue(state: AgentState) -> bool:
    """
    Controls whether the graph should keep looping.
    Returns True to continue, False to stop.
    """
    return state["counter"] < 6


# -----------------------------
# 6. Register nodes in the graph
# -----------------------------
graph.add_node("greet", greeting_node)
graph.add_node("random", random_node)


# -----------------------------
# 7. Define execution flow
# -----------------------------
graph.add_edge(START, "greet")     # Start → greeting
graph.add_edge("greet", "random")  # greeting → random generator

# Conditional loop:
# - If True → go back to "random"
# - If False → terminate the graph
graph.add_conditional_edges(
    "random",
    should_continue,
    {
        True: "random",
        False: END
    }
)


# -----------------------------
# 8. Compile and run the graph
# -----------------------------
app = graph.compile()

result = app.invoke({
    "name": "prahadeep",
    "number": []  # IMPORTANT: initialize list before first use
})

print(result)
