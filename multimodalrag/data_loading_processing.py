from unstructured.partition.pdf import partition_pdf

def get_images_base64(chunks):
    images_b64 = []
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            chunk_els = chunk.metadata.orig_elements
            for el in chunk_els:
                if "Image" in str(type(el)):
                    images_b64.append(el.metadata.image_base64)
    return images_b64

def get_tables_html(chunks):
    tables_html = []
    for chunk in chunks:
        chunk_els = chunk.metadata.orig_elements
        for el in chunk_els:
            if "Table" in str(type(el)):    
                tables_html.append(el.metadata.text_as_html)
    return tables_html

def get_text_data(texts):
    actual_texts = []
    for ele in texts:
        combined_elements = ele.metadata.orig_elements
        for particular_element in combined_elements:
            if "Text" in str(type(particular_element)):
                actual_texts.append(particular_element.text)
    return actual_texts

def load_document(pdf_path):
    elements = partition_pdf(
        filename=pdf_path,
        infer_table_structure=True,
        strategy="hi_res",
        extract_image_block_types=["Image", "Table"],
        extract_image_block_to_payload=True,
        chunking_strategy="by_title",
        max_characters=4000,
        combine_text_under_n_chars=2000,
        new_after_n_chars=3800,
    )

    texts = []

    for element in elements:
        texts.append(element)

    images_data = get_images_base64(elements)
    tables_data = get_tables_html(elements)
    texts_data = get_text_data(texts)
    
    return texts_data, tables_data, images_data