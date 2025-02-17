"""
VelocityAI - A Modular AI Agent Framework
"""

__version__ = "0.1.0"

from velocityai.core.agent import Agent
from velocityai.core.task import Task
from velocityai.tools.base import BaseTool, FunctionTool
from velocityai.tools.registry import register_tool, ToolRegistry
from velocityai.llms.base import BaseLLM
from velocityai.core.executor import run

__all__ = [
    "Agent",
    "Task",
    "BaseTool",
    "FunctionTool",
    "register_tool",
    "ToolRegistry",
    "BaseLLM",
    "run"
] 