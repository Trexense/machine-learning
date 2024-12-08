import argparse
# from dataclasses import dataclass
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma"
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

Do not Generate Any ID (ID: xxxxx) provided to you into the answer expect there are explicit instruction to do so

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if len(results) == 0 or results[0][1] < 0.1:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = genai.GenerativeModel("gemini-1.5-flash")
    #===
    response = model.generate_content(prompt)

    # Extract the text content
    response_text = response.candidates[0].content.parts[0].text
    print(response_text)
    #===


if __name__ == "__main__":
    main()