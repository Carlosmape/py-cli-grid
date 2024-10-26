import setuptools

setuptools.setup(
    name="py-cli-grid",
    version="0.0.1",
    author="Carlos G. Martín Pérez",
    author_email="cagrmape@gmail.com",
    description="Package to manage CLI as a grid",
    long_description="It allows to divide console in several boxes and print text in the grid",
    long_description_content_type="text/markdown",
    url="https://github.com/Carlosmape/py-cli-grid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.10"
)
