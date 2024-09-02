import os
import re

from PyInstaller import log as logging
from PyInstaller.utils.hooks import get_package_paths

PLAYHOUSE_DIR = get_package_paths("playhouse")[1]

logger = logging.getLogger(__name__)


def get_datas():
    """
    Data files for playhouse

    DATAS are in format: tuple(full_path, dest_subdir).
    """
    ret = list()

    # Binaries, licenses and readmes in the playhouse/ directory
    for filename in os.listdir(PLAYHOUSE_DIR):
        #  binaries and datas
        if re.match('^.*\.(exe|dll|so|pak|dat|bin|txt)$', filename):
            logger.info("Include playhouse data: %s" % filename)
            ret.append((os.path.join(PLAYHOUSE_DIR, filename),
                        os.path.join("playhouse")))

    return ret


# Info
logger.info("playhouse python package directory: %s" % PLAYHOUSE_DIR)

# Hidden imports.
hiddenimports = []
# Excluded modules
excludedimports = []

# Include binaries
binaries = []

# Include datas
datas = get_datas()

# Notify pyinstaller.spec code that this hook was executed
# and that it succeeded.
os.environ["PYINSTALLER_PLAYHOUSE_HOOK_SUCCEEDED"] = "1"
