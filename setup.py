import setuptools

setuptools.setup(
    name='faas-exp',
    version='0.1.0',
    description='Serverless OpenFaas Use Case Testing Tool',
    author='Mohammed AbuAisha',
    author_email='mabuaisha@outlook.com',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['faas-exp = faas_exp:main']},
    install_requires=[
        'requests==2.23.0',
        'click==7.1.1',
        'ruamel.yaml==0.16.10',
        'jinja2==2.11.2'
    ])
