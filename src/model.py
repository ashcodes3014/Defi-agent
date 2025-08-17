from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2,google_api_key=os.getenv("GOOGLE_API_KEY"))
parser = StrOutputParser()

prompt = PromptTemplate(
    template="""
You are a professional **Blockchain and Trading Expert**.  
Answer user questions about cryptocurrency, DeFi, trading strategies, blockchain technology, and tokenomics.  

Guidelines:
- Provide **short, well-structured answers not too long** (4–6 sentences or 2-3 lines).  
- **Return only plain text** — do NOT include JSON, markdown, code blocks, or any extra formatting.  
- Be concise and crisp.  
- If uncertain, clearly mention limitations.  

Conversation so far:
{context}

User Question:
{question}

Answer (plain text, structured, max 6-10 sentences): 

eg : "Bitcoin halving is an event that reduces the block reward by 50%, impacting supply and often influencing price."

""",
    input_variables=['context', 'question']
)


crypto_chain = prompt | llm | parser


def format_context(context_dict_list: list[dict]) -> str:
    formatted = []
    for conv in context_dict_list:
        q = conv.get("Query", "")
        a = conv.get("Ans", "")
        formatted.append(f"Query : {q}\nAns : {a}")
    return "\n\n".join(formatted)


def ask_crypto_bot(context_dict: list[dict], question: str) -> str:
    context = format_context(context_dict)
    response = crypto_chain.invoke({"context": context, "question": question})
    return response


