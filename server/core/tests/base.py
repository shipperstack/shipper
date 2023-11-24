from core.models import Build, Device, Variant

DEVICE_BUILD_PAIRING = {}


def mock_setup():
    mock_devices_setup()
    mock_variants_setup()
    mock_builds_setup()


def mock_devices_setup():
    def create_device_pairing(codename):
        DEVICE_BUILD_PAIRING[codename] = {}

    Device.objects.create(
        name="Nexus 5X",
        codename="bullhead",
        manufacturer="LG",
        photo="https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg",
        status=True,
    )
    create_device_pairing("bullhead")

    Device.objects.create(
        name="Nexus 6P",
        codename="angler",
        manufacturer="Huawei",
        photo="https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg",
        status=False,
    )
    create_device_pairing("angler")

    Device.objects.create(
        name="Galaxy S8+",
        codename="dream2lte",
        manufacturer="Samsung",
        status=True,
    )
    create_device_pairing("dream2lte")

    Device.objects.create(name="x86", codename="x86", manufacturer="x86", status=True)
    create_device_pairing("x86")

    # noinspection SpellCheckingInspection
    Device.objects.create(
        name="No Builds",
        codename="nobuild",
        manufacturer="NoBuilds",
        status=False,
    )
    create_device_pairing("nobuild")


def mock_variants_setup():
    # Right now we have to check if there are duplicates as the old deprecated variant
    # configuration option exists. In the future, don't check for this.
    # TODO: remove the checks once the configuration option is gone
    # get_or_create -> get
    Variant.objects.get_or_create(codename="gapps", description="GApps")
    Variant.objects.get_or_create(codename="vanilla", description="Vanilla (no GApps)")
    Variant.objects.get_or_create(codename="foss", description="FOSS")
    Variant.objects.get_or_create(
        codename="goapps", description="GoApps (Android Go Edition GApps)"
    )


def mock_builds_setup():
    from datetime import date

    def increment_device_build_variant_pairing(codename, variant):
        if variant in DEVICE_BUILD_PAIRING[codename]:
            DEVICE_BUILD_PAIRING[codename][variant] += 1
        else:
            DEVICE_BUILD_PAIRING[codename][variant] = 1

    Build.objects.create(
        device=Device.objects.get(codename="bullhead"),
        file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608",
        size=857483855,
        version="v14",
        md5sum="d8e8fca2dc0f896fd7cb4cb0031ba249",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant=Variant.objects.get(codename="gapps"),
        build_date=date(2020, 6, 8),
        zip_file="bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip",
    )
    increment_device_build_variant_pairing("bullhead", "gapps")

    Build.objects.create(
        device=Device.objects.get(codename="dream2lte"),
        file_name="Bliss-v14-dream2lte-OFFICIAL-gapps-20200609",
        size=857483995,
        version="v14",
        md5sum="d8e8fca2dc0f896fd7cb4cb0031ba249",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant=Variant.objects.get(codename="gapps"),
        build_date=date(2020, 6, 9),
        zip_file="dream2lte/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip",
    )
    increment_device_build_variant_pairing("dream2lte", "gapps")

    Build.objects.create(
        device=Device.objects.get(codename="angler"),
        file_name="Bliss-v14-angler-OFFICIAL-vanilla-20200608",
        size=857483855,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        md5sum="d8e8fca2dc0f896fd7cb4cb0031ba249",
        variant=Variant.objects.get(codename="vanilla"),
        build_date=date(2020, 6, 8),
        zip_file="angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip",
    )
    increment_device_build_variant_pairing("angler", "vanilla")
