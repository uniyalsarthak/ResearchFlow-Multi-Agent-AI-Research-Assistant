# ResearchFlow — Multi-Agent AI Research Assistant

ResearchFlow takes any topic and produces a complete, reviewed research report using a pipeline of AI agents that search, read, write, and critique, all working together instead of relying on a single AI response.

## How It Works

1. **Search Agent** — searches the web for recent, reliable information on the topic
2. **Reader Agent** — scrapes and extracts deeper content from the most relevant source
3. **Writer Chain** — drafts a structured report from the gathered research
4. **Critic Chain** — reviews and scores the report for quality before it's shown to the user

## Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **Agent Orchestration:** LangChain, LangGraph
- **LLM Inference:** Groq API
- **Web Search:** Tavily API
- **Web Scraping:** BeautifulSoup

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/uniyalsarthak/ResearchFlow-Multi-Agent-AI-Research-Assistant.git
cd ResearchFlow-Multi-Agent-AI-Research-Assistant
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
Create a `.env` file in the project root:

GROQ_API_KEY=your_groq_api_key_here

TAVILY_API_KEY=your_tavily_api_key_here


### 5. Run the app
```bash
streamlit run app.py
```



