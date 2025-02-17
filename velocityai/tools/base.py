from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, get_type_hints
import inspect
import logging
from functools import wraps

from velocityai.tools.schema import ToolMetadata, ToolParameter, ToolResult

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """Base class for all tools in Velocity."""
    
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        version: Optional[str] = None,
        author: Optional[str] = None
    ):
        self.metadata = ToolMetadata(
            name=name or self.__class__.__name__,
            description=description or self.__doc__ or "No description available",
            parameters=self._get_parameters(),
            return_type=self._get_return_type(),
            category=category,
            version=version,
            author=author
        )
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        pass
    
    def _get_parameters(self) -> List[ToolParameter]:
        """Extract parameters from execute method signature."""
        signature = inspect.signature(self.execute)
        type_hints = get_type_hints(self.execute)
        
        parameters = []
        for name, param in signature.parameters.items():
            if name == 'self' or name == 'kwargs':
                continue
                
            param_type = type_hints.get(name, Any).__name__
            parameters.append(
                ToolParameter(
                    name=name,
                    type=param_type,
                    description=None,  # Could be extracted from docstring in future
                    required=param.default == inspect.Parameter.empty,
                    default=None if param.default == inspect.Parameter.empty else param.default
                )
            )
        
        return parameters
    
    def _get_return_type(self) -> str:
        """Get return type of execute method."""
        return_hint = get_type_hints(self.execute).get('return', Any)
        return return_hint.__name__
    
    async def __call__(self, **kwargs) -> ToolResult:
        """Execute tool and wrap result in ToolResult."""
        try:
            result = await self.execute(**kwargs)
            return ToolResult(
                success=True,
                result=result,
                metadata={"tool_name": self.metadata.name}
            )
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}", exc_info=True)
            return ToolResult(
                success=False,
                error=str(e),
                metadata={"tool_name": self.metadata.name}
            )
    
    @classmethod
    def from_function(
        cls,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> 'FunctionTool':
        """Create a tool from a function."""
        return FunctionTool(func, name, description, **kwargs)

class FunctionTool(BaseTool):
    """Tool created from a function."""
    
    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ):
        self.func = func
        super().__init__(
            name=name or func.__name__,
            description=description or func.__doc__ or "No description available",
            **kwargs
        )
    
    async def execute(self, **kwargs) -> Any:
        """Execute the wrapped function."""
        if inspect.iscoroutinefunction(self.func):
            return await self.func(**kwargs)
        return self.func(**kwargs) 