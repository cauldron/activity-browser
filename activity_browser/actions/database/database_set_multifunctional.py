from multifunctional.database import SIMAPRO_ATTRIBUTES

from activity_browser import signals
from activity_browser.actions.base import ABAction, exception_dialogs
from activity_browser.logger import log
from activity_browser.mod import bw2data as bd
from activity_browser.ui.icons import qicons


class DatabaseSetMultifunctional(ABAction):
    """
    ABAction to set database backend to "multifunctional"
    """

    icon = qicons.settings
    text = "Set database to multifunctional"
    tool_tip = "Change database backend type to 'multifunctional'"

    @staticmethod
    @exception_dialogs
    def run(db_name: str):
        if bd.databases[db_name].get("backend") != "multifunctional":
            bd.databases[db_name]["backend"] = "multifunctional"
            bd.databases.flush()
