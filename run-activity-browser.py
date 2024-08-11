# -*- coding: utf-8 -*-
import importlib
import os
import sys

from PySide2.QtCore import QCoreApplication, QObject, QSysInfo, Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QSplashScreen


class ABApplication(QApplication):
    """Matches the ABApplication definied in application.py"""

    _main_window = None
    _controllers = None

    @property
    def main_window(self) -> QObject:
        """Returns the main_window widget of the Activity Browser"""
        if self._main_window:
            return self._main_window
        raise Exception(
            "main_window not yet initialized, did you try to access it during startup?"
        )

    @main_window.setter
    def main_window(self, widget):
        self._main_window = widget

    def show(self):
        self.main_window.showMaximized()

    def close(self):
        for child in self.children():
            if hasattr(child, "close"):
                child.close()

    def deleteLater(self):
        self.main_window.deleteLater()


if QSysInfo.productType() == "osx":
    # https://bugreports.qt.io/browse/QTBUG-87014
    # https://bugreports.qt.io/browse/QTBUG-85546
    # https://github.com/mapeditor/tiled/issues/2845
    # https://doc.qt.io/qt-5/qoperatingsystemversion.html#MacOSBigSur-var
    supported = {"10.10", "10.11", "10.12", "10.13", "10.14", "10.15"}
    if QSysInfo.productVersion() not in supported:
        os.environ["QT_MAC_WANTS_LAYER"] = "1"
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"

if QSysInfo.productType() in ["arch", "nixos"]:
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)


def show_splash_screen():
    application = ABApplication(sys.argv)
    # Create the splash screen
    splash = QSplashScreen(
        QPixmap(
            os.path.join(
                os.path.dirname(importlib.util.find_spec("activity_browser").origin),
                "static",
                "icons",
                "main",
                "activitybrowser.png",
            )
        ).scaledToHeight(480)
    )
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    splash.showMessage(
        "<h1>Loading, please wait...<h1/>", Qt.AlignBottom | Qt.AlignCenter, Qt.white
    )

    # Show the splash screen
    splash.show()

    application.processEvents()

    # from activity_browser import run_activity_browser
    activity_browser = importlib.import_module("activity_browser")
    application.processEvents()
    activity_browser.run_activity_browser(splash)


if __name__ == "__main__":
    # Useful if you want to run some interactive commands using the built
    # binary and test out dependencies to ensure that they work properly.
    # import code
    # code.interact()

    show_splash_screen()
