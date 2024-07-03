from setuptools import setup, find_packages

setup(
    name="langrade",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain_core",
        "langchain_openai",
        "langchain_community",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "langrade=langrade:main",
        ],
    },
)
