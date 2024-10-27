from setuptools import setup, find_packages

setup(
    name='manim-Astronomy',
    version='0.0.2',
    author='Hassam ul Haq',
    author_email='hassamrajpoot100@gmail.com',
    description='A Manim extension for creating astronomical visualizations',
    long_description=open('README.md',encoding="utf8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hassamrajpoot/manim-Astronomy',
    packages=find_packages(),
    install_requires=[
        'manim',
        'numpy',
        'vedo'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
