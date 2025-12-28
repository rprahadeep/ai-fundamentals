from typing import TypedDict
from langgraph.graph import StateGraph


# --------------------------------------------------
# 1️⃣ Define the STATE schema
# --------------------------------------------------
class AgentState(TypedDict):
    name: str
    age: str
    final: str


# --------------------------------------------------
# 2️⃣ Create the graph with the state schema
# --------------------------------------------------
graph = StateGraph(AgentState)


# --------------------------------------------------
# 3️⃣ First node
# --------------------------------------------------
# Reads `name` from the state
# Writes an initial value to `final`
def first_node(state: AgentState) -> AgentState:
    """First step in the sequence"""
    return {
        "final": state["name"]
    }


# --------------------------------------------------
# 4️⃣ Second node
# --------------------------------------------------
# Reads the updated `final` and `age`
# Appends age to the string
def second_node(state: AgentState) -> AgentState:
    return {
        "final": state["final"] + state["age"]
    }


# --------------------------------------------------
# 5️⃣ Register nodes in the graph
# --------------------------------------------------
graph.add_node("first", first_node)
graph.add_node("second", second_node)


# --------------------------------------------------
# 6️⃣ Define execution order (edges)
# --------------------------------------------------
# Execution flow:
# entry -> first -> second -> finish
graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.set_finish_point("second")


# --------------------------------------------------
# 7️⃣ Compile the graph
# --------------------------------------------------
app = graph.compile()


# --------------------------------------------------
# 8️⃣ Invoke the graph with initial state
# --------------------------------------------------
results = app.invoke({
    "name": "prahadeep",
    "age": "21"
})


# --------------------------------------------------
# 9️⃣ Final output
# --------------------------------------------------
print(results)
