import torch
import ollama
from openai import OpenAI
import argparse

COLORS = {
    'pink': '\033[95m',
    'cyan': '\033[96m',
    'yellow': '\033[93m',
    'green': '\033[92m',
    'reset': '\033[0m'
}

def colored_print(text, color):
    print(f"{COLORS[color]}{text}{COLORS['reset']}")

def get_relevant_context(query, embeddings, content, top_k=6):
    if embeddings.nelement() == 0:
        return []
        
    query_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=query)["embedding"]
    cos_scores = torch.cosine_similarity(torch.tensor(query_embedding).unsqueeze(0), embeddings)
    top_k = min(top_k, len(cos_scores))
    relevant_content = [content[i].strip() for i in torch.topk(cos_scores, k=top_k)[1].tolist()]
    
    return relevant_content

def chat(query, context, history, client, model):
    if context:
        context_str = "\n".join(context)
        colored_print(f"Context:\n{context_str}", 'cyan')
        query += f"\n\nRelevant Context:\n{context_str}"
        
    history.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that is an expert at answering job application questions. Keep answers concise and direct."},
            *history
        ],
        max_tokens=500,
    )
    
    history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Local Chat Application")
    parser.add_argument("--model", default="deepseek-r1:8b")
    args = parser.parse_args()

    client = OpenAI(base_url='http://localhost:11434/v1', api_key=args.model)
    
    # Load and embed vault content
    try:
        with open("vault.txt", "r", encoding='utf-8') as f:
            vault_content = f.readlines()
        vault_embeddings = torch.tensor([
            ollama.embeddings(model='mxbai-embed-large', prompt=content)["embedding"]
            for content in vault_content
        ])
    except FileNotFoundError:
        vault_content = []
        vault_embeddings = torch.tensor([])
        colored_print("No vault.txt found. Running without document context.", 'yellow')

    history = []
    colored_print("Chat initialized. Type 'quit' to exit.", 'green')
    
    while True:
        query = input(f"{COLORS['yellow']}Query: {COLORS['reset']}")
        if query.lower() == 'quit':
            break
            
        context = get_relevant_context(query, vault_embeddings, vault_content)
        response = chat(query, context, history, client, args.model)
        colored_print(f"Response:\n{response}", 'green')

if __name__ == "__main__":
    main()