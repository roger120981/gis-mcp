"""
My First GIS Agent
A LangChain agent connected to the GIS MCP server via MultiServerMCPClient

Documentation: https://docs.langchain.com/oss/python/langchain/mcp
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables from .env file
load_dotenv()

# Step 1: Configure API key and MCP server
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MCP_SERVER_URL = "http://localhost:9010/mcp"  # HTTP transport, port 9010
MODEL_NAME = "deepseek/deepseek-chat-v3.1"  # Change to any OpenRouter model

async def main():
    # Check API key before proceeding
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY is not set.")
        print("Please ensure it's set in your .env file or environment variables.")
        print("Example .env file content:")
        print("  OPENROUTER_API_KEY=your_api_key_here")
        return

    # Step 2: Initialize language model (after env is loaded)
    llm = ChatOpenAI(
        model=MODEL_NAME,
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
    )

    # Step 3: Initialize MCP client
    print(f"🔌 Initializing MCP client...")
    print(f"   Server URL: {MCP_SERVER_URL}")
    print(f"   Transport: streamable_http")
    
    # Create the MCP client (this doesn't connect yet, it's lazy)
    client = MultiServerMCPClient(
        {
            "gis": {
                "transport": "streamable_http",
                "url": MCP_SERVER_URL,
            }
        }
    )
    print("   ✅ MCP client created successfully (no connection made yet)")
    
    # Step 4: Load available GIS tools from MCP server
    # This is where the actual connection happens
    print(f"\n📡 Attempting to connect and fetch tools from {MCP_SERVER_URL}...")
    try:
        tools = await client.get_tools()
        if not tools:
            print("⚠️  No tools found. Ensure the GIS MCP server is running on port 9010.")
            return
        print(f"✅ Successfully loaded {len(tools)} GIS tools!")
    except Exception as e:
        print("\n❌ Error: Failed to connect to GIS MCP server!")
        print(f"   Connection URL: {MCP_SERVER_URL}")
        print("\n📝 What happened:")
        print("   1. MCP client was created successfully")
        print("   2. Connection attempt failed when calling get_tools()")
        print("   3. This means the server is not running or not reachable")
        print("\n💡 Make sure the GIS MCP server is running:")
        print("   1. Open a NEW terminal window (keep this one open)")
        print("   2. Activate your virtual environment:")
        print("      .\\.venv\\Scripts\\Activate.ps1  (PowerShell)")
        print("      .\\.venv\\Scripts\\activate     (CMD)")
        print("   3. Set environment variables:")
        print("      Windows PowerShell:")
        print("        $env:GIS_MCP_TRANSPORT='http'")
        print("        $env:GIS_MCP_HOST='localhost'")
        print("        $env:GIS_MCP_PORT='9010'")
        print("      Windows CMD:")
        print("        set GIS_MCP_TRANSPORT=http")
        print("        set GIS_MCP_HOST=localhost")
        print("        set GIS_MCP_PORT=9010")
        print("   4. Start the server: gis-mcp")
        print("\n   ✅ The server should show:")
        print("      'Starting GIS MCP server with http transport on localhost:9010'")
        print("      'MCP endpoint will be available at: http://localhost:9010/mcp'")
        print("\n   Then come back and run this agent again!")
        print(f"\n   Error details: {type(e).__name__}: {str(e)}")
        return

    # Step 5: Create agent with system prompt
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful GIS assistant. You have access to various GIS tools through the MCP server. Use these tools to help users with geospatial operations. Always provide clear and accurate responses based on the tool results."
    )

    print("GIS Agent is ready. Type 'exit' to quit.\n")

    # Step 6: Interactive loop
    while True:
        try:
            query = input("You: ").strip()
            if query.lower() in ["exit", "quit", "q"]:
                break

            if not query:
                continue

            result = await agent.ainvoke({
                "messages": [{"role": "user", "content": query}]
            })

            # Extract AI response
            messages = result.get("messages", [])
            response_text = ""
            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    response_text = msg.content
                    break

            if not response_text:
                response_text = str(messages[-1]) if messages else "No response"

            print(f"Agent: {response_text}\n")

        except KeyboardInterrupt:
            print("\nSession terminated by user.")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())

