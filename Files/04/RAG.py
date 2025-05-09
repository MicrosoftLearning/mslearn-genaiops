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

# Loop to handle multiple questions from the user
while True:
    question = input("\nPlease enter your question: ")
    if question.lower() in ['exit', 'quit']:
        break

    # Retrieve relevant documents from the vector store based on user input
    retrieved_docs = vector_store.similarity_search(question)
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Generate the prompt and obtain the answer from the language model
    prompt = prompt_template.invoke({"question": question, "context": docs_content})
    answer = llm.invoke(prompt)

    # Print the answer
    print("\nAnswer:")
    print(answer.content) 

