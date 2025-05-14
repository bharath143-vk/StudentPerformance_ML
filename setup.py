from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    Returns a list of packages from requirements.txt,
    excluding the editable install line "-e ."
    '''
    requirements = []
    with open(file_path) as file:
        for line in file:
            req = line.strip()
            if req and req != HYPHEN_E_DOT:
                requirements.append(req)
    return requirements

setup(
    name="mlproject",
    version='1.1.0',
    author='Bharath',
    author_email='pbharathvk143@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
