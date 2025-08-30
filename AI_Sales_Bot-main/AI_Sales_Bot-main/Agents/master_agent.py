from enum import Enum
from langchain_openai import ChatOpenAI
from Agents.sales_agent import SalesAgent
from Agents.support_agent import SupportAgent
from Agents.technical_agent import TechnicalAgent
from Agents.billing_agent import BillingAgent


class MasterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.agents = {
            "sales": SalesAgent(),
            "support": SupportAgent(),
            "technical": TechnicalAgent(),
            "billing": BillingAgent()
        }
        self.current_agent = "sales"

    def classify_intent(self, user_input: str) -> str:
        prompt = f"""
        You are an AI assistant that classifies user queries into one of the following categories: 
        
        - **sales**: Questions about pricing, product features, demos, discounts, or purchasing options.
        - **support**: Issues related to product returns, troubleshooting, customer feedback, or general assistance.
        - **technical**: Questions about compatibility, installation, software/hardware requirements, or configuration.
        - **billing**: Queries about payments, refunds, invoices, subscriptions, or transaction issues.
        
        **Examples:**
        1. "How much does the premium plan cost?" → **sales**
        2. "My product stopped working, what should I do?" → **support**
        3. "Does this software work on macOS?" → **technical**
        4. "I was charged twice for my order!" → **billing**
        
        **User Message:** "{user_input}"  
        **Category (one word response only):**
        """
        response = self.llm.invoke(prompt).content.strip().lower()

        if response not in self.agents:
            response = "sales"

        return response

    def process_input(self, user_input: str) -> str:
        new_agent = self.classify_intent(user_input)
        self.current_agent = new_agent
        return self.agents[self.current_agent].process_input(user_input)
