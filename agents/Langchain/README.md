# GIS MCP Agents - From Zero to Hero Tutorial

Welcome! This tutorial will guide you from complete beginner to creating your own AI agent that can perform geospatial operations. No prior experience needed - we'll cover everything step by step.

## 📋 Table of Contents

- [What You'll Build](#what-youll-build)
- [Prerequisites](#prerequisites)
- [Step 1: Install GIS MCP Server](#step-1-install-gis-mcp-server)
- [Step 2: Install Agent Dependencies](#step-2-install-agent-dependencies)
- [Step 3: Start the MCP Server](#step-3-start-the-mcp-server)
- [Step 4: Get Your OpenRouter API Key](#step-4-get-your-openrouter-api-key)
- [Step 5: Select a Model](#step-5-select-a-model)
- [Step 6: Build Your First Agent from Scratch](#step-6-build-your-first-agent-from-scratch)
- [Step 7: Test Your Agent](#step-7-test-your-agent)
- [Step 8: Customize Your Agent](#step-8-customize-your-agent)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## What You'll Build

By the end of this tutorial, you'll have:

- ✅ A working GIS MCP server running locally
- ✅ Your own AI agent built with LangChain
- ✅ An agent that can perform geospatial operations like:
  - Calculate distances between points
  - Transform coordinates between different systems
  - Create buffers around locations
  - Perform spatial analysis
  - And much more!

## Prerequisites

Before we start, make sure you have:

- **Python 3.10 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **A code editor** (VS Code, PyCharm, or any text editor)
- **An internet connection** for installing packages
- **Basic command line knowledge** (we'll guide you through everything)

That's it! No prior AI or GIS experience needed.

---

## Step 1: Install GIS MCP Server

The GIS MCP Server provides all the geospatial tools your agent will use. Let's install it.

### Option A: Using pip (Recommended)

1. **Open your terminal/command prompt**

   - **Windows**: Press `Win + R`, type `cmd` or `powershell`, press Enter
   - **Mac/Linux**: Open Terminal

2. **Create a project folder** (optional but recommended):

   ```bash
   mkdir gis-agent-project
   cd gis-agent-project
   ```

3. **Create a virtual environment** (keeps packages organized):

   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Mac/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   You should see `(.venv)` at the start of your command line.

4. **Install GIS MCP Server**:

   ```bash
   pip install gis-mcp
   ```

   Wait for the installation to complete. This may take a few minutes.

### Option B: Using uv (Faster Alternative)

If you want faster installation:

```bash
# Install uv first
pip install uv

# Create virtual environment
uv venv --python=3.10

# Activate it
# Windows:
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate

# Install GIS MCP
uv pip install gis-mcp
```

**✅ Verification**: Test that it's installed:

```bash
gis-mcp --help
```

You should see help text. If you get an error, make sure your virtual environment is activated.

---

## Step 2: Install Agent Dependencies

Now let's install the packages needed to build your agent with LangChain.

1. **Create a requirements file** (or install directly):

   Create a file named `requirements.txt` in your project folder with this content:

   ```
   langchain>=0.1.0
   langchain-openai>=0.1.0
   langchain-core>=0.1.0
   httpx>=0.25.0
   python-dotenv>=1.0.0
   ```

2. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Or install them one by one:

   ```bash
   pip install langchain langchain-openai langchain-core httpx python-dotenv
   ```

**✅ Verification**: Check that LangChain is installed:

```bash
python -c "import langchain; print('LangChain installed successfully!')"
```

---

## Step 3: Start the MCP Server

The MCP server needs to be running for your agent to use GIS tools. Let's start it in HTTP mode.

### Windows (PowerShell)

Open a **new terminal window** (keep your current one open too - you'll need both):

```powershell
# Activate your virtual environment first
.\.venv\Scripts\Activate.ps1

# Set environment variables
$env:GIS_MCP_TRANSPORT="http"
$env:GIS_MCP_HOST="localhost"
$env:GIS_MCP_PORT="8080"

# Start the server
gis-mcp
```

### Windows (Command Prompt)

```cmd
.\.venv\Scripts\activate
set GIS_MCP_TRANSPORT=http
set GIS_MCP_HOST=localhost
set GIS_MCP_PORT=8080
gis-mcp
```

### Mac/Linux

```bash
source .venv/bin/activate
export GIS_MCP_TRANSPORT=http
export GIS_MCP_HOST=localhost
export GIS_MCP_PORT=8080
gis-mcp
```

**✅ You should see**:

```
Starting GIS MCP server with http transport on localhost:8080
MCP endpoint will be available at: http://localhost:8080/mcp
```

**⚠️ Important**: Keep this terminal window open! The server needs to keep running. You'll use your other terminal for the next steps.

**✅ Verification**: Test that the server is running:

Open a **new terminal** and run:

```bash
# Windows PowerShell
curl http://localhost:8080/mcp/tools/list

# Or use Python
python -c "import requests; print(requests.get('http://localhost:8080/mcp/tools/list').json())"
```

You should see a list of available GIS tools in JSON format.

---

## Step 4: Get Your OpenRouter API Key

OpenRouter is a service that gives you access to many AI models (including DeepSeek, Gemini, GPT-4, Claude, etc.) through a single API. This is perfect for our agent!

### Create an OpenRouter Account

1. **Visit** [https://openrouter.ai](https://openrouter.ai)
2. **Click "Sign Up"** (or "Log In" if you have an account)
3. **Create your account** (you can use Google/GitHub to sign up quickly)

### Get Your API Key

1. **Navigate to API Keys**:

   - Click your profile icon (top right)
   - Select "Keys" or go directly to [https://openrouter.ai/keys](https://openrouter.ai/keys)

2. **Create a new key**:

   - Click "Create Key"
   - Give it a name (e.g., "GIS Agent")
   - Optionally set a credit limit (you can leave it unlimited)
   - Click "Create"

3. **Copy your API key**:
   - Click the copy icon next to your key
   - **Save it somewhere safe** - you'll need it in the next steps
   - ⚠️ **Never share your API key publicly!**

### Set Your API Key as Environment Variable

**Windows (PowerShell)**:

```powershell
$env:OPENROUTER_API_KEY="your_api_key_here"
```

**Windows (Command Prompt)**:

```cmd
set OPENROUTER_API_KEY=your_api_key_here
```

**Mac/Linux**:

```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

**✅ Verification**: Check that it's set:

```bash
# Windows PowerShell
echo $env:OPENROUTER_API_KEY

# Windows CMD
echo %OPENROUTER_API_KEY%

# Mac/Linux
echo $OPENROUTER_API_KEY
```

You should see your API key printed (don't worry, it's just in your terminal).

---

## Step 5: Select a Model

OpenRouter gives you access to many models. Here are some great options for GIS agents:

### Recommended Models

1. **DeepSeek Chat v3.1** (Best for cost-effectiveness)

   - Model ID: `deepseek/deepseek-chat-v3.1`
   - Great reasoning, very affordable
   - Excellent for technical tasks

2. **Google Gemini Pro 1.5** (Best for general use)

   - Model ID: `google/gemini-pro-1.5`
   - Strong performance, good balance
   - Also available: `google/gemini-2.0-flash-exp`

3. **GPT-4o** (Best for complex tasks)

   - Model ID: `openai/gpt-4o`
   - Most capable, higher cost

4. **Claude 3.5 Sonnet** (Best for analysis)
   - Model ID: `anthropic/claude-3.5-sonnet`
   - Excellent reasoning

### Browse All Models

Visit [https://openrouter.ai/models](https://openrouter.ai/models) to see all available models with pricing and capabilities.

**💡 Tip**: For this tutorial, we'll use `deepseek/deepseek-chat-v3.1` as it's cost-effective and works great. You can easily switch to any other model later!

**Note**: Gemini models are available on OpenRouter! You can use `google/gemini-pro-1.5` or `google/gemini-2.0-flash-exp` just like any other OpenRouter model - no need for a separate Google API key.

---

## Step 6: Build Your First Agent from Scratch

Now the fun part! Let's build your agent step by step.

### Create Your Agent File

Create a new file called `my_gis_agent.py` in your project folder:

```python
"""
My First GIS Agent
A simple agent that uses LangChain to connect to GIS MCP server
"""

import os
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
import httpx

# Step 1: Configure your API key and MCP server
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MCP_SERVER_URL = "http://localhost:8080/mcp"
MODEL_NAME = "deepseek/deepseek-chat-v3.1"  # Change this to any OpenRouter model

# Step 2: Create the language model
# OpenRouter uses OpenAI-compatible API, so we use ChatOpenAI with custom base URL
llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
)

# Step 3: Create a simple HTTP client to fetch tools from MCP server
async def get_mcp_tools():
    """Fetch available tools from the MCP server"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{MCP_SERVER_URL}/tools/list")
            response.raise_for_status()
            tools_data = response.json()
            return tools_data.get("tools", [])
        except Exception as e:
            print(f"Error fetching tools: {e}")
            return []

# Step 4: Create a tool wrapper for MCP tools
from langchain_core.tools import BaseTool

class MCPTool(BaseTool):
    """Wrapper to make MCP tools work with LangChain"""

    def __init__(self, tool_name: str, tool_description: str, mcp_url: str):
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.mcp_url = mcp_url
        super().__init__(name=tool_name, description=tool_description)

    def _run(self, *args, **kwargs):
        """Synchronous version (not used)"""
        raise NotImplementedError("Use async version")

    async def _arun(self, *args, **kwargs):
        """Call the MCP tool"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.mcp_url}/tools/call",
                    json={
                        "name": self.tool_name,
                        "arguments": kwargs
                    }
                )
                response.raise_for_status()
                result = response.json()
                # Format the result
                if isinstance(result, dict):
                    return str(result.get("content", result))
                return str(result)
            except Exception as e:
                return f"Error: {str(e)}"

# Step 5: Main function to run the agent
async def main():
    print("🤖 Building your GIS Agent...")
    print(f"📡 Connecting to MCP server at {MCP_SERVER_URL}")

    # Fetch tools from MCP server
    print("📋 Loading GIS tools...")
    tools_data = await get_mcp_tools()

    if not tools_data:
        print("❌ No tools found! Make sure MCP server is running.")
        return

    print(f"✅ Found {len(tools_data)} GIS tools!")

    # Convert MCP tools to LangChain tools
    langchain_tools = []
    for tool_data in tools_data:
        tool = MCPTool(
            tool_name=tool_data.get("name", ""),
            tool_description=tool_data.get("description", ""),
            mcp_url=MCP_SERVER_URL
        )
        langchain_tools.append(tool)

    # Create the agent with tools
    print("🔧 Creating agent...")
    system_prompt = """You are a helpful GIS assistant.
You have access to various GIS tools through the MCP server.
Use these tools to help users with geospatial operations.
Always provide clear and accurate responses based on the tool results."""

    agent = create_agent(
        model=llm,
        tools=langchain_tools,
        system_prompt=system_prompt,
        debug=True,  # Set to False to reduce output
    )

    print("✅ Agent ready!")
    print("\n" + "="*60)
    print("Ask me anything about GIS operations!")
    print("Type 'exit' to quit")
    print("="*60 + "\n")

    # Interactive loop
    while True:
        try:
            query = input("You: ").strip()
            if query.lower() in ['exit', 'quit', 'q']:
                break

            if not query:
                continue

            print("\n🤔 Thinking...\n")

            # Run the agent
            result = await agent.ainvoke({
                "messages": [HumanMessage(content=query)]
            })

            # Extract the response
            messages = result.get("messages", [])
            response_text = ""
            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    response_text = msg.content
                    break

            if not response_text:
                response_text = str(messages[-1]) if messages else "No response"

            print(f"\n🤖 Agent: {response_text}\n")
            print("-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    # Make sure API key is set
    if not OPENROUTER_API_KEY:
        print("❌ Error: OPENROUTER_API_KEY not set!")
        print("Set it with: $env:OPENROUTER_API_KEY='your_key' (PowerShell)")
        print("Or: export OPENROUTER_API_KEY='your_key' (Mac/Linux)")
        exit(1)

    # Run the agent
    asyncio.run(main())
```

### Save and Run Your Agent

1. **Save the file** as `my_gis_agent.py`

2. **Make sure**:

   - Your MCP server is still running (Step 3)
   - Your API key is set (Step 4)

3. **Run your agent**:

   ```bash
   python my_gis_agent.py
   ```

**🎉 Congratulations!** You just built your first GIS agent from scratch!

---

## Step 7: Test Your Agent

Now let's test it with some real GIS queries!

### Test Queries

Try asking your agent:

1. **"What GIS operations can you help me with?"**

   - This will show you what tools are available

2. **"Calculate the distance between points (0, 0) and (1, 1) in WGS84"**

   - Tests coordinate calculations

3. **"Transform point (0, 30) from WGS84 to Mercator projection"**

   - Tests coordinate transformation

4. **"Create a 1km buffer around point (lat: 0, lon: 30)"**

   - Tests geometric operations

5. **"What is the area of a polygon with coordinates [(0,0), (1,0), (1,1), (0,1), (0,0)]?"**
   - Tests area calculations

### What to Expect

- The agent will think about your query
- It will automatically select and use the appropriate GIS tools
- You'll see tool calls in the output (if debug=True)
- The agent will provide a clear answer

**💡 Tip**: Watch the terminal output - you'll see the agent's "thinking" process as it decides which tools to use!

---

## Step 8: Customize Your Agent

Now that you have a working agent, let's customize it!

### Change the Model

Edit `my_gis_agent.py` and change the model:

```python
# Try different models:
MODEL_NAME = "google/gemini-pro-1.5"  # Use Gemini via OpenRouter
# MODEL_NAME = "openai/gpt-4o"        # Use GPT-4
# MODEL_NAME = "anthropic/claude-3.5-sonnet"  # Use Claude
```

### Adjust Temperature

Control how creative the agent is:

```python
llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,  # Lower = more focused, Higher = more creative (0.0-2.0)
)
```

### Customize the System Prompt

Make your agent specialized:

```python
system_prompt = """You are an expert geospatial analyst assistant.
You specialize in coordinate transformations and spatial analysis.
Always explain your calculations step by step.
Use the available GIS tools to provide accurate results."""
```

### Add Custom Behavior

You can add features like:

- **Save conversation history**
- **Export results to files**
- **Add custom tools**
- **Create a web interface**
- **Add error handling**

The possibilities are endless!

---

## Troubleshooting

### "OPENROUTER_API_KEY not set"

**Solution**: Make sure you set the environment variable in the same terminal where you're running the script:

```powershell
# Windows PowerShell
$env:OPENROUTER_API_KEY="your_key"
python my_gis_agent.py
```

### "Cannot connect to MCP server"

**Symptoms**:

- `Error fetching tools: ...`
- `No tools found!`

**Solutions**:

1. **Check if server is running**:

   - Look at your MCP server terminal - it should show it's running
   - If not, go back to Step 3 and start it

2. **Check the URL**:

   - Make sure `MCP_SERVER_URL = "http://localhost:8080/mcp"` matches your server port
   - If you changed the port, update the URL

3. **Test the connection**:
   ```bash
   curl http://localhost:8080/mcp/tools/list
   ```

### "No tools available"

**Solution**:

- Make sure the MCP server is in HTTP mode (not STDIO)
- Check that you set `GIS_MCP_TRANSPORT=http` when starting the server

### Agent doesn't use tools

**Possible reasons**:

- The query doesn't require GIS operations
- Try more specific queries like "Calculate distance..." or "Transform coordinates..."
- Check that tools were loaded (you should see "Found X GIS tools!")

### Import errors

**Solution**: Make sure all dependencies are installed:

```bash
pip install langchain langchain-openai langchain-core httpx python-dotenv
```

---

## Next Steps

Congratulations! You've built a working GIS agent. Here's what you can do next:

### 1. Explore More Models

Try different models on OpenRouter:

- `google/gemini-2.0-flash-exp` - Fast Gemini model
- `anthropic/claude-3.5-sonnet` - Great reasoning
- `openai/gpt-4o` - Most capable

### 2. Add More Features

- **File I/O**: Save/load geospatial data
- **Visualization**: Create maps with results
- **Batch Processing**: Process multiple queries
- **Web Interface**: Build a web UI with Flask/FastAPI

### 3. Learn More

- **LangChain Documentation**: [https://python.langchain.com](https://python.langchain.com)
- **OpenRouter Models**: [https://openrouter.ai/models](https://openrouter.ai/models)
- **GIS MCP Server**: Check the main project README for all available tools

### 4. Share Your Agent

- Add it to your portfolio
- Share on GitHub
- Contribute improvements back to the project

---

## Quick Reference

### Environment Variables

```powershell
# Windows PowerShell
$env:OPENROUTER_API_KEY="your_key"
$env:GIS_MCP_TRANSPORT="http"
$env:GIS_MCP_PORT="8080"
```

```bash
# Mac/Linux
export OPENROUTER_API_KEY="your_key"
export GIS_MCP_TRANSPORT="http"
export GIS_MCP_PORT="8080"
```

### Common Commands

```bash
# Start MCP server
gis-mcp

# Test server
curl http://localhost:8080/mcp/tools/list

# Run your agent
python my_gis_agent.py
```

### Model IDs

- `deepseek/deepseek-chat-v3.1` - DeepSeek (recommended for beginners)
- `google/gemini-pro-1.5` - Gemini Pro
- `google/gemini-2.0-flash-exp` - Gemini Flash
- `openai/gpt-4o` - GPT-4
- `anthropic/claude-3.5-sonnet` - Claude

---

## Summary

You've learned:

✅ How to install and run the GIS MCP server  
✅ How to get an OpenRouter API key  
✅ How to select and use different AI models  
✅ How to build a LangChain agent from scratch  
✅ How to connect your agent to GIS tools  
✅ How to customize and extend your agent

**You're now ready to build amazing geospatial AI applications!** 🚀

---

## Need Help?

- **Check the troubleshooting section** above
- **Review the code comments** in `my_gis_agent.py`
- **Visit OpenRouter docs**: [https://openrouter.ai/docs](https://openrouter.ai/docs)
- **Check LangChain docs**: [https://python.langchain.com](https://python.langchain.com)

Happy coding! 🎉
