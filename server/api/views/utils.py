import random

from constance import config


def get_distributed_download_url(request, build):
    if not build.is_mirrored():
        return get_main_download_url(request, build)

    available_servers = ["main", *build.get_downloadable_mirrors()]

    if config.SHIPPER_DOWNLOADS_DISABLE_MAIN_SERVER:
        available_servers.remove("main")

    selected_server = random.choice(available_servers)
    if selected_server == "main":
        return get_main_download_url(request, build)
    else:
        return selected_server.get_download_url(build)


def get_main_download_url(request, build):
    return f"https://{request.get_host()}{build.zip_file.url}"
