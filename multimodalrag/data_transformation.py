from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def summarize_tables(tables):
    prompt_text = """
    You are an assistant tasked with summarizing tables.
    Give a summary of the table and start by giving it an appropriate concise tile.

    Do not start your message by saying "Here is a summary" or anything like that.
    Just give the summary with the title as it is.

    Table chunk: {element}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    model = ChatGroq(temperature=0.5, model="llama-3.1-8b-instant")

    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    table_summaries = summarize_chain.batch(tables, {"max_concurrency": 3})

    return table_summaries

def summarize_images(images):
    prompt_template = """Describe the image in detail. Start with giving it an appropriate caption. The image can contain 
                        block diagrams, experiment analysis or plots. Just give a summary of the image starting with the caption."""
    messages = [
        (
            "user",
            [
                {"type": "text", "text": prompt_template},
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image}"},
                },
            ],
        )
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

    image_summaries = chain.batch(images)

    return image_summaries

def summarize_text(texts):
    prompt_text = """
    You are an assistant tasked with summarizing text data.
    Do not start your message by saying "Here is a summary" or anything like that.
    Just give the summary with the text as it is.

    Text chunk: {element}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    summarize_chain = {"element": lambda x: x} | prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 3})

    return text_summaries