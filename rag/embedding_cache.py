import os
from functools import lru_cache
from langchain_community.embeddings import OpenAIEmbeddings

@lru_cache(maxsize=None)
def get_cached_embedding():
    return OpenAIEmbeddings()
