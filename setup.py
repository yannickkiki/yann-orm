from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    README = readme.read()

setup(
    name="yannorm",
    version="0.0.1",
    author="Yannick KIKI",
    author_email="seyive.kiki@gmail.com",
    description="Simple ORM",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yannickkiki/yann-orm",
    project_urls={
        "Bug Tracker": "https://github.com/yannickkiki/yann-orm/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "psycopg2-binary==2.8.6"
    ],
)
