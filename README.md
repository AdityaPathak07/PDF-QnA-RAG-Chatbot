# 📄 PDF RAG Chatbot

A simple **Retrieval-Augmented Generation (RAG)** chatbot that lets you upload a PDF and ask questions about its content. Built with **Streamlit**, **LangChain**, and **Google Gemini**.

## ✨ Features

- Upload any PDF and chat with it in natural language
- Answers are grounded in the document's content (RAG)
- Semantic search using Google Gemini embeddings
- Clean chat interface with conversation history
- Lightweight: uses an in-memory vector store, so there is no external database to set up

## 🧠 How It Works

```
PDF → Load → Split into chunks → Embed → Vector store
                                              │
User question → Embed → Similarity search (top 2 chunks)
                                              │
                         Context + Question → Gemini LLM → Answer
```

1. **Load**: the PDF is read with `PyPDFLoader`.
2. **Split**: text is divided into chunks of 1000 characters with a 200-character overlap using `RecursiveCharacterTextSplitter`.
3. **Embed**: each chunk is converted to a vector with `GoogleGenerativeAIEmbeddings` (`gemini-embedding-2-preview`).
4. **Store**: vectors are held in LangChain's `InMemoryVectorStore`.
5. **Retrieve**: for each question, the 2 most similar chunks are fetched.
6. **Generate**: the chunks and the question are sent to Gemini (`gemini-3-flash-preview`), which writes the answer.

## 🛠️ Tech Stack

| Component       | Technology                                      |
| --------------- | ----------------------------------------------- |
| UI              | [Streamlit](https://streamlit.io/)              |
| Framework       | [LangChain](https://www.langchain.com/)         |
| LLM             | Google Gemini (`gemini-3-flash-preview`)        |
| Embeddings      | Google Gemini (`gemini-embedding-2-preview`)    |
| Vector Store    | LangChain `InMemoryVectorStore`                 |
| PDF Loader      | `PyPDFLoader`                                   |

## 📋 Prerequisites

- Python 3.9 or higher
- A Google Gemini API key. Get one free from [Google AI Studio](https://aistudio.google.com/app/apikey).

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv venv

   # macOS / Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Or install them manually:

   ```bash
   pip install streamlit python-dotenv pypdf langchain-core langchain-community langchain-text-splitters langchain-google-genai
   ```

4. **Set up your environment variables**

   Create a `.env` file in the project root:

   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

## ▶️ Usage

Run the app (replace `main.py` with your file name):

```bash
streamlit run main.py
```

Then open the URL shown in your terminal (usually `http://localhost:8501`) and:

1. Upload a PDF file.
2. Wait for the "Uploaded Successfully" message.
3. Type your question in the chat box and press Enter.

## 📁 Project Structure

```
.
├── main.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # API key (not committed)
└── README.md
```

## ⚙️ Configuration

You can tweak these values in the code to change the bot's behavior:

| Setting         | Location                          | Default | Description                                   |
| --------------- | --------------------------------- | ------- | --------------------------------------------- |
| `chunk_size`    | `RecursiveCharacterTextSplitter`  | `1000`  | Size of each text chunk                       |
| `chunk_overlap` | `RecursiveCharacterTextSplitter`  | `200`   | Overlap between consecutive chunks            |
| `k`             | `similarity_search`               | `2`     | Number of chunks retrieved per question       |
| `model`         | `ChatGoogleGenerativeAI`          | `gemini-3-flash-preview` | LLM used for answers       |

## ⚠️ Limitations

- The vector store is **in-memory**, so data is lost when the app restarts or the session ends.
- Only **one PDF per session** is supported.
- Scanned or image-only PDFs won't work without OCR.
- Each question is answered independently; previous chat turns are not passed to the model as context.
- Answer quality depends on retrieval, so very large or complex documents may need a higher `k` or different chunk settings.

## 🔮 Future Improvements

- [ ] Persistent vector store (Chroma, FAISS, or Pinecone)
- [ ] Support for multiple PDFs and other file types
- [ ] Conversational memory for follow-up questions
- [ ] Show source page numbers with each answer
- [ ] Option to upload a new document without restarting

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m "Add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgements

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Google Gemini](https://ai.google.dev/)
