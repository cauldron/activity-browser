from typing import Union, Callable, List, Any

from PySide2 import QtCore

from activity_browser import exchange_controller
from ..base import ABAction
from ...ui.icons import qicons
from ...bwutils import uncertainty


class ExchangeUncertaintyRemove(ABAction):
    """
    ABAction to clear the uncertainty of one or multiple exchanges.
    """
    icon = qicons.delete
    title = "Remove uncertainty/-ies"
    exchanges: List[Any]

    def __init__(self, exchanges: Union[List[Any], Callable], parent: QtCore.QObject):
        super().__init__(parent, exchanges=exchanges)

    def onTrigger(self, toggled):
        for exchange in self.exchanges:
            exchange_controller.edit_exchange(exchange, uncertainty.EMPTY_UNCERTAINTY)