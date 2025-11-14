# Barber RAG Agent with LangSmith

Agent-based barber shop assistant with LangSmith observability.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```
OPENAI_API_KEY=your_key_here
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=barber-rag-agent
```

3. Initialize database:
```bash
python setup_db.py
```

4. Run Streamlit app:
```bash
streamlit run app.py
```

## Architecture

- `agent.py`: Agent with tools (services, business_info, appointments)
- `app.py`: Streamlit chat interface
- `setup_db.py`: Database initialization
- LangSmith: Tracks all agent/tool calls with full observability




## Tools

- `get_services`: Fetches barber services
- `get_business_info`: Fetches business details
- `get_appointments`: Queries SQLite appointments

<img width="844" height="344" alt="image" src="https://github.com/user-attachments/assets/693ee936-a12d-4fef-970c-36c551f85806" />

