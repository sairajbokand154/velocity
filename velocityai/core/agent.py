from typing import Any, Dict, List, Optional
import json

from velocityai.core.task import Task
from velocityai.llms.base import BaseLLM

class Agent:
    """AI Agent that can execute tasks using LLMs and tools."""
    
    def __init__(
        self,
        llm: BaseLLM,
        name: str = "Assistant",
        description: Optional[str] = None
    ):
        self.llm = llm
        self.name = name
        self.description = description or f"AI Agent named {name}"
        
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task and return the result."""
        messages = [
            {"role": "system", "content": self.llm.get_system_prompt(task.tools)},
            {"role": "user", "content": task.to_prompt()}
        ]
        
        for _ in range(task.max_iterations):
            # Get next action from LLM
            response = await self.llm.chat(messages)
            
            try:
                step = json.loads(response)
                task.add_to_history(step)
                
                if step["type"] == "output":
                    return {"content": step["content"], "history": task.get_history()}
                
                if step["type"] == "action":
                    # Execute tool and get observation
                    tool_name = step["content"].get("tool")
                    tool = task.get_tool(tool_name)
                    if tool:
                        result = await tool(
                            **{k: v for k, v in step["content"].get("parameters", {}).items()}
                        )
                        observation = {
                            "type": "observation",
                            "content": str(result.result if result.success else result.error)
                        }
                        task.add_to_history(observation)
                        messages.append({"role": "assistant", "content": json.dumps(observation)})
                    
                messages.append({"role": "assistant", "content": response})
                
            except json.JSONDecodeError:
                task.add_to_history({
                    "type": "error",
                    "content": "Failed to parse LLM response as JSON"
                })
                continue
                
        return {
            "type": "error",
            "content": f"Task exceeded maximum iterations ({task.max_iterations})",
            "history": task.get_history()
        } 