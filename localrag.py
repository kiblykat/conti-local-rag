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

# Quality control settings
SETTINGS = {
    # Context retrieval settings
    'context': {
        'top_k': 8,                    # Number of relevant chunks to retrieve
        'embedding_model': 'mxbai-embed-large',  # Model for embeddings
    },
    
    # Generation settings
    'generation': {
        'max_tokens': 1000,             # Maximum length of response
        'temperature': 0.3,            # Randomness (0.0-1.0)
        'top_p': 0.8,                 # Nucleus sampling threshold
        'presence_penalty': 0.0,       # Topic diversity
        'frequency_penalty': 0.3,      # Word diversity
    },
    
    # System prompt settings
    'system_prompt': """You are a helpful assistant that is an expert at answering job application questions.
    Please provide clear, professional responses that:
    - Are concise and direct
    - Use professional language
    - Focus on concrete examples and achievements
    - Avoid filler words and redundancy
    - Stay within 2-3 paragraphs unless specifically asked for more detail
    """
}

def colored_print(text, color):
    print(f"{COLORS[color]}{text}{COLORS['reset']}")

def get_relevant_context(query, embeddings, content):
    if embeddings.nelement() == 0:
        return []
        
    query_embedding = ollama.embeddings(
        model=SETTINGS['context']['embedding_model'], 
        prompt=query
    )["embedding"]
    
    cos_scores = torch.cosine_similarity(torch.tensor(query_embedding).unsqueeze(0), embeddings)
    top_k = min(SETTINGS['context']['top_k'], len(cos_scores))
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
            {"role": "system", "content": SETTINGS['system_prompt']},
            *history
        ],
        max_tokens=SETTINGS['generation']['max_tokens'],
        temperature=SETTINGS['generation']['temperature'],
        top_p=SETTINGS['generation']['top_p'],
        presence_penalty=SETTINGS['generation']['presence_penalty'],
        frequency_penalty=SETTINGS['generation']['frequency_penalty']
    )
    
    history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

def load_vault():
    try:
        with open("vault.txt", "r", encoding='utf-8') as f:
            content = f.readlines()
        embeddings = torch.tensor([
            ollama.embeddings(
                model=SETTINGS['context']['embedding_model'], 
                prompt=text
            )["embedding"]
            for text in content
        ])
        return content, embeddings
    except FileNotFoundError:
        colored_print("No vault.txt found. Running without document context.", 'yellow')
        return [], torch.tensor([])

def main():
    parser = argparse.ArgumentParser(description="Enhanced Local Chat Application")
    parser.add_argument("--model", default="deepseek-r1:8b")
    parser.add_argument("--temperature", type=float, help="Override default temperature")
    parser.add_argument("--max_tokens", type=int, help="Override default max tokens")
    args = parser.parse_args()

    # Override settings with command line arguments if provided
    if args.temperature is not None:
        SETTINGS['generation']['temperature'] = args.temperature
    if args.max_tokens is not None:
        SETTINGS['generation']['max_tokens'] = args.max_tokens

    client = OpenAI(base_url='http://localhost:11434/v1', api_key=args.model)
    vault_content, vault_embeddings = load_vault()
    
    # Print current settings
    colored_print("\nCurrent Quality Settings:", 'green')
    for category, settings in SETTINGS.items():
        if category != 'system_prompt':
            colored_print(f"\n{category.title()}:", 'yellow')
            for param, value in settings.items():
                print(f"  {param}: {value}")

    history = []
    colored_print("\nChat initialized. Type 'quit' to exit.", 'green')
    
    while True:
        query = input(f"{COLORS['yellow']}Query: {COLORS['reset']}")
        if query.lower() == 'quit':
            break
            
        context = get_relevant_context(query, vault_embeddings, vault_content)
        response = chat(query, context, history, client, args.model)
        colored_print(f"Response:\n{response}", 'green')

if __name__ == "__main__":
    main()