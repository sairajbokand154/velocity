from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

class ToolParameter(BaseModel):
    """Schema for tool parameter definition."""
    name: str = Field(..., description="Name of the parameter")
    type: str = Field(..., description="Type of the parameter")
    description: Optional[str] = Field(None, description="Description of the parameter")
    required: bool = Field(True, description="Whether the parameter is required")
    default: Optional[Any] = Field(None, description="Default value for the parameter")

class ToolMetadata(BaseModel):
    """Schema for tool metadata."""
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of what the tool does")
    parameters: List[ToolParameter] = Field(default_factory=list, description="Parameters accepted by the tool")
    return_type: str = Field(..., description="Return type of the tool")
    category: Optional[str] = Field(None, description="Category of the tool (e.g., 'IO', 'Math', 'API')")
    version: Optional[str] = Field(None, description="Version of the tool")
    author: Optional[str] = Field(None, description="Author of the tool")

class ToolResult(BaseModel):
    """Schema for tool execution result."""
    success: bool = Field(..., description="Whether the tool execution was successful")
    result: Optional[Any] = Field(None, description="Result of the tool execution")
    error: Optional[str] = Field(None, description="Error message if execution failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the execution") 