from setuptools import setup, find_packages

setup(
    name="velocityai",
    version="0.1.0",
    description="A modular AI Agent Framework",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/velocityai",
    packages=find_packages(),
    install_requires=[
        "google-generativeai>=0.3.0",
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="ai, agents, llm, gemini, framework",
) 