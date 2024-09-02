import os

from PyInstaller.utils.hooks import get_package_paths
from PyInstaller import log as logging

PYECOSPOLD_DIR = get_package_paths("pyecospold")[1]

logger = logging.getLogger(__name__)

# Info
logger.info("pyecospold python package directory: %s" % PYECOSPOLD_DIR)

# Hidden imports.
hiddenimports = []
# Excluded modules
excludedimports = []

# Include binaries
binaries = []

# Include datas
datas = [
    (os.path.join(PYECOSPOLD_DIR, "schemas"), "./pyecospold/schemas"),
]

# Notify pyinstaller.spec code that this hook was executed
# and that it succeeded.
os.environ["PYINSTALLER_PYECOSPOLD_HOOK_SUCCEEDED"] = "1"
