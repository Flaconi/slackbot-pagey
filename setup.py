"""Pip configuration."""
# https://github.com/pypa/sampleproject/blob/main/setup.py

from setuptools import setup

with open("README.md", "r") as fp:
    long_description = fp.read()

with open("requirements.txt", "r") as fp:
    requirements = fp.read()

setup(
    name="pagey",
    version="0.1.0",
    packages=[
        "pagey",
        "pagey.pagerduty",
        "pagey.slack",
    ],
    entry_points={
        "console_scripts": [
            # cmd = package[.module]:func
            "pagey=pagey:main",
        ],
    },
    install_requires=requirements,
    description="Pagey is a Pagerduty slack bot.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["pagerduty", "slack"],
    author="cytopia",
    author_email="cytopia@everythingcli.org",
    url="https://github.com/Flaconi/slackbot-pagey",
    project_urls={
        "Source Code": "https://github.com/Flaconi/slackbot-pagey",
        "Bug Tracker": "https://github.com/Flaconi/slackbot-pagey",
    },
    python_requires=">=3.6",
    classifiers=[
        # https://pypi.org/classifiers/
        #
        # How mature is this project
        "Development Status :: 3 - Alpha",
        # How does it run
        "Environment :: Console",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        # License
        "License :: OSI Approved :: MIT License",
        # Where does it run
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # Project topics
        "Topic :: Internet",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        # Typed
        "Typing :: Typed",
    ],
)
