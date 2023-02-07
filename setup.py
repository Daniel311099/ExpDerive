from setuptools import setup

setup(
    name='ExpDerive',
    version='0.1.0',    
    description='A Python package for deriving custom columns',
    url='https://github.com/Daniel311099/ExpDerive.git',
    author='Daniel Fisaha',
    author_email='DanielFisaha@Gmail.com',
    license='BSD 2-clause',
    packages=['ExpDerive'],
    install_requires=[
                      'numpy',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)