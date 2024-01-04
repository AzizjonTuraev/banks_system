from langchain import HuggingFaceHub, LLMChain
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate


load_dotenv()

llm = HuggingFaceHub(repo_id="mrm8488/t5-base-finetuned-wikiSQL")
prompt = PromptTemplate(
    input_variables = ["question"],
    template = "Translate English to SQL: {question}"
)
hub_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
print(hub_chain.run("What is the average age of the respondents using a mobile device?"))