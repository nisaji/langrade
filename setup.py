from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langrade",
    version="0.1.3",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for grading and retrieving documents based on relevance",  # noqa: E501
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/langrade",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "langchain>=0.3,<0.4",
        "langchain_core>=0.3,<0.4",
        "langchain_openai>=0.2,<0.3",
        "langchain_community>=0.3,<0.4",
        "openai>=1.2.0,<2.0.0",
        "chromadb>=0.5.3,<0.6.0",
        "tiktoken>=0.5.2,<0.6.0",
        "python-dotenv>=1.0.0,<2.0.0",
        "beautifulsoup4>=4.12.0,<5.0.0",
        "groq>=0.1.0,<1.0.0",
    ],
)
