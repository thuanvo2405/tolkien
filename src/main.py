import os
import shutil


def main() -> None:
    copy_static_to_public()


def copy_static_to_public():
    public_path = "./public"
    if os.path.exists(os.path.join("./", "public")):
        shutil.rmtree(public_path)

    os.mkdir(public_path)
    copy_path_and_file("./static", "./public")


def copy_path_and_file(soucre_path, receive_path):
    list = os.listdir(soucre_path)
    for item in list:
        if os.path.isfile(os.path.join(soucre_path, item)):
            print(os.path.join(soucre_path, item))
            shutil.copy(
                os.path.join(soucre_path, item), os.path.join(receive_path, item)
            )
        else:
            os.mkdir(f"{receive_path}/{item}")
            copy_path_and_file(
                os.path.join(soucre_path, item), os.path.join(receive_path, item)
            )


main()
