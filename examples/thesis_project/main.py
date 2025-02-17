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