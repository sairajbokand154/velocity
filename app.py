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
    research_findings_task = asyncio.create_task(researcher.research_topic(topic))
    research_findings = await research_findings_task
    print("\nInitial Research Findings:")
    print(research_findings)
    
    analysis_task = asyncio.create_task(researcher.analyze_findings(research_findings))
    analysis = await analysis_task
    print("\nResearch Analysis:")
    print(analysis)
    
    # Writing phase
    print("\n=== Writing Phase ===")
    outline_task = asyncio.create_task(writer.outline_section(topic, research_findings))
    outline = await outline_task
    print("\nSection Outline:")
    print(outline)
    
    draft_task = asyncio.create_task(writer.write_section(outline))
    draft = await draft_task
    print("\nFirst Draft:")
    print(draft)
    
    edited_task = asyncio.create_task(writer.review_and_edit(draft))
    edited = await edited_task  
    print("\nEdited Version:")
    print(edited)

if __name__ == "__main__":
    asyncio.run(main())
