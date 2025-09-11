# rag_build.py
import os
import json
import math
import numpy as np
import faiss
from pypdf import PdfReader
from huggingface_hub import InferenceClient

import dotenv
dotenv.load_dotenv()

HF_TOKEN = os.environ["HF_TOKEN"]
EMBED_MODEL = os.environ.get("EMBED_MODEL", "BAAI/bge-small-en-v1.5")  # 384-dim
PDF_PATH = os.environ.get("PDF_PATH", "docs/Ironlady_Knowledgebase.pdf")

# Index files
HEAD_IDX_PATH = r"index\faiss_headings.index"
PAGE_IDX_PATH = r"index\faiss_pages.index"
HEAD_META_PATH = r"index\metadata_headings.json"
PAGE_META_PATH = r"index\metadata_pages.json"

client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

def l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True) + 1e-12
    return x / norms

def embed_texts(texts, batch_size=16):
    # InferenceClient.feature_extraction supports list[str] inputs
    embs = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        vecs = client.feature_extraction(batch, model=EMBED_MODEL)
        arr = np.array(vecs, dtype=np.float32)
        embs.append(arr)
    embs = np.vstack(embs)
    embs = l2_normalize(embs)  # for cosine via inner product
    return embs

def extract_pages(pdf_path):
    reader = PdfReader(pdf_path)
    pages = []
    for i, p in enumerate(reader.pages):
        raw = (p.extract_text() or "").strip()
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
        heading = lines if lines else f"Page {i+1}"
        text = "\n".join(lines)
        pages.append({"page_no": i+1, "heading": heading, "text": text})
    return pages

def build_indexes(pages):
    headings = [p["heading"] for p in pages]
    page_texts = [p["text"] for p in pages]

    head_embs = embed_texts(headings)
    page_embs = embed_texts(page_texts)

    d = head_embs.shape[1]
    head_index = faiss.IndexFlatIP(d)
    head_index.add(head_embs)

    d2 = page_embs.shape[1]
    assert d == d2, "Heading and page embeddings must use the same model/dim"
    page_index = faiss.IndexFlatIP(d2)
    page_index.add(page_embs)

    faiss.write_index(head_index, HEAD_IDX_PATH)
    faiss.write_index(page_index, PAGE_IDX_PATH)

    with open(HEAD_META_PATH, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    with open(PAGE_META_PATH, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    pages = extract_pages(PDF_PATH)
    build_indexes(pages)
    print(f"Built indexes for {len(pages)} pages")
