# rag_chat.py - Complete working version
import os
import json
import numpy as np
import faiss
from typing import List, Dict
from huggingface_hub import InferenceClient


import dotenv
dotenv.load_dotenv()

HF_TOKEN = os.environ["HF_TOKEN"]
EMBED_MODEL = os.environ.get("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
GEN_MODEL = os.environ.get("GEN_MODEL", "microsoft/DialoGPT-medium")  # Changed to a supported model

HEAD_IDX_PATH = r"index\faiss_headings.index"
PAGE_IDX_PATH = r"index\faiss_pages.index"
HEAD_META_PATH = r"index\metadata_headings.json"
PAGE_META_PATH = r"index\metadata_pages.json"

client = InferenceClient(token=HF_TOKEN)

def l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True) + 1e-12
    return x / norms

def embed_query(q: str) -> np.ndarray:
    v = client.feature_extraction(q, model=EMBED_MODEL)
    v = np.array(v, dtype=np.float32)[None, :]
    return l2_normalize(v)

class HeadingFirstRetriever:
    def __init__(self, k_head=3, k_pages=2):
        self.k_head = k_head
        self.k_pages = k_pages

        self.head_index = faiss.read_index(HEAD_IDX_PATH)
        self.page_index = faiss.read_index(PAGE_IDX_PATH)
        with open(HEAD_META_PATH, "r", encoding="utf-8") as f:
            self.head_meta = json.load(f)
        with open(PAGE_META_PATH, "r", encoding="utf-8") as f:
            self.page_meta = json.load(f)

        assert len(self.head_meta) == self.head_index.ntotal == self.page_index.ntotal

    def retrieve(self, query: str) -> List[Dict]:
        qv = embed_query(query)
        # Stage 1: headings
        sims_h, idxs_h = self.head_index.search(qv, self.k_head)  # (1, k_head)
        
        # Fix: Access first row since FAISS returns (1, k_head) shape
        candidate_pages = set(int(i) for i in idxs_h[0] if i >= 0)

        # Stage 2: re-rank candidate pages using page embeddings
        sims_p, idxs_p = self.page_index.search(qv, min(10, self.page_index.ntotal))
        page_rank = []
        for score, idx in zip(sims_p[0].tolist(), idxs_p[0].tolist()):
            if idx in candidate_pages:
                meta = self.page_meta[idx]
                page_rank.append({"idx": idx, "score": float(score), "meta": meta})
        page_rank.sort(key=lambda x: x["score"], reverse=True)
        return page_rank[: self.k_pages]


def build_prompt(contexts: List[Dict], question: str, mode: str) -> str:
    style = "concise and bullet-heavy" if mode == "compress" else "comprehensive and explanatory"
    instructions = f"""Based on the Iron Lady leadership programs context provided below, please answer the question in a {style} manner.

Question: {question}

Context from Iron Lady knowledge base:
"""
    for c in contexts:
        pg = c["meta"]["page_no"]
        hd = c["meta"]["heading"]
        tx = c["meta"]["text"]
        snippet = tx if len(tx) < 3000 else tx[:3000] + "..."
        instructions += f"\n[Page {pg}] {hd}\n{snippet}\n"
    
    instructions += f"\nAnswer ({mode} style):"
    return instructions

def generate_answer(question: str, mode: str = "compress") -> Dict:
    retriever = HeadingFirstRetriever()
    top = retriever.retrieve(question)
    prompt = build_prompt(top, question, mode)

    try:
        # Try multiple approaches in order of preference
        
        # Approach 1: Try chat_completion with Mistral (if available)
        if "mistral" in GEN_MODEL.lower():
            messages = [{"role": "user", "content": prompt}]
            response = client.chat_completion(
                messages=messages,
                model="mistralai/Mistral-7B-Instruct-v0.3",
                max_tokens=300 if mode == "elaborate" else 150,
                temperature=0.3,
                stream=False,
            )
            answer = response.choices.message.content
        
        # Approach 2: Use text_generation with reliable models
        else:
            # Try different models in order of preference
            models_to_try = [
                "microsoft/DialoGPT-medium",
                "gpt2",
                "facebook/blenderbot-400M-distill"
            ]
            
            answer = None
            for model in models_to_try:
                try:
                    response = client.text_generation(
                        prompt,
                        model=model,
                        max_new_tokens=200 if mode == "elaborate" else 100,
                        temperature=0.7,
                        do_sample=True,
                        return_full_text=False,
                        stream=False,
                    )
                    answer = response
                    break
                except Exception as model_error:
                    print(f"Model {model} failed: {model_error}")
                    continue
            
            if not answer:
                # Fallback to a simple template-based response
                answer = generate_fallback_answer(top, question, mode)
                
    except Exception as e:
        print(f"All generation methods failed: {e}")
        answer = generate_fallback_answer(top, question, mode)
    
    return {
        "question": question,
        "mode": mode,
        "contexts": [{"page_no": t["meta"]["page_no"], "heading": t["meta"]["heading"]} for t in top],
        "answer": answer,
    }

def generate_fallback_answer(contexts: List[Dict], question: str, mode: str) -> str:
    """Generate a simple template-based answer when LLM generation fails"""
    if not contexts:
        return "I couldn't find relevant information to answer your question."
    
    answer_parts = []
    if mode == "compress":
        answer_parts.append(f"Based on the Iron Lady knowledge base:")
        for ctx in contexts:
            pg = ctx["meta"]["page_no"]
            hd = ctx["meta"]["heading"]
            answer_parts.append(f"• [section 4 {pg}] {hd}")
    else:
        answer_parts.append(f"According to the Iron Lady documentation, here's what I found:")
        for ctx in contexts:
            pg = ctx["meta"]["page_no"]
            hd = ctx["meta"]["heading"]
            text_snippet = ctx["meta"]["text"][:500] + "..." if len(ctx["meta"]["text"]) > 500 else ctx["meta"]["text"]
            answer_parts.append(f"\nFrom section 4 {pg} ({hd}):\n{text_snippet}")
    
    return "\n".join(answer_parts)

if __name__ == "__main__":
    import json
    q = "What programs does Iron Lady offer?"
    result = generate_answer(q, mode="elaborate")
    print(json.dumps(result, ensure_ascii=False, indent=2))
