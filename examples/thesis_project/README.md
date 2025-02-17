# Thesis Writing Example using Velocity

This example demonstrates how to use the Velocity framework to create specialized AI agents for thesis research and writing.

## Project Structure

```
thesis_project/
├── agents/                # Custom agent implementations
│   ├── researcher.py     # Research agent for gathering information
│   └── writer.py         # Writer agent for content creation
├── tools/                # Custom tools (add your own)
└── main.py              # Example usage script
```

## Getting Started

1. Install the Velocity package:
```bash
pip install velocity
```

2. Set up your environment variables:
```bash
# Create a .env file with your API keys
GEMINI_API_KEY=your_api_key_here
```

3. Run the example:
```bash
python main.py
```

## LLM Configuration

Configure the LLM by passing parameters directly:

```python
# Using default settings
llm = GeminiLLM()

# With custom settings
llm = GeminiLLM(
    model="gemini-1.5-pro",
    temperature=0.8,  # More creative responses
    top_p=0.9,
    max_output_tokens=4096
)
```

Available parameters (with defaults):
- model: "gemini-1.5-pro"
- temperature: 0.7 (0.0 to 1.0)
- top_p: 0.95 (0.0 to 1.0)
- top_k: 40
- max_output_tokens: 8192

## Creating Custom Agents

To create your own agents, inherit from `velocity.core.agent.Agent`:

```python
from velocity.core.agent import Agent
from velocity.llms.base import BaseLLM

class MyCustomAgent(Agent):
    def __init__(self, llm: BaseLLM):
        super().__init__(
            llm=llm,
            name="My Agent",
            description="Description of what your agent does"
        )
    
    async def my_custom_method(self, input: str) -> str:
        prompt = f"Your custom prompt with {input}"
        messages = [
            {"role": "system", "content": self.llm.get_system_prompt("Your Role")},
            {"role": "user", "content": prompt}
        ]
        return await self.llm.chat(messages)
```

## Adding Custom Tools

Create custom tools by inheriting from `velocity.core.tool.BaseTool`:

```python
from velocity.core.tool import BaseTool

class MyCustomTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="What your tool does"
        )
    
    async def execute(self, **kwargs) -> str:
        # Implement your tool logic here
        pass
```

## Extending the Example

Feel free to:
1. Add more specialized agents
2. Create custom tools for specific tasks
3. Modify the prompts and system messages
4. Integrate with external APIs or databases

## Best Practices

1. Keep agents focused on specific tasks
2. Use descriptive names and documentation
3. Handle errors gracefully
4. Use type hints for better code clarity
5. Follow async/await patterns consistently
6. Configure LLMs based on your needs:
   - Higher temperature (0.8-1.0) for creative tasks
   - Lower temperature (0.1-0.5) for focused, factual responses
   - Adjust max_output_tokens based on expected response length 