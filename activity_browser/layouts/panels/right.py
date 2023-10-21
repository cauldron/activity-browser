# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import brightway2 as bw
from bw2data import get_node
from PySide2.QtWidgets import QVBoxLayout

from activity_browser.logger import ABHandler

from ...bwutils.commontasks import get_activity_name
from ...signals import signals
from ...ui.web import GraphNavigatorWidget, RestrictedWebViewWidget
from ..tabs import (
    ActivitiesTab,
    CharacterizationFactorsTab,
    LCAResultsTab,
    LCASetupTab,
    ParametersTab,
)
from .panel import ABTab

logger = logging.getLogger("ab_logs")
log = ABHandler.setup_with_logger(logger, __name__)


class RightPanel(ABTab):
    side = "right"

    def __init__(self, *args):
        super(RightPanel, self).__init__(*args)
        package_dir = Path(__file__).resolve().parents[2]
        html_file = str(package_dir.joinpath("static", "startscreen", "welcome.html"))
        self.tabs = {
            "Welcome": RestrictedWebViewWidget(html_file=html_file),
            "Characterization Factors": CharacterizationFactorsTab(self),
            "Activity Details": ActivitiesTab(self),
            "LCA Setup": LCASetupTab(self),
            "Graph Explorer": GraphExplorerTab(self),
            "LCA results": LCAResultsTab(self),
            "Parameters": ParametersTab(self),
        }
        self.tab_order = {}

        for tab_name, tab in self.tabs.items():
            self.tab_order[tab_name] = self.addTab(tab, tab_name)

        # tabs hidden at start
        for tab_name in [
            "Activity Details",
            "Characterization Factors",
            "Graph Explorer",
            "LCA results",
        ]:
            self.hide_tab(tab_name)

    def show_tab(self, tab_name):
        """Re-inserts tab at the initial location.

        This avoids constantly re-ordering the mayor tabs.
        """
        if tab_name in self.tabs:
            tab = self.tabs[tab_name]
            log.info("+showing tab:", tab_name)
            tab.setVisible(True)
            self.insertTab(self.tab_order[tab_name], tab, tab_name)
            self.select_tab(tab)


class GraphExplorerTab(ABTab):
    def __init__(self, parent):
        super(GraphExplorerTab, self).__init__(parent)

        self.setMovable(True)
        self.setTabsClosable(True)
        # self.setTabShape(1)  # Triangular-shaped Tabs

        # Generate layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.connect_signals()

    def connect_signals(self):
        self.tabCloseRequested.connect(self.close_tab)
        signals.project_selected.connect(self.close_all)
        signals.open_activity_graph_tab.connect(self.add_tab)

    def add_tab(self, key, select=True):
        """Opens new tab or focuses on already open one."""
        if key not in self.tabs:
            log.info("adding graph tab")
            new_tab = GraphNavigatorWidget(self, key=key)
            self.tabs[key] = new_tab
            self.addTab(
                new_tab,
                get_activity_name(
                    get_node(database=key[0], code=key[1]), str_length=30
                ),
            )
        else:
            tab = self.tabs[key]
            tab.new_graph(key)

        if select:
            self.select_tab(self.tabs[key])
            signals.show_tab.emit("Graph Explorer")
