import sqlite3
import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "barber-rag-agent"

llm = ChatOpenAI(model="gpt-5-chat-latest", temperature=0.5)

@tool
def get_services() -> str:
    """Fetch barber services from file."""
    try:
        with open("barber_services.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Services information not available."

@tool
def get_business_info() -> str:
    """Fetch business information from file."""
    try:
        with open("barber_business_info.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Business information not available."

@tool
def get_appointments() -> str:
    """Query appointments from database."""
    try:
        conn = sqlite3.connect('barber_appointments.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, customer_name, phone_number, appointment_date, appointment_time,
                   service_type, barber_name, duration_minutes, price, status, notes
            FROM appointments
            ORDER BY appointment_date, appointment_time
        ''')
        appointments = cursor.fetchall()
        conn.close()
        
        if not appointments:
            return "No appointments found."
        
        context = "Current Appointments:\n\n"
        for apt in appointments:
            context += f"ID: {apt[0]}\n"
            context += f"Customer: {apt[1]}\n"
            context += f"Phone: {apt[2]}\n"
            context += f"Date: {apt[3]}\n"
            context += f"Time: {apt[4]}\n"
            context += f"Service: {apt[5]}\n"
            context += f"Barber: {apt[6]}\n"
            context += f"Duration: {apt[7]} minutes\n"
            context += f"Price: ${apt[8]}\n"
            context += f"Status: {apt[9]}\n"
            if apt[10]:
                context += f"Notes: {apt[10]}\n"
            context += "\n"
        return context
    except Exception as e:
        return f"Error fetching appointments: {str(e)}"

tools = [get_services, get_business_info, get_appointments]

system_prompt = """You are a barber assistant. Answer user questions by using the appropriate tools.

If user asks about:
- Services, prices, or hair treatments: use get_services tool
- Business hours, location, contact info: use get_business_info tool
- Appointments, scheduling: use get_appointments tool

Analyze user intent and call the right tool. Answer based on fetched context."""

agent = create_react_agent(llm, tools, prompt=system_prompt)

def chat(user_input: str, chat_history: list = None) -> dict:
    """Process user input through agent."""
    if chat_history is None:
        chat_history = []
    
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    
    return {
        "response": result["messages"][-1].content if result["messages"] else "",
        "chat_history": chat_history
    }
