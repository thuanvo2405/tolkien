import os
import shutil
import sys

from generate_page import generate_pages_recursive

template_path = "./template.html"


def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public()
    generate_pages_recursive("./content", template_path, "./docs", basepath)


def copy_static_to_public():
    public_path = "./docs"
    if os.path.exists(os.path.join("./", "docs")):
        shutil.rmtree(public_path)

    os.makedirs(public_path, exist_ok=True)
    copy_path_and_file("./static", "./docs")


def copy_path_and_file(soucre_path, receive_path):
    list = os.listdir(soucre_path)

    for item in list:
        if os.path.isfile(os.path.join(soucre_path, item)):
            print(os.path.join(soucre_path, item))
            shutil.copy(
                os.path.join(soucre_path, item), os.path.join(receive_path, item)
            )
        else:
            os.makedirs(os.path.join(receive_path, item), exist_ok=True)
            copy_path_and_file(
                os.path.join(soucre_path, item), os.path.join(receive_path, item)
            )


main()
