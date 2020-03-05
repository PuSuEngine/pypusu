from distutils.core import setup

# Convert README.md to reStructuredText
try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
    print("Converted README.md into reStructuredText")
except(IOError, ImportError, RuntimeError):
    try:
        long_description = open('README.md').read()
    except IOError:
        long_description = None

setup(
    name='pypusu',
    packages=['pypusu'],  # this must be the same as the name above
    version='1.0.6',
    description='Python client for PuSuEngine',
    long_description=long_description,
    author='Janne Enberg',
    author_email='janne.enberg@lietu.net',
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*,<4",
    url='https://github.com/PuSuEngine/pypusu',
    download_url='https://github.com/PuSuEngine/pypusu/tarball/v1.0.6',
    keywords=['pubsub', 'publisher', 'subscriber', 'messaging'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
