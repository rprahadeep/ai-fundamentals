from typing import TypedDict
from langgraph.graph import StateGraph


# --------------------------------------------------
# 1️⃣ Define the STATE SCHEMA
# --------------------------------------------------
# This TypedDict defines the structure of the graph state.
# Every node in this graph will:
# - Receive this state as input
# - Return a partial update to this state
class AgentState(TypedDict):
    message: str


# --------------------------------------------------
# 2️⃣ Create the graph with the state schema
# --------------------------------------------------
# StateGraph enforces that all nodes obey AgentState
graph = StateGraph(AgentState)


# --------------------------------------------------
# 3️⃣ Define a node (graph step)
# --------------------------------------------------
# Each node:
# - Takes the current state as input
# - MUST NOT mutate it in-place
# - Returns a dict with updated fields
def greeting(state: AgentState) -> AgentState:
    return {
        "message": "Hello " + state["message"]
    }


# --------------------------------------------------
# 4️⃣ Add the node to the graph
# --------------------------------------------------
# "greeter" is the node name used inside the graph
graph.add_node("greeter", greeting)


# --------------------------------------------------
# 5️⃣ Define graph flow
# --------------------------------------------------
# Entry point: where execution starts
graph.set_entry_point("greeter")

# Finish point: where execution stops
graph.set_finish_point("greeter")


# --------------------------------------------------
# 6️⃣ Compile the graph into an executable app
# --------------------------------------------------
app = graph.compile()


# --------------------------------------------------
# 7️⃣ Invoke the graph with an initial state
# --------------------------------------------------
# The input MUST match AgentState
result = app.invoke({"message": "prahadeep"})


# --------------------------------------------------
# 8️⃣ Read the final state
# --------------------------------------------------
print(result["message"])
