from setuptools import setup, find_packages

setup(
    name="blur_detection",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "requests>=2.25.0",
        "imutils>=0.5.4",
    ],
    entry_points={
        "console_scripts": [
            "detect-blur=blur_detection.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to detect and process blurry images",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/blur_detection",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)