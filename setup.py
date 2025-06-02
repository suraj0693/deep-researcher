from setuptools import setup, find_packages

setup(
    name="deep-researcher",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "smolagents",
        "crawl4ai",
        "tavily-python",
        "litellm",
        "mlx",
        "huggingface-hub",
        "huggingface",
    ],
    python_requires=">=3.10",
    author="suraj0693",
    description="A deep research agent that can perform comprehensive web research",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/suraj0693/deep-researcher",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
) 