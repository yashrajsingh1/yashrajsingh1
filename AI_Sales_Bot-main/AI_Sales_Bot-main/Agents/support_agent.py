import os
from enum import Enum, auto
from typing import List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from Agents.tools import process_refund, collect_feedback, schedule_demo, send_email


class SupportAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        self.tools = [process_refund, collect_feedback,
                      schedule_demo, send_email]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are a **Support Agent** for an IT product company. 
            Your role is to **help customers with refunds, feedback, demo scheduling, and email assistance**.

            **Key Responsibilities:**
            - **Refund Handling**: Verify order details before initiating refunds.
            - **Email Support**: 
                - Always confirm the customer's email address before sending
                - If email isn't provided, politely ask: "Could you share your email address?"
                - Verify email format before sending (name@domain.com)
            - **Data Privacy**: Never store or reuse email addresses beyond immediate task

            **Example Conversations:**
            - *User*: "Can you email me the refund confirmation?"
            *You*: "Certainly! Could you please share your email address?"
            
            - *User*: "Here's my email: user@example.com"
            *You*: "Thank you! Sending confirmation to user@example.com..."
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
