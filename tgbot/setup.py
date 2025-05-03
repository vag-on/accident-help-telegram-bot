from setuptools import setup, find_namespace_packages

setup(
    name="accident_help_bot",
    version="1.0.0",
    packages=find_namespace_packages(include=['bot', 'bot.*']),
    package_dir={'': '.'},
    install_requires=[
        "aiogram==3.2.0",
        "django==5.0",
        "python-dotenv",
        "asgiref>=3.7.0",
    ],
    python_requires=">=3.8",
)
