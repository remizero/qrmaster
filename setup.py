from setuptools import setup, find_packages

setup (
  name="qrmaster",
  version="1.0.0",
  description="A flexible and customizable QR code generator",
  long_description=open("README.md", encoding="utf-8").read(),
  long_description_content_type="text/markdown",
  author="Filiberto Zaá Avila - remizero",
  author_email="filizaa@gmail.com",
  url="https://github.com/remizero/qrmaster",
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    "cairosvg",
    "fpdf",
    "jsonschema",
    "pillow",
    "pixels2svg",
    "segno",
    "svgutils",
    "svgwrite"
  ],
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Utilities",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
  ],
  python_requires='>=3.8',
)
