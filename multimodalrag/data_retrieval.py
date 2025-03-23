import io, base64
import re

from IPython.display import HTML, display
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from PIL import Image

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from multimodalrag.config import openai_key

def plt_img_base64(img_base64):
    image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />' # create a html tag to display the image by taking the base 64 encoded image as input
    display(HTML(image_html))

# sanity check to see if the data encoded is in base 64 format or not
def check_if_base64(sb):
    return re.match("^[A-Za-z0-9+/]+[=]{0,2}$", sb) is not None

# this function is used to check the first 8 bytes of data and determine if the base64 data is an image or not
def is_it_image(b64data):
    image_signatures = {
        b"\xff\xd8\xff": "jpg",
        b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a": "png",
        b"\x47\x49\x46\x38": "gif",
        b"\x52\x49\x46\x46": "webp",
    }
    try:
        header = base64.b64decode(b64data)[:8]
        for sig, format in image_signatures.items():
            if header.startswith(sig):
                return True
        return False
    except Exception:
        return False
    
def resize_base64_image(base64_string, size=(128, 128)):
    img_data = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_data))
    resized_img = img.resize(size, Image.LANCZOS)
    buffered = io.BytesIO() # Saving the resized image to a bytes buffer
    resized_img.save(buffered, format=img.format)

    # Encoding the image to Base64 again
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def parse_retrieved_docs(parsed_documents):
    b64_images = []
    texts = []
    for doc in parsed_documents:
        if isinstance(doc, Document):
            doc = doc.page_content
        if check_if_base64(doc) and is_it_image(doc):
            doc = resize_base64_image(doc, size=(1300, 600))
            b64_images.append(doc)
        else:
            texts.append(doc)
    return {"images": b64_images, "texts": texts}

def custom_prompt(input_data):
    content_text_combined = "\n".join(input_data["context"]["texts"])
    messages = [] # will store image data if it's being retrieved from the docs

    if input_data["context"]["images"]:
        for image in input_data["context"]["images"]:
            image_text_data = {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image}"},
            }
            messages.append(image_text_data)
    
    prompt_template = f"""
        Answer the question based only on the following context, which can include text, tables, and the below image.
        Context: {content_text_combined}
        Question: {input_data["question"]}
    """

    text_message = {
        "type": "text",
        "text": (
            prompt_template
        ),
    }

    messages.append(text_message)
    return [HumanMessage(content=messages)]

def rag_chain_for_multi_modal(retriever):
    chain = (
        {
            "context": retriever | RunnableLambda(parse_retrieved_docs),
            "question": RunnablePassthrough(),
        }
        | RunnableLambda(custom_prompt)
        | ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)
        | StrOutputParser()
    )

    return chain

def rag_chain_for_multi_modal_with_sources(retriever):
    chain_with_sources = {
            "context": retriever | RunnableLambda(parse_retrieved_docs),
            "question": RunnablePassthrough(),
        } | RunnablePassthrough().assign(
            response = (RunnableLambda(custom_prompt)
            | ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)
            | StrOutputParser()
        )
    )

    return chain_with_sources