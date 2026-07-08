import asyncio

from langchain_ollama import ChatOllama

from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import HumanMessage

from langchain_core.globals import set_debug

from services.mcp_client_manager import MCPClientManager

from security import detect_prompt_injection
from prompts import system_prompt

import config


set_debug(True)


llm = ChatOllama(
    model=config.OLLAMA_MODEL,
    temperature=0.1,
    base_url=config.OLLAMA_URL
)


memory = MemorySaver()



async def run_agent():

    # ---------------------------------
    # Connect to MCP Server
    # ---------------------------------

    mcp_manager = MCPClientManager(
        config.MCP_SERVERS
    )


    tools = await mcp_manager.connect()


    # ---------------------------------
    # Create Agent
    # ---------------------------------

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=memory,
    )


    print("\n========================================================")
    print("Bank Infrastructure Agent Ready (MCP Enabled)")
    print("Type 'exit' or 'quit' to end the session.")
    print("========================================================\n")


    session_id = "bank_dev_session_1"


    while True:

        try:

            user_input = input(
                "You: "
            ).strip()


            if user_input.lower() in [
                "exit",
                "quit"
            ]:
                print(
                    "\nEnding session. Goodbye!"
                )
                break


            if not user_input:
                continue


            # -------------------------
            # Prompt Injection Detection
            # -------------------------

            if detect_prompt_injection(
                user_input
            ):

                print(
                    "\n=== Agent Response ==="
                )

                print(
                    "Your request appears to contain "
                    "instructions that attempt to override "
                    "the assistant's operating rules. "
                    "Please ask a question related to bank "
                    "infrastructure, GCP, or internal bank policy."
                )

                print(
                    "======================\n"
                )

                continue



            print(
                "\n--- Processing Request ---"
            )


            response = await agent.ainvoke(
                {
                    "messages": [
                        HumanMessage(
                            content=user_input
                        )
                    ]
                },
                config={
                    "configurable": {
                        "thread_id": session_id
                    }
                },
            )


            print(
                "\n=== Agent Response ==="
            )

            print(
                response["messages"][-1].content
            )

            print(
                "======================\n"
            )


        except KeyboardInterrupt:

            print(
                "\nSession interrupted. Goodbye!"
            )

            break
        
        finally:

            await mcp_manager.close()



if __name__ == "__main__":

    asyncio.run(
        run_agent()
    )