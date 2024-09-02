import os

from PyInstaller.utils.hooks import get_package_paths
from PyInstaller import log as logging

BW2IO_DIR = get_package_paths("bw2io")[1]

logger = logging.getLogger(__name__)

# Info
logger.info("bw2io python package directory: %s" % BW2IO_DIR)

# Hidden imports.
hiddenimports = []
# Excluded modules
excludedimports = []

# Include binaries
binaries = []

# Include datas
datas = [
    (os.path.join(BW2IO_DIR, "data"), "./bw2io/data"),
]

# Notify pyinstaller.spec code that this hook was executed
# and that it succeeded.
os.environ["PYINSTALLER_BW2IO_HOOK_SUCCEEDED"] = "1"
