import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub

load_dotenv()
llm_name = 'gpt-4o'
embeddings_name = 'text-embedding-ada-002'

# Initialize the components that will be used from LangChain's suite of integrations
llm = AzureChatOpenAI(azure_deployment=llm_name)
embeddings = AzureOpenAIEmbeddings(azure_deployment=embeddings_name)
vector_store = InMemoryVectorStore(embeddings)

# Load the dataset to begin the indexing process:
loader = CSVLoader(file_path='./app_hotel_reviews.csv',
    csv_args={
    'delimiter': ',',
    'fieldnames': ['Hotel Name', 'User Review']
})
docs = loader.load()

# Split the documents into chunks for embedding and vector storage
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    add_start_index=True,
)
all_splits = text_splitter.split_documents(docs)

print(f"Split documents into {len(all_splits)} sub-documents.")

# Embed the contents of each text chunk and insert these embeddings into a vector store
document_ids = vector_store.add_documents(documents=all_splits)

# Test the RAG application
prompt_template = hub.pull("rlm/rag-prompt")

print("Enter 'exit' or 'quit' to close the program.")

history = []

# Loop to handle multiple questions from the user
while True:
    question = input("\nPlease enter your question: ")
    if question.lower() in ['exit', 'quit']:
        break

    # Retrieve relevant documents from the vector store based on user input
    retrieved_docs = vector_store.similarity_search(question, k=10)
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Format the conversation history as a string
    history_text = ""
    if history:
        history_lines = []
        for record in history:
            history_lines.append(f"Q: {record['question']}\nA: {record['answer']}")
        history_text = "\n\n".join(history_lines)

    # Generate the prompt with the latest question, retrieved context, and conversation history
    prompt = prompt_template.invoke({
        "question": question,
        "context": docs_content,
        "history": history_text
    })
    answer = llm.invoke(prompt)

    # Print the answer
    print("\nAnswer:")
    print(answer.content) 

    # Append the current exchange to the history
    history.append({
        "question": question,
        "answer": answer.content
    })
