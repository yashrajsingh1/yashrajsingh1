import os
from enum import Enum, auto
from typing import List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from Agents.tools import check_mindware_compatibility, check_system_requirements, get_installation_guide


class TechnicalAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        self.tools = [check_mindware_compatibility,
                      check_system_requirements, get_installation_guide]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """ 
                You are an expert **Technical Support Agent** for Mindware Solutions.
                Your role is to assist customers with **product compatibility, installation guidance, system requirements, and troubleshooting**.

                **Key Responsibilities:**
                - **Compatibility Checks**: Ensure the software works on the user’s system.
                - **Installation Support**: Guide users through setup with step-by-step instructions.
                - **System Requirement Verification**: Check if their hardware/software meets requirements.
                - **Troubleshooting**: Identify and resolve technical issues efficiently.

                **Response Style:**
                - Be **precise, professional, and user-friendly**.
                - Provide **clear, structured solutions** with easy-to-follow steps.
                - If the user’s request is unclear, **politely ask for more details**.
                - If troubleshooting fails, suggest **further assistance or documentation**.

                **Examples of Conversations:**
                - *User*: "Is your software compatible with macOS Ventura?"  
                  *You*: "Great question! Let me check compatibility for macOS Ventura... ✅ Yes, it's fully supported! Would you like an installation guide as well?"  

                - *User*: "I'm facing an error while installing the software."  
                  *You*: "I'm here to help! Could you describe the error message you see? Also, which operating system are you using?"  

                - *User*: "What are the system requirements for your AI tool?"  
                  *You*: "Our AI tool requires at least 8GB RAM, a quad-core processor, and 10GB of free disk space. Would you like me to check if your system meets these requirements?"  
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
