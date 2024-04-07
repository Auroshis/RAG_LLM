import langchain
from langchain.llms import ollama_llama2
from langchain.prompts import PromptTemplate
from langchain.chains import RunnablePassthrough, RunnableLambda
from langchain.document_loaders import PyPDFLoader
from langchain.document_splitters import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import HuggingFaceEmbeddings
from chromadb import Chroma
from chromadb.retriever import filter_complex_metadata
from langchain_community.chat_models import ChatOllama

class ChatBot:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        self.model = ChatOllama(model="llama2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=50)
        self.embedding_model = "all-MiniLM-L6-v2"
        self.memory = ConversationBufferMemory()
        self.memory.save_context({"input": "Hi"}, {"output": "Hi, I am your AI buddy!"})
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. [/INST] </s>
            [INST] Question: {question}
            Context: {context}
            Answer: [/INST]
            """
        )

    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        vector_store = Chroma.from_documents(documents=chunks, embedding=HuggingFaceEmbeddings(self.embedding_model), persist_directory="context")  # Corrected embedding model usage
        vector_store.persist()
        self.retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.6,
            },
        )

    def ask(self, query: str):
        if not self.chain:
            self.chain = langchain.Chain(
                {"context": self.retriever, "question": RunnablePassthrough(history=RunnableLambda(self.memory.retrieve_context))}
                | self.prompt
                | self.model
                | StrOutputParser()
            )
        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
