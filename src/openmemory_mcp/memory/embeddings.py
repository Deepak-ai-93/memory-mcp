import hashlib
import math
from abc import ABC, abstractmethod

from openmemory_mcp.config import Settings


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Return an embedding vector for text."""


class HashEmbeddingProvider(EmbeddingProvider):
    """Offline deterministic embedding fallback.

    This is intentionally simple but useful for local installs and tests. Provider classes below can
    replace it without changing repositories or MCP tools.
    """

    def __init__(self, dimensions: int = 128) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = [token for token in text.lower().split() if token]
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model: str) -> None:
        from openai import OpenAI

        self.client = OpenAI()
        self.model = model

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(model=self.model, input=text)
        return list(response.data[0].embedding)


class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model: str) -> None:
        from google import genai

        self.client = genai.Client()
        self.model = model

    def embed(self, text: str) -> list[float]:
        response = self.client.models.embed_content(model=self.model, contents=text)
        return list(response.embeddings[0].values)


class SentenceTransformersEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model: str) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model)

    def embed(self, text: str) -> list[float]:
        return [float(value) for value in self.model.encode(text, normalize_embeddings=True)]


def build_embedding_provider(settings: Settings) -> EmbeddingProvider:
    if settings.embedding_provider == "openai":
        return OpenAIEmbeddingProvider(settings.embedding_model)
    if settings.embedding_provider == "gemini":
        return GeminiEmbeddingProvider(settings.embedding_model)
    if settings.embedding_provider == "sentence_transformers":
        return SentenceTransformersEmbeddingProvider(settings.embedding_model)
    return HashEmbeddingProvider()
