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
    research_findings = await researcher.research_topic(topic)
    print("\nInitial Research Findings:")
    print(research_findings)
    
    analysis = await researcher.analyze_findings(research_findings)
    print("\nResearch Analysis:")
    print(analysis)
    
    # Writing phase
    print("\n=== Writing Phase ===")
    outline = await writer.outline_section(topic, research_findings)
    print("\nSection Outline:")
    print(outline)
    
    draft = await writer.write_section(outline)
    print("\nFirst Draft:")
    print(draft)
    
    edited = await writer.review_and_edit(draft)
    print("\nEdited Version:")
    print(edited)

if __name__ == "__main__":
    asyncio.run(main())

