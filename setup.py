from setuptools import setup

# noinspection PyUnresolvedReferences
setup(
    author="David Navarro Alvarez",
    author_email="me@davengeo.com",
    description="message handler to write in cloud blob storage",
    url="https://github.com/davengeo/devops-tools",
    name="write-in-blob",
    version='0.0.1',
    packages=[
        'src',
        'src.setup_obj'
    ],
    install_requires=[
        'dependency-injector>=4.0,<5.0',
        'devopsprocessor_ifn==0.1.0',
        'messagehandler-ifn==0.1.0',
        'devops-tools-daven==0.0.14',
        'devops-processors==0.0.2',
        'requests',
        'kombu'
    ],
    package_data={
        'ini': ['app.ini']
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Systems Administration',
    ]
)
