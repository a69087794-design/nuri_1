from setuptools import setup, find_packages

setup(
    name="NURI",
    version="1.0.0",
    description="Neyronli Universal Robot Intellekti",
    author="horaphile",
    packages=find_packages(),
    install_requires=[
        'aiogram==3.28.2',
        'aiofiles==25.1.0',
        'aiohttp==3.13.5',
        'groq==1.4.0',
        'pydantic==2.13.4',
        'PyQt5==5.15.11',
        'python-dotenv==1.2.2',
        'PyAutoGUI==0.9.54',
        'edge-tts==7.2.8',
        'yt-dlp==2024.12.6',
        'feedparser==6.0.10',
    ],
    python_requires='>=3.9',
)
