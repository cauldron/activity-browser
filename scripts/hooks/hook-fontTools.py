import glob
import os
import re

from PyInstaller.utils.hooks import get_package_paths
from PyInstaller import log as logging

FONT_TOOLS_DIR = get_package_paths("fontTools")[1]

logger = logging.getLogger(__name__)

# Info
logger.info("fontTools python package directory: %s" % FONT_TOOLS_DIR)


def get_datas():
    """
    Data files for fontTools

    DATAS are in format: tuple(full_path, dest_subdir).
    """
    ret = list()

    # Binaries, licenses and readmes in the fontTools/ directory
    for filename in glob.glob(os.path.join(FONT_TOOLS_DIR, "*")):
        #  binaries and datas
        if re.match('^.*\.(exe|dll|so|pak|dat|bin|txt)$', filename):
            logger.info("Include playhouse data: %s" % filename)
            ret.append((os.path.join(FONT_TOOLS_DIR, filename),
                        os.path.join("fontTools", os.path.dirname(filename).removeprefix(FONT_TOOLS_DIR))))

    return ret


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
os.environ["PYINSTALLER_FONTTOOLS_HOOK_SUCCEEDED"] = "1"
