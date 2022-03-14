import os
from typing import List


def get_include() -> str:
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dirname, '../lagraph.include'))


def get_library_dir() -> str:
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dirname, '../lagraph.libs'))


def get_libraries() -> List[str]:
    """Get list of libraries which can be given to "libraries" in setuptools.
    linux:  [ ":liblagraph.so.0.1.0",    ":libgraphblas.so.3.3.3"    ]
    darwin: [ ":liblagraph.0.1.0.dylib", ":libgraphblas.3.3.3.dylib" ] etc.
    """
    return [ f':{library}' for library in os.listdir(get_library_dir()) ]
