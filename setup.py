from setuptools import setup
import os

def files_in(dir: str):
    return [ os.path.join(dir, f) for f in os.listdir(dir) ]

setup(
    name='lagraph',
    version='3.3.3',
    description='Python wheel containing prebuild GraphBLAS/LAGraph libraries/header files.',
    author='Tobias Bergkvist <tobias@bergkv.ist>',
    packages=['lagraph'],
    data_files=[
        ('../../lagraph.libs', files_in('./lagraph.libs')),
        ('../../lagraph.include', files_in('./lagraph.include'))
    ],
    zip_safe=False,
)
