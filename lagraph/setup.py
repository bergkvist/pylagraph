from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools import setup
import os

class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False
    def get_tag(self):
        python, abi, platform =  super().get_tag()
        python, abi = 'py3', 'none'
        return python, abi, platform

def files_in(dir: str):
    return [ os.path.join(dir, f) for f in os.listdir(dir) ]

setup(
    packages=['lagraph'],
    data_files=[
        ('../../lagraph.libs', files_in('./lagraph.libs')),
        ('../../lagraph.include', files_in('./lagraph.include'))
    ],
    zip_safe=False,
    cmdclass={'bdist_wheel': bdist_wheel}
)
