from setuptools import setup, find_packages

setup(
    name='user-management-app',
    version='1.0.0',
    description='A comprehensive user management application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/user-management-app',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt6>=6.6.1',
        'PyInstaller>=6.3.0',
        'pyyaml>=6.0.1',
    ],
    extras_require={
        'dev': [
            'pytest>=8.0.2',
            'flake8>=7.0.0',
        ],
        'packaging': [
            'py2app>=0.28.6',
            'dmgbuild>=1.6.1',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'user-management-app=src.main:main',
        ],
    },
)