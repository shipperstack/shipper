import random


def get_distributed_download_url(request, build):
    if not build.is_mirrored():
        return get_main_download_url(request, build)

    available_servers = ["main", *build.get_downloadable_mirrors()]

    selected_server = random.choice(available_servers)
    match selected_server:
        case "main":
            return get_main_download_url(request, build)
        case _:
            return selected_server.get_download_url(build)


def get_main_download_url(request, build):
    return f"https://{request.get_host()}{build.zip_file.url}"
