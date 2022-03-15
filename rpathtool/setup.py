from setuptools import setup

setup(
  packages=['rpathtool'],
  install_requires=[
    'patchelf; sys_platform == "linux"'
    # install_name_tool on macOS (https://www.unix.com/man-page/osx/1/install_name_tool/)
  ]
)