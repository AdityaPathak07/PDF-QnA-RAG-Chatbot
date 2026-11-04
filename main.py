from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader         
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.vectorstores import InMemoryVectorStore
import streamlit as st
from time import sleep

load_dotenv()
google_api_key = st.secrets["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "messages" not in st.session_state:
    st.session_state.messages = []

def doc_process(path):

# LOADER
  loader = PyPDFLoader(path)
  doc = loader.load()

# SPLITTING
  splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
  docs = splitter.split_documents(doc)

# EMBEDDING
  embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

# VECTOR STORE
  vector_db = InMemoryVectorStore.from_documents(
    documents=docs,
    embedding=embeddings
 )

  st.session_state.vector_db = vector_db
  st.session_state.document_uploaded = True

st.subheader("QnA PDF Chatbot")

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if not st.session_state.document_uploaded:
    file = st.file_uploader(label="Select your PDF", type="pdf")
    if file:
        with open("uploaded_document.pdf", "wb") as f:
            f.write(file.getvalue())
        with st.spinner("Loading..."):
            doc_process("uploaded_document.pdf")
        st.markdown("Uploaded Successfully")
        sleep(2)
        st.rerun()

if st.session_state.document_uploaded and st.session_state.vector_db:
    
    for oneMessage in st.session_state.messages:
        role = oneMessage["role"]
        content = oneMessage["content"]

        st.chat_message(role).markdown(content)

    query = st.chat_input("Ask any query")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").markdown(query)
        documents = st.session_state.vector_db.similarity_search(query, k=2)
        context = ""
        for doc in documents:
          context = context + doc.page_content + "\n\n"

        prompt = f""" You are helpful AI assistant who gives answer as per the context.
        Context: {context}
        question: {query} """
        result = llm.invoke(prompt)

        print(result.content[0]["text"])
        st.session_state.messages.append({"role": "ai", "content": result.content[0]["text"]})
        st.chat_message("ai").markdown(result.content[0]["text"])