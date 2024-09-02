import os

from PyInstaller.utils.hooks import get_package_paths
from PyInstaller import log as logging

NETWORKX_DIR = get_package_paths("networkx")[1]

logger = logging.getLogger(__name__)

# Info
logger.info("networkx python package directory: %s" % NETWORKX_DIR)

# Hidden imports.
hiddenimports = []
# Excluded modules
excludedimports = []

# Include binaries
binaries = []

# Include datas
datas = [
    (os.path.join(NETWORKX_DIR, "generators"), "./networkx/generators"),
]

# Notify pyinstaller.spec code that this hook was executed
# and that it succeeded.
os.environ["PYINSTALLER_NETWORKX_HOOK_SUCCEEDED"] = "1"
