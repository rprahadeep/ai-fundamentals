from typing import TypedDict, List
from langgraph.graph import StateGraph


# --------------------------------------------------
# 1️⃣ State schema
# --------------------------------------------------
class AgentState(TypedDict):
    values: List[int]
    name: str
    results: str


# --------------------------------------------------
# 2️⃣ Create the graph
# --------------------------------------------------
graph = StateGraph(AgentState)


# --------------------------------------------------
# 3️⃣ Node: process values and name
# --------------------------------------------------
def process_values(state: AgentState) -> AgentState:
    total = sum(state["values"])        # sum the list of integers
    name = state["name"]                # read name from state

    return {
        "results": f"{name} {total}"
    }


# --------------------------------------------------
# 4️⃣ Add node and define flow
# --------------------------------------------------
graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")


# --------------------------------------------------
# 5️⃣ Compile and invoke
# --------------------------------------------------
app = graph.compile()

result = app.invoke({
    "values": [1, 2, 3],
    "name": "prahadeep"
})


# --------------------------------------------------
# 6️⃣ Output
# --------------------------------------------------
print(result["results"])
