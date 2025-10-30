# Test SDK App - Python MCP Server

A Python-based test application demonstrating the OpenAI Apps SDK with Model Context Protocol (MCP) integration. This server showcases carousel and widget responses with proper metadata formatting for ChatGPT integration.

## Features

- **Carousel Widget**: Display multiple items in a scrollable carousel format
- **List Widget**: Show structured lists with status indicators
- **Card Widget**: Present detailed information in card layouts
- **MCP Integration**: Full Model Context Protocol support for ChatGPT
- **Apps SDK Compatible**: Includes `_meta.openai/outputTemplate` metadata for proper widget rendering

## Architecture

This application is built using:
- **FastAPI**: Modern Python web framework for building APIs
- **MCP Server**: Model Context Protocol server implementation
- **Uvicorn**: ASGI server for running the FastAPI application

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Create a virtual environment** (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the MCP server using uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or run directly with Python:

```bash
python main.py
```

The server will start at `http://localhost:8000`.

### Endpoints

- **`GET /`**: Root endpoint with server information
- **`GET /health`**: Health check endpoint
- **`POST /mcp`**: MCP protocol endpoint for tool interactions

### Available Tools

#### 1. get_carousel
Returns a carousel widget with multiple items.

**Parameters:**
- `category` (string): Category of items to display

**Example:**
```json
{
  "name": "get_carousel",
  "arguments": {
    "category": "products"
  }
}
```

#### 2. get_widget_list
Returns a list widget with multiple entries.

**Parameters:**
- `item_type` (string): Type of items to list

**Example:**
```json
{
  "name": "get_widget_list",
  "arguments": {
    "item_type": "tasks"
  }
}
```

#### 3. get_card_widget
Returns a card widget with detailed information.

**Parameters:**
- `item_id` (string): ID of the item to display

**Example:**
```json
{
  "name": "get_card_widget",
  "arguments": {
    "item_id": "123"
  }
}
```

## Widget Response Format

All widgets are returned with the proper Apps SDK metadata structure:

```json
{
  "type": "resource",
  "_meta": {
    "openai/outputTemplate": {
      "html": "http://localhost:4444/assets/widget-name.html",
      "data": {
        // Widget-specific data
      }
    }
  }
}
```

## Integration with ChatGPT

### Local Development

1. **Run the server** as described above
2. **Use ngrok** or similar tool to expose your local server:
   ```bash
   ngrok http 8000
   ```
3. **Enable Developer Mode** in ChatGPT settings
4. **Add the connector** in Settings > Connectors with your ngrok URL + `/mcp`
   - Example: `https://your-ngrok-url.ngrok-free.app/mcp`

### Production Deployment

1. Deploy to your preferred cloud platform (AWS, GCP, Azure, etc.)
2. Set the `BASE_URL` environment variable to your deployment URL:
   ```bash
   export BASE_URL=https://your-server.com
   ```
3. Configure the connector in ChatGPT with your deployment URL + `/mcp`

## Environment Variables

- `BASE_URL`: Base URL for serving static assets (default: `http://localhost:4444`)
  - Used to generate HTML paths for widget templates
  - Set this to your deployment URL in production

## Development

### Adding New Widgets

1. Create a new handler function in `main.py`:
```python
async def handle_my_widget(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    widget_data = {
        # Your widget data
    }
    return [
        {
            "type": "text",
            "text": "Description text",
        },
        {"type": "resource", **create_widget_meta("my-widget", widget_data)},
    ]
```

2. Register the tool in `list_tools()`
3. Add the tool handler in `call_tool()`

### Testing

Test the server endpoints:

```bash
# Check health
curl http://localhost:8000/health

# List available tools
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'
```

## Project Structure

```
test_sdk_app_python/
├── main.py              # Main application file with MCP server
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Troubleshooting

### Server won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 8000 is not already in use
- Verify Python version is 3.10 or higher: `python --version`

### Widgets not displaying in ChatGPT
- Verify the `BASE_URL` environment variable points to accessible widget assets
- Ensure the connector URL is correct (should end with `/mcp`)
- Check that the server is accessible from the internet (use ngrok for local development)

## License

This project follows the parent repository's MIT License.

## Related Resources

- [OpenAI Apps SDK Documentation](https://platform.openai.com/docs/guides/apps-sdk)
- [Model Context Protocol](https://spec.modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Parent Repository](https://github.com/openai/openai-apps-sdk-examples)
