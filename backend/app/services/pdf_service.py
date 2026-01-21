from typing import Dict, Any

from langchain_community.document_loaders import PyPDFLoader


def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    full_text = "\n".join(page.page_content for page in pages)

    return {
        "title": "Uploaded PDF",
        "url": None,
        "sections": {
            "Content": full_text,
        },
    }
