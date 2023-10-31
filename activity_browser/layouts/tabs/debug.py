import sys

from PySide2 import QtCore, QtWidgets

from activity_browser.layouts.base import ABTab
from activity_browser.signals import signals
from activity_browser.ui.style import header
from activity_browser.ui.utils import StdRedirector


class DebugTab(ABTab):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.log = QtWidgets.QPlainTextEdit(self)
        sys.stdout = StdRedirector(self.log, sys.stdout)
        sys.stderr = StdRedirector(self.log, sys.stderr)

        self.debug_display = QtWidgets.QVBoxLayout()
        self.title = header("Program debugger output:")

        self.debug_display.addWidget(self.title)
        self.debug_display.addWidget(self.log)

        self.setLayout(self.debug_display)
        self.setVisible(False)

        signals.log.connect(self.write_log_message)

    @QtCore.Slot(name="writeLogMessage")
    def write_log_message(self, msg: str):
        self.log.appendPlainText(msg)
        self.log.centerCursor()
