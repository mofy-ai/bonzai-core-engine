from setuptools import setup, find_packages

setup(
    name='podplay_sanctuary',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-cors',
        'flask-socketio',
        'google-generativeai',
        'anthropic',
        'mem0ai',
        'python-dotenv',
        'scrapybara',
        'aiohttp'
    ],
)