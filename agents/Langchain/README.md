# GIS MCP LangChain Agent

A LangChain-based agent implementation that connects to the GIS MCP (Model Context Protocol) server to provide geospatial analysis capabilities through natural language interactions.

## Overview

This agent utilizes:

- **LangChain**: For agent orchestration and tool integration
- **OpenRouter API**: For language model access (supports multiple models)
- **GIS MCP Server**: For geospatial operations and analysis
- **MultiServerMCPClient**: For seamless MCP server integration

## Features

- Natural language interface for GIS operations
- Support for multiple AI models via OpenRouter
- Automatic tool discovery from MCP server
- Interactive command-line interface
- Comprehensive error handling and diagnostics

## Prerequisites

- Python 3.10 or higher
- Virtual environment (recommended)
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))
- GIS MCP server installed and running

## Installation

### 1. Install GIS MCP Server

```bash
pip install gis-mcp
```

### 2. Install Agent Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install langchain langchain-openai langchain-core langchain-mcp-adapters python-dotenv
```

## Configuration

### 1. Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Alternatively, set the environment variable directly:

**Windows PowerShell:**

```powershell
$env:OPENROUTER_API_KEY="your_api_key_here"
```

**Windows CMD:**

```cmd
set OPENROUTER_API_KEY=your_api_key_here
```

**Mac/Linux:**

```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

### 2. Configure MCP Server

The agent expects the GIS MCP server to be running on `http://localhost:9010/mcp`.

Start the server in a separate terminal:

**Windows PowerShell:**

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Set environment variables
$env:GIS_MCP_TRANSPORT="http"
$env:GIS_MCP_HOST="localhost"
$env:GIS_MCP_PORT="9010"

# Start server
gis-mcp
```

**Windows CMD:**

```cmd
.\.venv\Scripts\activate
set GIS_MCP_TRANSPORT=http
set GIS_MCP_HOST=localhost
set GIS_MCP_PORT=9010
gis-mcp
```

**Mac/Linux:**

```bash
source .venv/bin/activate
export GIS_MCP_TRANSPORT=http
export GIS_MCP_HOST=localhost
export GIS_MCP_PORT=9010
gis-mcp
```

**Expected server output:**

```
Starting GIS MCP server with http transport on localhost:9010
MCP endpoint will be available at: http://localhost:9010/mcp
```

### 3. Configure Model (Optional)

Edit `my_gis_agent.py` to change the model:

```python
MODEL_NAME = "deepseek/deepseek-chat-v3.1"  # Default model
```

**Available models on OpenRouter:**

- `deepseek/deepseek-chat-v3.1` - Cost-effective, excellent for technical tasks
- `google/gemini-pro-1.5` - Strong general performance
- `google/gemini-2.0-flash-exp` - Fast Gemini model
- `openai/gpt-4o` - Most capable, higher cost
- `anthropic/claude-3.5-sonnet` - Excellent reasoning

Browse all models at [https://openrouter.ai/models](https://openrouter.ai/models)

## Usage

### Running the Agent

1. **Ensure the MCP server is running** (see Configuration step 2)

2. **Run the agent:**

   ```bash
   python my_gis_agent.py
   ```

3. **Interact with the agent:**

   ```
   You: Calculate the distance between points (0, 0) and (1, 1) in WGS84
   Agent: [Response with calculation results]
   ```

4. **Exit the agent:**
   - Type `exit`, `quit`, or `q`
   - Or press `Ctrl+C`

### Example Queries

- **Distance calculations:**

  - "Calculate the distance between points (0, 0) and (1, 1) in WGS84"
  - "What's the distance from New York to Los Angeles?"

- **Coordinate transformations:**

  - "Transform point (0, 30) from WGS84 to Mercator projection"
  - "Convert coordinates (40.7128, -74.0060) to UTM zone 18N"

- **Spatial operations:**

  - "Create a 1km buffer around point (lat: 0, lon: 30)"
  - "What is the area of a polygon with coordinates [(0,0), (1,0), (1,1), (0,1), (0,0)]?"

- **General queries:**
  - "What GIS operations can you help me with?"
  - "List all available geospatial tools"

## Architecture

### Components

1. **Language Model (LLM)**

   - Configured via `ChatOpenAI` with OpenRouter base URL
   - Handles natural language understanding and generation

2. **MCP Client**

   - `MultiServerMCPClient` manages connection to GIS MCP server
   - Uses `streamable_http` transport for HTTP-based communication
   - Lazy connection: connects only when tools are requested

3. **Agent**

   - LangChain agent created with `create_agent()`
   - Integrates LLM with MCP tools
   - Handles tool selection and execution automatically

4. **Tool Integration**
   - Tools are automatically discovered from MCP server
   - Converted to LangChain-compatible format
   - Made available to the agent for execution

### Code Structure

```python
# Configuration
- Environment variable loading
- API key validation
- Server URL configuration

# Initialization
- Language model setup
- MCP client creation
- Tool loading from server

# Agent Creation
- Agent instantiation with tools
- System prompt configuration

# Interactive Session
- User input handling
- Agent invocation
- Response extraction and display
```

## Troubleshooting

### "OPENROUTER_API_KEY is not set"

**Solution:** Ensure the API key is set in your `.env` file or as an environment variable:

```bash
# Check if set
echo $OPENROUTER_API_KEY  # Mac/Linux
echo %OPENROUTER_API_KEY%  # Windows CMD
echo $env:OPENROUTER_API_KEY  # Windows PowerShell
```

### "Failed to connect to GIS MCP server"

**Symptoms:**

- Connection errors when starting the agent
- "No tools found" message

**Solutions:**

1. **Verify server is running:**

   - Check the server terminal window
   - Server should show: "Starting GIS MCP server with http transport on localhost:9010"

2. **Check server URL:**

   - Default: `http://localhost:9010/mcp`
   - Verify port matches in both server and agent configuration

3. **Test server connection:**

   ```bash
   curl http://localhost:9010/mcp/tools/list
   ```

   Should return a JSON list of available tools

4. **Verify environment variables:**
   - Server must have `GIS_MCP_TRANSPORT=http`
   - Server must have `GIS_MCP_PORT=9010`

### "No tools found"

**Possible causes:**

- Server not running
- Wrong port configuration
- Server not in HTTP transport mode

**Solution:**

- Restart server with correct environment variables
- Verify server is accessible at the configured URL

### Import Errors

**Solution:** Install all required dependencies:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install langchain langchain-openai langchain-core langchain-mcp-adapters python-dotenv
```

### Agent Not Using Tools

**Possible reasons:**

- Query doesn't require GIS operations
- Tools not loaded successfully
- Model not recognizing when to use tools

**Solutions:**

- Use more specific queries (e.g., "Calculate distance...", "Transform coordinates...")
- Verify tools were loaded (check startup messages)
- Try different models if tool usage is inconsistent

## Customization

### Change System Prompt

Edit the `SYSTEM_PROMPT` constant in `my_gis_agent.py`:

```python
SYSTEM_PROMPT: str = (
    "You are an expert geospatial analyst. "
    "Provide detailed explanations of all calculations. "
    "Always verify results using appropriate GIS tools."
)
```

### Adjust Temperature

Modify the `DEFAULT_TEMPERATURE` constant:

```python
DEFAULT_TEMPERATURE: float = 0.7  # Range: 0.0-2.0
# Lower = more focused/deterministic
# Higher = more creative/varied
```

### Change Server Configuration

Modify the `MCP_SERVER_URL` constant:

```python
MCP_SERVER_URL: str = "http://localhost:9010/mcp"
```

Ensure the server is configured to match this URL.

## Dependencies

See `requirements.txt` for complete dependency list:

- `langchain>=1.0.0` - Agent framework
- `langchain-openai>=1.0.0` - OpenAI-compatible API support
- `langchain-core>=1.0.0` - Core LangChain functionality
- `langchain-mcp-adapters>=0.1.0` - MCP server integration
- `python-dotenv>=1.0.0` - Environment variable management

## Documentation

- **LangChain MCP Documentation**: [https://docs.langchain.com/oss/python/langchain/mcp](https://docs.langchain.com/oss/python/langchain/mcp)
- **OpenRouter API**: [https://openrouter.ai/docs](https://openrouter.ai/docs)
- **OpenRouter Models**: [https://openrouter.ai/models](https://openrouter.ai/models)
- **GIS MCP Server**: See main project README for available tools

## License

See main project LICENSE file.

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review code comments in `my_gis_agent.py`
3. Consult LangChain and OpenRouter documentation
4. Check GIS MCP server documentation for available tools
