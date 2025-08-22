from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

chat_history = []

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a professional Blockchain and Trading Expert. "
     "Answer user questions about cryptocurrency, DeFi, trading strategies, blockchain technology, and tokenomics. "
     "Guidelines:\n"
     "- Provide short, well-structured answers (4–6 sentences or 2–3 lines).\n"
     "- Return only plain text — no JSON, markdown, or code formatting.\n"
     "- Be concise and crisp.\n"
     "- If uncertain, clearly mention limitations."
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

crypto_chain = prompt | llm | parser


def ask_crypto_bot(question: str) -> str:
    response = crypto_chain.invoke({"chat_history": chat_history, "question": question})
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))
    return response
