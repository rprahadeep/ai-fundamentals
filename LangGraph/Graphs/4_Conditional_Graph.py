from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# --------------------------------------------------
# 1️⃣ Define the STATE schema
# --------------------------------------------------
# This is the single logical state that flows
# through all nodes in the graph.
class AgentState(TypedDict):
    num1: int
    num2: int
    op: str          # operator: "+" or "-"
    final: int       # final computed result


# --------------------------------------------------
# 2️⃣ Create the graph
# --------------------------------------------------
graph = StateGraph(AgentState)


# --------------------------------------------------
# 3️⃣ Define computation nodes
# --------------------------------------------------
# These nodes perform actual work on the state.
# They read values and return a partial update.

def adder(state: AgentState) -> AgentState:
    """Adds num1 and num2"""
    return {
        "final": state["num1"] + state["num2"]
    }


def subtract(state: AgentState) -> AgentState:
    """Subtracts num2 from num1"""
    return {
        "final": state["num1"] - state["num2"]
    }


# --------------------------------------------------
# 4️⃣ Define routing (decision) function
# --------------------------------------------------
# This function DOES NOT modify state.
# It only decides which node should run next.
# It must return a string key.
def decide_next_node(state: AgentState) -> str:
    if state["op"] == "+":
        return "addition_operation"
    elif state["op"] == "-":
        return "subtraction_operation"
    else:
        raise ValueError("Unsupported operator")


# --------------------------------------------------
# 5️⃣ Register nodes
# --------------------------------------------------
# "router" is a passthrough node used only to attach
# conditional edges.
graph.add_node("add", adder)
graph.add_node("subtract", subtract)
graph.add_node("router", lambda state:state)


# --------------------------------------------------
# 6️⃣ Define graph flow
# --------------------------------------------------
# START → router
graph.add_edge(START, "router")

# Conditional routing based on operator
graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "addition_operation": "add",
        "subtraction_operation": "subtract",
    }
)

# Both computation nodes lead to END
graph.add_edge("add", END)
graph.add_edge("subtract", END)


# --------------------------------------------------
# 7️⃣ Compile the graph
# --------------------------------------------------
app = graph.compile()


# --------------------------------------------------
# 8️⃣ Invoke the graph
# --------------------------------------------------
result = app.invoke({
    "num1": 1,
    "num2": 3,
    "op": "+"
})


# --------------------------------------------------
# 9️⃣ Final result
# --------------------------------------------------
print(result)
