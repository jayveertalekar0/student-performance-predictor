from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """Read requirements from file"""
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements if req.strip()]
    return requirements

setup(
    name="student-performance-predictor",
    version="1.0.0",
    author="Jayveer Talekar",
    author_email="jayveertalekar0@gmail.com",
    description="ML web app to predict student math scores",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jayveertalekar0/student-performance-predictor",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
)