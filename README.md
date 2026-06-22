# Personal AI Assistant for Tech News and GitHub

This example demonstrates a zero-dependency personal AI assistant that aggregates tech news from Hacker News RSS and trending repositories from the GitHub API. It then leverages an LLM (OpenAI-compatible API) to filter, curate, and summarize the content into a personalized Turkish daily digest based on user-defined interests, falling back to basic keyword filtering if no API key is provided.

## Language

`python`

## How to Run

To run with AI summarization: export OPENAI_API_KEY='your_key' (optional: export OPENAI_API_BASE='custom_endpoint' and LLM_MODEL='model_name') and execute: python assistant.py

## Original Article

This example accompanies the Turkish article: [Kişisel Yapay Zeka Asistanı ile GitHub ve Haber Akışı Yönetimi](https://fatihsoysal.com/blog/kisisel-yapay-zeka-asistani-ile-github-ve-haber-akisi-yonetimi/).

## License

MIT — see [LICENSE](LICENSE).
