import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path for development
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in os.environ.get("PYTHONPATH", "").split(os.pathsep):
    os.environ["PYTHONPATH"] = os.pathsep.join([project_root, os.environ.get("PYTHONPATH", "")])

from velocityai.llms.gemini import GeminiLLM
from agents.researcher import ResearchAgent
from agents.writer import WriterAgent

# Load environment variables
load_dotenv()

async def main():
    # Initialize LLM with custom settings
    llm = GeminiLLM(
        model="gemini-1.5-pro",
        temperature=0.8,  # More creative responses
        top_p=0.9
    )
    
    # Create agents
    researcher = ResearchAgent(llm)
    writer = WriterAgent(llm)
    
    # Define thesis topic
    topic = "The Impact of Generative AI on Software Development"
    
    print(f"\nStarting thesis research and writing on: {topic}")
    print("=" * 50)
    
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
    