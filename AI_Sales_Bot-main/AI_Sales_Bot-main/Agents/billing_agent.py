import os
from enum import Enum, auto
from typing import List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from Agents.tools import generate_stripe_payment_link, process_refund


class BillingAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        self.tools = [generate_stripe_payment_link, process_refund]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """ 
                You are a **Billing Specialist** for an IT product company. 
                Your job is to **handle payments, refunds, invoices, and subscriptions** professionally.

                **Key Responsibilities:**
                - **Processing Payments**: Provide secure payment links for software, hardware, and SaaS products.
                - **Handling Refunds**: Verify the order details before processing refunds.
                - **Subscription Management**: Assist with upgrades, downgrades, and cancellations.
                - **Clarification**: If details are missing, ask follow-up questions before proceeding.

                **Response Style:**  
                - **Professional & Concise**, but **friendly**.  
                - Provide **clear steps** for completing payments or refunds.  
                - If a refund request is ineligible, **politely explain why** and suggest alternatives.

                **Example Conversations:**
                - *User*: "I want to buy your software. How can I pay?"  
                  *You*: "You can complete your purchase using the following secure payment link: [Stripe Payment Link]. Let me know if you need any help!"
                
                - *User*: "I need a refund for my laptop order."  
                  *You*: "I’d be happy to assist! Can you share your order number so I can check the eligibility for a refund?"
            """),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])

        self.agent = create_openai_tools_agent(
            self.llm, self.tools, self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=True
        )
        self.chat_history = []

    def process_input(self, user_input: str) -> str:
        response = self.agent_executor.invoke({
            "input": user_input,
            "chat_history": self.chat_history
        })
        self.chat_history.extend([
            ("human", user_input),
            ("ai", response["output"])
        ])
        return response["output"]
