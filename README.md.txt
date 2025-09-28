# MUN Debater 🗣️

A Streamlit-based AI-powered Model United Nations (MUN) debater.  
This app allows users to input a debate topic and get AI-generated responses as if debating in a real MUN setting.  
Designed for hackathons and student demos.

---

## 🚀 Features
- Simple, clean **Streamlit interface**
- Textbox to input debate topic
- "Generate Response" button
- Chat-like area to show AI responses
- Brand color scheme: **Purple, Black, Yellow**
- Works with OpenAI API (or mock responses for demo without a paid API)

---

🔑 Environment Variables

This project uses environment variables to keep your API key secure.
You need to create a .env file in the project root folder.

Example .env file
OPENAI_API_KEY=your_api_key_here


OPENAI_API_KEY: Your OpenAI API key (required if you want real AI responses).

If you don’t have a key, the app can still run in mock mode, returning sample pre-written responses.
