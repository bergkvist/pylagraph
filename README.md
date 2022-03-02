![](./header.png)

# LAGraph/GraphBLAS in a PyPi-wheel
Multiplatform prebuilt wheels with GraphBLAS/LAGraph shared libraries.

## Installation
```sh
pip install lagraph
```

## Why?
The idea of this package is to make it easier for other developers to create Python bindings for GraphBLAS/LAGraph without needing to set up their own build system for GraphBLAS/LAGraph.

Since this package doesn't contain any Python C-bindings, it doesn't depend on a specific Python ABI version - and only needs to be published once per platform and desired GraphBLAS/LAGraph version.

## Supported platforms
- Linux
- macOS
- Windows (through WSL2)

## Usage

Assuming you want to write a Python C extension or similar

```py
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import lagraph

setup(
  # ...
  ext_modules=[
    Extension(
      name='mylib.cextension',
      sources=['mylib/cextension.c'],
      libraries=[*lagraph.get_libraries()],
      include_dirs=[lagraph.get_include()],
      library_dirs=[lagraph.get_library_dir()]
    ),
    # ...
  ],
  cmdclass={'build_ext': lagraph.patch_build_ext(build_ext, [lagraph.get_library_dir()])}
)
```

If you want to build inplace, make sure you use --build_lib=.

### Why do we need to patch build_ext?
In order to allow a Python C extension to find `libgraphblas.so.3.3.3` at a relative path, we need to use something called `RPATH`. This is implemented slightly differently on macOS and Linux, but with some tweaking we can get the same behaviour on both platforms.
The binary extension modules need to be patched after being built, which is the reason for patching build_ext, so that this can be added right after the compilation.

#### On Linux, [`patchelf`](https://github.com/NixOS/patchelf) (which is available on PyPi) is used.
```
patchelf './mylib/cextension.cpython-38-x86_64-linux-gnu.so' \
  --set-rpath '$ORIGIN/../lagraph.libs' \
  --force-rpath
```

#### On macOS, [`install_name_tool`](https://www.unix.com/man-page/osx/1/install_name_tool/) (built into macOS) is used.
```
install_name_tool './mylib/cextension.cpython-38-darwin.so' \
  --add_rpath '@loader_path/../lagraph.libs'
```
