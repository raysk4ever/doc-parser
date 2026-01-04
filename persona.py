# from langchain.agents import create_agent
# from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

class PersonaInfo(BaseModel):
    name: str = Field(description="The name of the person")
    role: str = Field(description="The role of the person")
    skills: list[str] = Field(description="The skills of the person")
    unique_traits: list[str] = Field(description="The unique traits of the person")
    hobbies: list[str] = Field(description="The hobbies of the person")
    websites: list[str] = Field(description="The websites of the person")
    phone: str = Field(description="The phone number of the person")
    email: str = Field(description="The email address of the person")

# ollama_model = ChatOllama(model='qwen2.5:7b')

# test = ollama_model.invoke([
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ])

# print(test, "test")

# persona_agent = create_agent(
#     model=ollama_model,
#     response_format=PersonaInfo
# )

with open("resume.md", "r") as f:
    resume = f.read()

# print(len(resume), "resume")

# result = persona_agent.invoke({
#     "messages": [
#         {
#             "role": "user",
#             "content": """Extract info from resume: {resume}"""
#         }
#     ]
# })

# print(result, "result")


from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")

ollama_model = ChatOllama(model='qwen2.5:7b', temperature=0)
agent = create_agent(
    model=ollama_model,
    response_format=PersonaInfo  # Auto-selects ProviderStrategy
)
print("")
result = agent.invoke({
    "messages": [{"role": "user", "content": f"Extract info from resume below: {resume}"}]
})

print(result["structured_response"])
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')