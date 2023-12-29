# import
from langchain.document_loaders import TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document

# load the document and split it into chunk
loader = TextLoader("D:/Alex/Documents/TestingLLM/test_file.txt")
documents = loader.load()

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""

prompt = PromptTemplate.from_template(template)
#prompt = hub.pull("rlm/rag-prompt")

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)

API_KEY = "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"
llm_id = "databricks/dolly-v2-3b"
transformer_id = "sentence-transformers/all-MiniLM-L6-v2"

llm = HuggingFaceHub(repo_id=llm_id, huggingfacehub_api_token=API_KEY, model_kwargs={"temperature":0.2, "max_length":64})
retriever = db.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("ready")
while True:
    query = input()
    if not query:
        break
    # query it
    response = chain.invoke(query)
    print(response)