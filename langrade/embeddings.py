from typing import List, Union
import vertexai
from vertexai.language_models import TextEmbeddingModel
from google.oauth2 import service_account
import json


class VertexAIEmbeddings:
    def __init__(
        self, credentials: Union[str, dict], model_name: str = "multilingual-e5-large"
    ):
        if isinstance(credentials, str):
            try:
                with open(credentials) as f:
                    credentials_dict = json.load(f)
            except Exception as e:
                raise ValueError(f"Failed to load credentials file: {str(e)}")
        else:
            credentials_dict = credentials

        project_id = credentials_dict.get("project_id")
        location = credentials_dict.get("location", "asia-northeast1")

        if not project_id:
            raise ValueError("project_id is required in credentials")

        credentials_object = service_account.Credentials.from_service_account_info(
            credentials_dict
        )

        vertexai.init(
            project=project_id, location=location, credentials=credentials_object
        )

        self.model = TextEmbeddingModel.from_pretrained(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            embedding = self.model.get_embeddings([text])[0]
            embeddings.append(embedding.values)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        embedding = self.model.get_embeddings([text])[0]
        return embedding.values
