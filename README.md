# local-rag

1. Ensure ollama is downloaded on system
2. Ensure necessary dependencies are pulled

- LLM: "ollama pull mistral:latest"
- Embedding model:"ollama pull mxbai-embed-large:latest"

3. Start by running "python upload.py"
4. Choose the pdf you want to upload
5. After embeddings are created, run "python local-rag.py"
6. If all dependencies are correctly downloaded, a CLI should start up where you can ask your questions.
7. Otherwise, read the error log and download missing deps.
8. If new context is required, please clear vault.txt and upload the new files

---

scrapeEmails.py scrapes through a folder filled with .msg files, add it to the vault, then answers questions based retrieved context

Reference is taken from this repository: https://github.com/AllAboutAI-YT/easy-local-rag/tree/main
