import os
import shutil


def clone_contents(src: str, dst: str) -> None:
    script_dir = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))
    src = os.path.join(project_root, src)
    dst = os.path.join(project_root, dst)

    if not os.path.isdir(src):
        raise ValueError("src does not lead to an existing directory.")

    if os.path.isdir(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)
    _clone_contents(src, dst)


def _clone_contents(src: str, dst: str) -> None:
    for name in os.listdir(src):
        src_name = os.path.join(src, name)
        dst_name = os.path.join(dst, name)
        if os.path.isfile(src_name):
            shutil.copy(src_name, dst_name)
            print(src_name)
        else:
            os.mkdir(dst_name)
            _clone_contents(src_name, dst_name)
