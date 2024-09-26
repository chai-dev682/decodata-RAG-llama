import os
import glob
import nest_asyncio
from typing import List, Dict

from llama_parse import LlamaParse
from llama_index.core import Document

nest_asyncio.apply()

parser = LlamaParse(
    api_key=os.getenv("LLAMA_PARSE_API_KEY"),  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    num_workers=4,  # if multiple files passed, split in `num_workers` API calls
    verbose=True,
    language="en",  # Optionally you can define a language, default=en
)


def parse_pdf_directory(directory_path: str) -> List[Document]:
    """
    Parses all PDF documents in a directory using LlamaParse.

    Args:
        directory_path: Path to the directory containing PDF files.

    Returns:
        A list of parsed Document objects.
    """
    global parser
    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
    documents = parser.load_data(pdf_files)

    return documents


def parse_single_pdf(pdf_path: str) -> List[Document]:
    """
    Parses a single PDF document using LlamaParse.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list of parsed Document objects (usually representing pages).
    """
    global parser
    documents = parser.load_data(pdf_path)
    return documents


def parse_pdfs_with_subdirectory_metadata(directory_path: str) -> List[Document]:
    """
    Parses PDF documents from subdirectories, adding subdirectory name as metadata.

    Args:
        directory_path: Path to the main directory containing subdirectories with PDFs.

    Returns:
        A dictionary where keys are subdirectory names and values are lists of
        parsed Document objects with metadata.
    """
    parsed_documents = []

    for subdir_name in os.listdir(directory_path):
        subdir_path = os.path.join(directory_path, subdir_name)
        if os.path.isdir(subdir_path):
            # Use parse_pdf_directory if there are multiple PDFs in the subdirectory
            pdf_files = glob.glob(os.path.join(subdir_path, "*.pdf"))
            if len(pdf_files) > 1:
                documents = parse_pdf_directory(subdir_path)
            # Use parse_single_pdf if there's only one PDF in the subdirectory
            elif len(pdf_files) == 1:
                documents = parse_single_pdf(pdf_files[0])
            else:
                print(f"Warning: No PDF files found in subdirectory '{subdir_name}'")
                continue  # Skip to the next subdirectory

            # Add subdirectory name as metadata to each Document
            for doc in documents:
                doc.metadata = {"subdirectory": subdir_name}

            parsed_documents = parsed_documents + documents

    return parsed_documents
