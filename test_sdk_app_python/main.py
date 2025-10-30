"""Test SDK App - MCP Server with Carousel and Widget Responses"""

import os
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mcp.server.fastapi import MCPServer

# Get base URL from environment or default to localhost
BASE_URL = os.getenv("BASE_URL", "http://localhost:4444")

app = FastAPI(title="Test SDK App")
mcp_server = MCPServer("test-sdk-app")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_widget_meta(widget_name: str, data: dict[str, Any]) -> dict[str, Any]:
    """Create widget metadata for Apps SDK integration."""
    return {
        "_meta": {
            "openai/outputTemplate": {
                "html": f"{BASE_URL}/assets/{widget_name}.html",
                "data": data,
            }
        }
    }


@mcp_server.list_tools()
async def list_tools() -> list[dict[str, Any]]:
    """List available tools."""
    return [
        {
            "name": "get_carousel",
            "description": "Returns a carousel widget with multiple items",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category of items to display",
                    }
                },
            },
        },
        {
            "name": "get_widget_list",
            "description": "Returns a list widget with multiple entries",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "item_type": {
                        "type": "string",
                        "description": "Type of items to list",
                    }
                },
            },
        },
        {
            "name": "get_card_widget",
            "description": "Returns a card widget with detailed information",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "ID of the item to display",
                    }
                },
            },
        },
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """Handle tool calls and return responses with widgets."""
    if name == "get_carousel":
        return await handle_carousel(arguments)
    elif name == "get_widget_list":
        return await handle_widget_list(arguments)
    elif name == "get_card_widget":
        return await handle_card_widget(arguments)
    else:
        return [
            {
                "type": "text",
                "text": f"Unknown tool: {name}",
            }
        ]


async def handle_carousel(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a carousel widget response."""
    category = arguments.get("category", "products")

    # Sample carousel data
    carousel_items = [
        {
            "id": "item1",
            "title": f"{category.capitalize()} Item 1",
            "description": "This is the first item in the carousel",
            "image": "https://via.placeholder.com/300x200?text=Item+1",
            "price": "$29.99",
        },
        {
            "id": "item2",
            "title": f"{category.capitalize()} Item 2",
            "description": "This is the second item in the carousel",
            "image": "https://via.placeholder.com/300x200?text=Item+2",
            "price": "$39.99",
        },
        {
            "id": "item3",
            "title": f"{category.capitalize()} Item 3",
            "description": "This is the third item in the carousel",
            "image": "https://via.placeholder.com/300x200?text=Item+3",
            "price": "$49.99",
        },
    ]

    widget_data = {"items": carousel_items, "category": category}

    return [
        {
            "type": "text",
            "text": f"Here's a carousel of {category} items. Browse through the options!",
        },
        {"type": "resource", **create_widget_meta("carousel", widget_data)},
    ]


async def handle_widget_list(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a list widget response."""
    item_type = arguments.get("item_type", "tasks")

    # Sample list data
    list_items = [
        {"id": "1", "name": f"{item_type.capitalize()} Alpha", "status": "active"},
        {"id": "2", "name": f"{item_type.capitalize()} Beta", "status": "pending"},
        {"id": "3", "name": f"{item_type.capitalize()} Gamma", "status": "completed"},
        {"id": "4", "name": f"{item_type.capitalize()} Delta", "status": "active"},
    ]

    widget_data = {"items": list_items, "type": item_type}

    return [
        {
            "type": "text",
            "text": f"Here's a list of {item_type}. Each item shows its current status.",
        },
        {"type": "resource", **create_widget_meta("list", widget_data)},
    ]


async def handle_card_widget(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a card widget response."""
    item_id = arguments.get("item_id", "default")

    # Sample card data
    card_data = {
        "id": item_id,
        "title": f"Item {item_id}",
        "subtitle": "Detailed Information",
        "description": "This is a detailed card view with comprehensive information about the selected item.",
        "image": f"https://via.placeholder.com/400x300?text=Item+{item_id}",
        "metadata": {
            "Created": "2025-10-30",
            "Status": "Active",
            "Category": "Test",
        },
        "actions": [
            {"label": "View Details", "action": "view"},
            {"label": "Edit", "action": "edit"},
        ],
    }

    return [
        {
            "type": "text",
            "text": f"Here's the detailed card for item {item_id}.",
        },
        {"type": "resource", **create_widget_meta("card", card_data)},
    ]


# Mount MCP server
app.include_router(mcp_server.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Test SDK App - MCP Server Running", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "base_url": BASE_URL}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
