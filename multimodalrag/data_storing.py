import uuid
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

def create_multi_vector_retriever(
    vectorstore, text_summaries, texts, table_summaries, tables, image_summaries, images   
):
    store = InMemoryStore()
    id_key = "doc_id"

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key
    )

    def add_docs(retriever, summaries, original_content):
        doc_ids = [str(uuid.uuid4()) for _ in original_content]
        summary_documents = [
            Document(page_content=s, metadata={id_key: doc_ids[i]})
            for i, s in enumerate(summaries)
        ]

        retriever.vectorstore.add_documents(summary_documents)
        retriever.docstore.mset(list(zip(doc_ids, original_content)))
    
    if text_summaries:
        add_docs(retriever, text_summaries, texts)
    if table_summaries:
        add_docs(retriever, table_summaries, tables)
    if image_summaries:
        add_docs(retriever, image_summaries, images)
    
    return retriever

def create_multimodal_retriever(text_summaries, texts, table_summaries, tables, image_summaries, images):
    vectorstore = Chroma(
        collection_name="multimodalvectorstore", embedding_function=OpenAIEmbeddings()
    )

    multimodal_retriever = create_multi_vector_retriever(
        vectorstore,
        text_summaries,
        texts,
        table_summaries,
        tables,
        image_summaries,
        images
    )

    return multimodal_retriever