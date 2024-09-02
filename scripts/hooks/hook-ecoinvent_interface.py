import os

from PyInstaller.utils.hooks import get_package_paths
from PyInstaller import log as logging

ECOINVENT_INTERFACE_DIR = get_package_paths("ecoinvent_interface")[1]

logger = logging.getLogger(__name__)

# Info
logger.info("ecoinvent_interface python package directory: %s" % ECOINVENT_INTERFACE_DIR)

# Hidden imports.
hiddenimports = []
# Excluded modules
excludedimports = []

# Include binaries
binaries = []

# Include datas
datas = [
    (os.path.join(ECOINVENT_INTERFACE_DIR, "data"), "./ecoinvent_interface/data"),
]

# Notify pyinstaller.spec code that this hook was executed
# and that it succeeded.
os.environ["PYINSTALLER_ECOINVENT_INTERFACE_HOOK_SUCCEEDED"] = "1"
