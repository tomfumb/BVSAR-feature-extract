from setuptools import find_namespace_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="feature_extract",
    version="0.1.0",
    description="Feature Extract for SAR data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=False,
    zip_safe=True,
    install_requires=["pydantic==1.9.2", "boto3==1.24.80"],
    extras_require={
        "test": [
            "pytest==7.1.2",
            "requests==2.28.1",
        ],
    },
)
