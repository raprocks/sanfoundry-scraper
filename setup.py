import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
INSTALL_REQUIRES = (HERE / "requirements.txt").read_text().split("\n")
README = (HERE / "README.md").read_text()

setup(
    name="sanfoundry_scraper",
    version="0.0.1",
    description="Python library for scrapping MCQs from Sanfoundry",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/raprocks/sanfoundry-scraper",
    entry_points={
        "console_scripts": ["sanfoundry_scraper=sanfoundry_scraper.main:scraper"]
    },
    packages=find_packages(exclude=["tests"]),
    install_requires=INSTALL_REQUIRES,
)
