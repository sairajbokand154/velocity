from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

class Tool:
    """Base class for all tools in Velocity."""
    
    def __init__(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters or {}
        
    async def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        return await self.func(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

class FunctionTool(Tool):
    """Tool created from a function with type hints."""
    
    def __init__(self, func: Callable):
        """Create a tool from a function using its docstring and type hints."""
        super().__init__(
            name=func.__name__,
            description=func.__doc__ or "No description available",
            func=func,
            parameters=self._get_parameters(func)
        )
    
    @staticmethod
    def _get_parameters(func: Callable) -> Dict[str, Any]:
        """Extract parameters from function type hints."""
        import inspect
        
        params = {}
        signature = inspect.signature(func)
        
        for name, param in signature.parameters.items():
            params[name] = {
                "type": str(param.annotation),
                "default": None if param.default == inspect.Parameter.empty else param.default,
                "required": param.default == inspect.Parameter.empty
            }
        
        return params 