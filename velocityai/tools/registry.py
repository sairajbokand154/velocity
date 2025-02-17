from typing import Dict, List, Optional, Type
from velocityai.tools.base import BaseTool

class ToolRegistry:
    """Registry for managing and discovering tools."""
    
    _instance = None
    _tools: Dict[str, Type[BaseTool]] = {}
    _categories: Dict[str, List[str]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(
        cls,
        tool_cls: Type[BaseTool],
        name: Optional[str] = None,
        category: Optional[str] = None
    ) -> None:
        """Register a tool class."""
        tool_name = name or tool_cls.__name__
        cls._tools[tool_name] = tool_cls
        
        if category:
            if category not in cls._categories:
                cls._categories[category] = []
            cls._categories[category].append(tool_name)
    
    @classmethod
    def get_tool(cls, name: str) -> Optional[Type[BaseTool]]:
        """Get a tool class by name."""
        return cls._tools.get(name)
    
    @classmethod
    def list_tools(cls) -> List[str]:
        """List all registered tools."""
        return list(cls._tools.keys())
    
    @classmethod
    def list_categories(cls) -> List[str]:
        """List all tool categories."""
        return list(cls._categories.keys())
    
    @classmethod
    def get_tools_by_category(cls, category: str) -> List[str]:
        """Get all tool names in a category."""
        return cls._categories.get(category, [])
    
    @classmethod
    def clear(cls) -> None:
        """Clear all registered tools."""
        cls._tools.clear()
        cls._categories.clear()

# Decorator for registering tools
def register_tool(name: Optional[str] = None, category: Optional[str] = None):
    """Decorator to register a tool class."""
    def decorator(cls: Type[BaseTool]) -> Type[BaseTool]:
        ToolRegistry.register(cls, name=name, category=category)
        return cls
    return decorator 