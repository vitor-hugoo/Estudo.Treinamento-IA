import os
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core import settings
from oraculo.models import Treinamento
from oraculo.utils import gerar_documentos
from langchain_community.vectorstores import FAISS


def task_treinar_ia(instance_id):
    instance = Treinamento.objects.get(id=instance_id)
    documentos = gerar_documentos(instance)
    if not documentos:
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documentos)

    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

    db_path = settings.BASE_DIR / "banco_faiss"
    if os.path.exists(db_path):
        vectordb = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
        vectordb.add_documents(chunks)
    else:
        vectordb = FAISS.from_documents(chunks, embeddings)
        vectordb.save_local(db_path)
