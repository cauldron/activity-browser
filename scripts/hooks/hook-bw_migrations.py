import os

from PyInstaller.utils.hooks import get_package_paths
from PyInstaller import log as logging

BW_MIGRATIONS_DIR = get_package_paths("bw_migrations")[1]

logger = logging.getLogger(__name__)

# Info
logger.info("bw_migrations python package directory: %s" % BW_MIGRATIONS_DIR)

# Hidden imports.
hiddenimports = []
# Excluded modules
excludedimports = []

# Include binaries
binaries = []

# Include datas
datas = [
    (os.path.join(BW_MIGRATIONS_DIR, "data"), "./bw_migrations/data"),
]

# Notify pyinstaller.spec code that this hook was executed
# and that it succeeded.
os.environ["PYINSTALLER_BW_MIGRATIONS_HOOK_SUCCEEDED"] = "1"
