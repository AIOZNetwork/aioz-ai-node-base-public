import os
from setuptools import find_packages, setup


def read_version(fname="aioz_ainode_adapter/version.py"):
    exec(compile(open(fname, encoding="utf-8").read(), fname, "exec"))
    return locals()["__version__"]


setup(
    name="aioz-ainode-adapter",
    py_modules=["aioz_ainode_adapter"],
    version=read_version(),
    description="The module supports building AI models to integrate into the AIOZ-AI-NODE system",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    python_requires=">=3.10",
    author="AIOZ AI",
    license="MIT",
    packages=find_packages(exclude=["tests*", "example*", "my_ai_lib"]),
    install_requires=[
        "pydantic==2.4.2"
    ]
)
