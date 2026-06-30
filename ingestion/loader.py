from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)

from config import DATA_DIR

SUPPORTED_EXTENSIONS = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
}


def load_documents(data_dir: str = DATA_DIR) -> list[Document]:

    documents = []

    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"{data_dir} does not exist.")

    for file in data_path.rglob("*"):

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            print(f"Skipping {file.name}")
            continue

        try:

            loader = SUPPORTED_EXTENSIONS[extension](str(file))

            docs = loader.load()

            for doc in docs:
                doc.metadata["filename"] = file.name
                doc.metadata["extension"] = extension
                doc.metadata["source_path"] = str(file.resolve())

            documents.extend(docs)

            print(f"Loaded {file.name}")

        except Exception as e:
            print(f"Error loading {file.name}")
            print(e)

    print(f"\nTotal documents loaded : {len(documents)}")

    return documents