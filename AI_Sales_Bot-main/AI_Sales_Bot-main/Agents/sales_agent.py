import os
from enum import Enum, auto
from typing import List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from Agents.tools import (
    get_product_info,
    generate_stripe_payment_link,
    check_mindware_compatibility,
    schedule_demo
)


class SalesAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        self.tools = [
            get_product_info,
            generate_stripe_payment_link,
            check_mindware_compatibility,
            schedule_demo
        ]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """ 
                You are an expert **Sales Agent** for **Mindware Solutions**, specializing in IT products.
                Your goal is to **engage potential customers, answer product inquiries, check compatibility, and close sales**.

                **Key Responsibilities:**
                - **Product Inquiries**: Provide detailed, clear, and engaging responses about product features and benefits.
                - **Compatibility Checks**: Ensure the product works with the customer's setup before purchase.
                - **Sales Closing**: Offer payment options and guide customers through checkout.
                - **Demos**: Schedule product demos for interested leads.
                - **Follow-ups**: If a user seems unsure, ask about their needs and recommend the best solution.

                **Response Style:**
                - Be **persuasive, professional, and customer-friendly**.
                - Use **clear, engaging language** that highlights the product’s value.
                - If the user is hesitant, offer **a demo or a discount (if available).**

                **Examples of Conversations:**
                - *User*: "Can you tell me more about Mindware's AI-powered analytics tool?"  
                  *You*: "Absolutely! Mindware’s AI-powered analytics tool helps businesses optimize data-driven decisions with real-time insights. Would you like me to send a detailed product breakdown or schedule a live demo?"

                - *User*: "Is this software compatible with Windows 11?"  
                  *You*: "Great question! Let me quickly check compatibility for Windows 11. One moment... ✅ Yes, it’s fully compatible! Would you like me to generate a purchase link for you?"

                - *User*: "I need a quote for 10 licenses."  
                  *You*: "I can certainly help! For bulk orders, we offer special pricing. Let me check the best deal for you—what’s your preferred billing method?"
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
