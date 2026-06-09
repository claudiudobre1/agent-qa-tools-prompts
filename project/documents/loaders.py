from pathlib import Path

from project.documents.models import Document, make_document_id


SUPPORTED_EXTENSIONS = {".txt"}


def load_text_file(path: str | Path) -> Document:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension: {extension}. "
            f"Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    text = path.read_text(encoding="utf-8")

    return Document(
        id=make_document_id(path),
        source_path=str(path),
        filename=path.name,
        extension=extension,
        text=text,
    )