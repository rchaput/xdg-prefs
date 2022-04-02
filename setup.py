import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='XDG-Prefs',
    version='0.1',

    packages=['xdgprefs', 'xdgprefs.core', 'xdgprefs.gui'],
    install_requires=['PySide2'],

    entry_points={
        'gui_scripts': [
            'xdg-prefs = xdgprefs.__main__:main'
        ]
    },


    author='Remy Chaput',
    author_email='rchaput.pro@gmail.com',
    description='A GUI program to view and change your default programs\' '
                'preferences (which program should open which type of file), '
                'using the XDG Specifications',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',

    license='Apache',
    keywords='GUI MIME preferences XDG',
    platforms=['GNU/Linux'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ]
)
