import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

setuptools.setup(
    name="user-authentication-jr",
    version="0.0.4",
    author="John Rei Enriquez",
    author_email="johnrei.enriquez@gmail.com",
    description="A django app with token based authentication for both Session and API Token",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrbenriquez/user-authentication-jr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)
