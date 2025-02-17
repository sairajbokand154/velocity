from velocityai.core.agent import Agent
from velocityai.llms.base import BaseLLM

class ResearchAgent(Agent):
    """Example agent specialized in research and information gathering."""
    
    def __init__(self, llm: BaseLLM):
        super().__init__(
            llm=llm,
            name="Research Assistant",
            description="Specialized in gathering and analyzing information for thesis research"
        )
        
    async def research_topic(self, topic: str) -> str:
        """Research a specific topic and provide findings."""
        prompt = f"""As a research assistant, please analyze the following topic:
{topic}

Please provide:
1. Key aspects to investigate
2. Main research questions
3. Potential sources of information
4. Initial hypotheses

Structure your response clearly and concisely."""
        
        messages = [
            {"role": "system", "content": self.llm.get_system_prompt("Research Assistant")},
            {"role": "user", "content": prompt}
        ]
        
        return await self.llm.chat(messages)
    
    async def analyze_findings(self, findings: str) -> str:
        """Analyze research findings and provide insights."""
        prompt = f"""Please analyze these research findings:
{findings}

Provide:
1. Key insights
2. Patterns or trends
3. Areas needing further investigation
4. Potential implications"""
        
        messages = [
            {"role": "system", "content": self.llm.get_system_prompt("Research Analyst")},
            {"role": "user", "content": prompt}
        ]
        
        return await self.llm.chat(messages) 