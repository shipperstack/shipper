import os

from django.conf import settings


# Delete build artifact and MD5 hash
def delete_artifact(codename, file_path):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, codename, file_path))
        os.remove("{}.md5".format(os.path.join(settings.MEDIA_ROOT, codename, file_path)))
    except OSError:
        pass
