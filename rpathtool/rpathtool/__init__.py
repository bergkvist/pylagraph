import os
import sys
from typing import List


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
    """Modify a compiled Python C extension/shared library to look for its dependencies at a relative path.
   
    We can't control the absolute path when running `pip install <package>` - which is why this is needed.
    
    PATH/CLI dependencies:
    - patchelf on Linux (might be possible to install with `pip install patchelf`)
    - install_name_tool on macOS (likely preinstalled)
    - Windows (other than WSL2) is currently not supported
    """
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