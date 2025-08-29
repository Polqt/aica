from ...core.config import settings
from .vector_store import vector_store as pgvector_store


def get_vector_store():
    backend = (settings.VECTOR_BACKEND or "pgvector").lower()
    if backend == "pgvector":
        return pgvector_store
    raise NotImplementedError(f"Vector backend '{backend}' is not implemented.")


