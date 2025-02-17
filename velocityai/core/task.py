from typing import Any, Dict, List, Optional
from velocityai.core.tool import Tool

class Task:
    """Represents a task to be executed by an AI agent."""
    
    def __init__(
        self,
        description: str,
        tools: Optional[List[Tool]] = None,
        context: Optional[Dict[str, Any]] = None,
        max_iterations: int = 10
    ):
        self.description = description
        self.tools = tools or []
        self.context = context or {}
        self.max_iterations = max_iterations
        self.history: List[Dict[str, Any]] = []
        
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the task."""
        self.tools.append(tool)
        
    def add_context(self, key: str, value: Any) -> None:
        """Add context information to the task."""
        self.context[key] = value
        
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        for tool in self.tools:
            if tool.metadata.name == name:
                return tool
        return None
    
    def add_to_history(self, step: Dict[str, Any]) -> None:
        """Add a step to the task history."""
        self.history.append(step)
        
    def get_history(self) -> List[Dict[str, Any]]:
        """Get the task execution history."""
        return self.history
    
    def to_prompt(self) -> str:
        """Convert task to a prompt for the LLM."""
        tool_descriptions = "\n".join(
            [f"- {tool.metadata.name}: {tool.metadata.description}" for tool in self.tools]
        )
        
        context_str = "\n".join(
            [f"{key}: {value}" for key, value in self.context.items()]
        )
        
        return f"""Task Description: {self.description}

Available Context:
{context_str}

Available Tools:
{tool_descriptions}

Please help me complete this task by following the steps:
1. Analyze the task and create a plan
2. Execute the plan using available tools
3. Provide the final result""" 