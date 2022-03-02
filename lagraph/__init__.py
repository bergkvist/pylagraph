import sys
import os
from typing import List


def get_include() -> str:
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dirname, '../lagraph.include'))


def get_library_dir() -> str:
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dirname, '../lagraph.libs'))


def patch_build_ext(build_ext, library_dirs):
    class patched_build_ext(build_ext):
        def build_extension(self, ext) -> None:
            super().build_extension(ext)
            cmds = make_patch_rpath_commands(
                platform=sys.platform,
                ext_file=self.get_ext_fullpath(ext.name),
                library_dirs=library_dirs,
                build_lib=self.build_lib
            )
            for cmd in cmds:
                print(cmd)
                os.system(cmd)
    return patched_build_ext


def make_patch_rpath_commands(platform: str, ext_file: str, build_lib: str, library_dirs: List[str]) -> List[str]:
    if len(library_dirs) == 0:
        return []

    rpaths = [ os.path.relpath(os.path.join(build_lib, library_dir), os.path.dirname(ext_file))
               for library_dir in library_dirs ]

    if platform == 'linux':
        rpath_string = ':'.join([ f'$ORIGIN/{r}' for r in rpaths ])
        return [
            f"patchelf '{ext_file}' --set-rpath '{rpath_string}' --force-rpath"
        ]

    if platform == 'darwin':
        return [
            f"install_name_tool '{ext_file}' -add_rpath '@loader_path/{rpath}'"
            for rpath in rpaths
        ]

    raise Exception(f'Unsupported platform: {platform}')
