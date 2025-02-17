from typing import Any, Dict, List, Optional, Union

from velocityai.core.agent import Agent
from velocityai.core.task import Task
from velocityai.core.tool import Tool, FunctionTool
from velocityai.llms.base import BaseLLM

async def run(
    llm: BaseLLM,
    task_description: str,
    tools: Optional[List[Union[Tool, FunctionTool]]] = None,
    context: Optional[Dict[str, Any]] = None,
    max_iterations: int = 10
) -> Dict[str, Any]:
    """
    Execute a task using an AI agent.
    
    Args:
        llm: The language model to use
        task_description: Description of the task to execute
        tools: List of tools available to the agent
        context: Additional context for the task
        max_iterations: Maximum number of iterations before giving up
        
    Returns:
        Dict containing the task result
    """
    # Create task
    task = Task(
        description=task_description,
        tools=tools,
        context=context,
        max_iterations=max_iterations
    )
    
    # Create agent
    agent = Agent(llm=llm)
    
    # Execute task
    result = await agent.execute_task(task)
    
    return result 