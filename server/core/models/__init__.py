from auditlog.registry import auditlog

from .device import Device
from .variant import Variant
from .build import Build, BuildFeature
from .mirror_server import MirrorServer
from .x86type import X86Type
from .statistics import Statistics

__all__ = [
    "Device",
    "Variant",
    "Build",
    "BuildFeature",
    "MirrorServer",
    "X86Type",
    "Statistics",
]


# Register all models to audit log
auditlog.register(Device)
auditlog.register(MirrorServer)
auditlog.register(Build)
auditlog.register(BuildFeature)
