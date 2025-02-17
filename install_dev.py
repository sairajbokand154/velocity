import subprocess
import sys
from pathlib import Path

def install_dev():
    """Install package in development mode."""
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.absolute()
        
        # Install in development mode
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], cwd=project_root)
        
        print("✅ Development installation successful!")
        print("\nYou can now import the package as:")
        print("from velocityai.llms.gemini import GeminiLLM")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_dev() 