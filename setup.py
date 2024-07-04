from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    import setuptools

    setup: Callable[..., None] = setuptools.setup
    find_packages: Callable[..., List[str]] = setuptools.find_packages

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setup(
        name="langrade",
        version="0.1.0",
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
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
        ],
        python_requires=">=3.7",
        install_requires=[
            "langchain",
            "langchain_core",
            "langchain_openai",
            "langchain_community",
            "python-dotenv",
            "pymongo",
        ],
        entry_points={
            "console_scripts": [
                "langrade=langrade.cli:main",
            ],
        },
    )
except Exception as e:
    print(f"An error occurred: {e}")
