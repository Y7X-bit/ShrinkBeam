from setuptools import setup, find_packages

setup(
    name="LinkShortenerPro",
    version="1.0.0",
    author="Yugank (Y7X)",
    description="A glowing AMOLED link shortener GUI with QR, save, and copy features.",
    packages=find_packages(),
    install_requires=[
        "customtkinter",
        "pyshorteners",
        "pyperclip",
        "qrcode"
    ],
    entry_points={
        "console_scripts": [
            "linkshortener=main:LinkShortenerPro"
        ]
    },
    include_package_data=True,
)
