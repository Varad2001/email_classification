from setuptools import setup, find_packages

REQUIREMENTS_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."


def get_requirements() -> list[str] :
    with open(REQUIREMENTS_FILE_NAME) as f:
        requirements_list = f.readlines()

    requirements_list = [requirement.replace('\n', '') for requirement in requirements_list]

    if HYPHEN_E_DOT in requirements_list:
        requirements_list.remove(HYPHEN_E_DOT)
    
    return requirements_list


setup(
    name="email_classification",
    version='0.0.1',
    author='varad',
    author_email='varadkhonde@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements()
)

