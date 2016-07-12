from distutils.core import setup

# Convert README.md to reStructuredText
try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
    print("Converted README.md into reStructuredText")
except(IOError, ImportError):
    long_description = open('README.md').read()
except(IOError, ImportError):
    long_description = None

setup(
    name='pypusu',
    packages=['pypusu'],  # this must be the same as the name above
    version='1.0.4',
    description='Python client for PuSuEngine',
    long_description=long_description,
    author='Janne Enberg',
    author_email='janne.enberg@lietu.net',
    url='https://github.com/PuSuEngine/pypusu',
    download_url='https://github.com/PuSuEngine/pypusu/tarball/v1.0.4',
    keywords=['pubsub', 'publisher', 'subscriber', 'messaging'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
