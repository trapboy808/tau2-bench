"""OpenAI embedder using text-embedding models."""

import os
from typing import List

import numpy as np
from openai import OpenAI

from tau2.knowledge.embedders.base import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):
    """Embedder using OpenAI's embedding models."""

    def __init__(self, model: str = "text-embedding-ada-002", api_key: str = None):
        """
        Initialize OpenAI embedder.

        Args:
            model: OpenAI model name. Supported models include:
                   - text-embedding-ada-002 (default, 1536 dimensions)
                   - text-embedding-3-small (1536 dimensions)
                   - text-embedding-3-large (3072 dimensions)
            api_key: OpenAI API key (if None, will use OPENAI_API_KEY env var)
        """
        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def embed(self, texts: List[str], batch_size: int = 10) -> np.ndarray:
        """
        Embed texts using OpenAI API.

        Args:
            texts: List of text strings to embed
            batch_size: Maximum number of texts per API call (DashScope limits to 10)

        Returns:
            Array of embeddings with shape (len(texts), embedding_dim)
        """
        if not texts:
            raise ValueError("No text to embed.")

        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(input=batch, model=self.model)
            all_embeddings.extend([item.embedding for item in response.data])
        return np.array(all_embeddings)

    def get_name(self) -> str:
        """Return the name of the embedder."""
        return f"openai_{self.model}"
