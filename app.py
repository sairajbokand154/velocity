import asyncio
from velocityai.llms.gemini import GeminiLLM
from velocityai.agents.researcher import ResearchAgent
from velocityai.agents.writer import WriterAgent

async def main():
    # Initialize LLM
    import os
    llm = GeminiLLM(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Create agents
    researcher = ResearchAgent(llm)
    writer = WriterAgent(llm)
    
    # Define thesis topic
    topic = "The usecases of generative ai"
    
    # Research phase
    print("\n=== Research Phase ===")
    research_findings = ""
    async for chunk in researcher.research_topic(topic):
        research_findings += chunk
        print(chunk, end="", flush=True)
    
    print("\nInitial Research Findings:")
    print(research_findings)
    
    analysis = ""
    async for chunk in researcher.analyze_findings(research_findings):
        analysis += chunk
        print(chunk, end="", flush=True)
    
    print("\nResearch Analysis:")
    print(analysis)
    
    # Writing phase
    print("\n=== Writing Phase ===")
    outline = ""
    async for chunk in writer.outline_section(topic, research_findings):
        outline += chunk
        print(chunk, end="", flush=True)
    
    print("\nSection Outline:")
    print(outline)
    
    draft = ""
    async for chunk in writer.write_section(outline):
        draft += chunk
        print(chunk, end="", flush=True)
    
    print("\nFirst Draft:")
    print(draft)
    edited = ""
    async for chunk in writer.review_and_edit(draft):
        edited += chunk
        print(chunk, end="", flush=True)
    
    print("\nEdited Version:")
    print(edited)

if __name__ == "__main__":
    asyncio.run(main())
