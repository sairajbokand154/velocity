from velocityai.core.agent import Agent
from velocityai.llms.base import BaseLLM
import hashlib

class WriterAgent(Agent):
    """Example agent specialized in academic writing and thesis composition."""
    
    def __init__(self, llm: BaseLLM):
        super().__init__(
            llm=llm,
            name="Academic Writer",
            description="Specialized in academic writing and thesis composition"
        )
        self.cache = {}
    
    def _generate_cache_key(self, *args) -> str:
        """Generate a unique cache key based on input arguments."""
        return hashlib.md5("".join(args).encode()).hexdigest()
    
    async def outline_section(self, topic: str, research_findings: str) -> str:
        """Create an outline for a thesis section."""
        cache_key = self._generate_cache_key(topic, research_findings)
        if cache_key in self.cache:
            return self.cache[cache_key]
        prompt = f"""Based on the following research findings:
{research_findings}

Please create a detailed outline for the thesis section on: {topic}

Include:
1. Main section headings
2. Key points under each heading
3. Potential subsections
4. Important citations needed"""
        
        messages = [
            {"role": "system", "content": self.llm.get_system_prompt("Academic Writer")},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm.chat(messages)
        self.cache[cache_key] = response
        return response
    
    async def write_section(self, outline: str) -> str:
        """Write a thesis section based on an outline."""
        cache_key = self._generate_cache_key(outline)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        prompt = f"""Using this outline:
{outline}

Please write a draft of this thesis section. Focus on:
1. Clear academic writing style
2. Logical flow of ideas
3. Proper paragraph structure
4. Integration of research findings"""
        
        messages = [
            {"role": "system", "content": self.llm.get_system_prompt("Academic Writer")},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm.chat(messages)
        self.cache[cache_key] = response
        return response
    
    async def review_and_edit(self, content: str) -> str:
        """Review and edit written content."""
        cache_key = self._generate_cache_key(content)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        prompt = f"""Please review and improve this academic content:
{content}

Focus on:
1. Academic writing standards
2. Clarity and coherence
3. Grammar and style
4. Suggestions for improvement"""
        
        messages = [
            {"role": "system", "content": self.llm.get_system_prompt("Editor")},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm.chat(messages)
        self.cache[cache_key] = response
        return response