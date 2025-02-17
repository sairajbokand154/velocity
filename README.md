# VelocityAI

A modular AI Agent Framework for building intelligent applications with LLMs.

## Installation

### For Users

Once published:
```bash
pip install velocityai
```

### For Developers

1. Clone the repository:
```bash
git clone https://github.com/yourusername/velocityai.git
cd velocityai
```

2. Install in development mode:
```bash
# Option 1: Using pip
pip install -e .

# Option 2: Using the installation script
python install_dev.py
```

## Quick Start

```python
from velocityai.llms.gemini import GeminiLLM

# Initialize LLM
llm = GeminiLLM(
    model="gemini-1.5-pro",
    temperature=0.8
)

# Use with agents
from velocityai.core.agent import Agent

class MyAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            name="My Agent",
            description="Custom agent for specific tasks"
        )
```

## Examples

Check out the `examples/` directory for complete examples:
- `thesis_project/`: AI agents for research and academic writing
- More examples coming soon!

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 