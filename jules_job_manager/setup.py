from setuptools import setup, find_packages

setup(
    name="jules-job-manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich",
        "python-dotenv",
    ],
    description="Python tools for managing Google Jules tasks",
    author="Windsurf Engineering",
)
