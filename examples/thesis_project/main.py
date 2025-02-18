import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path for development
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in os.environ.get("PYTHONPATH", "").split(os.pathsep):
    os.environ["PYTHONPATH"] = os.pathsep.join([project_root, os.environ.get("PYTHONPATH", "")])
    import sys
    sys.path.append(project_root)

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
