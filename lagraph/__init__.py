import sys
import os


def get_include():
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dirname, '../lagraph.include'))


def get_library_dir():
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dirname, '../lagraph.libs'))


def patch_build_ext(build_ext):    
    class patched_build_ext(build_ext):
        def build_extension(self, ext) -> None:
            super().build_extension(ext)
            cmd = make_patch_rpath_command(platform=sys.platform,
                                           ext_file=self.get_ext_fullpath(ext.name),
                                           library_dir='lagraph.libs',
                                           build_lib=self.build_lib)
            print(cmd)
            os.system(cmd)
    return patched_build_ext


def make_patch_rpath_command(platform: str, ext_file: str, build_lib: str, library_dir: str) -> str:
    relpath = os.path.relpath(os.path.join(build_lib, library_dir), os.path.dirname(ext_file))
    if platform == 'linux':
        return f"patchelf '{ext_file}' --set-rpath '$ORIGIN/{relpath}' --force-rpath"
    if platform == 'darwin':
        return f"install_name_tool '{ext_file}' -add_rpath '@loader_path/{relpath}'"
    raise Exception(f'Unsupported platform: {platform}')
