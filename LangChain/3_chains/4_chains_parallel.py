from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

# Define prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert product reviewer."),
        ("human", "List the main features of the product {product_name}."),
    ]
)

# Define the templates
pros_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert product reviewer."),
    ("human", "Given these features: {features}, list the pros of these features."),
])

cons_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert product reviewer."),
    ("human", "Given these features: {features}, list the cons of these features."),
])

# Create branch chains
pros_branch_chain = (
    RunnableLambda(lambda x: {"features": x}) 
    | pros_template 
    | model 
    | StrOutputParser()
)

cons_branch_chain = (
    RunnableLambda(lambda x: {"features": x}) 
    | cons_template 
    | model 
    | StrOutputParser()
)

# Create the combined chain using LangChain Expression Language (LCEL)
chain = (
    prompt_template 
    | model
    | StrOutputParser()
    | RunnableParallel(branches={"pros": pros_branch_chain, "cons": cons_branch_chain})
)

# Run the chain
result = chain.invoke({"product_name": "MacBook Pro"})

# Output
print(result)
