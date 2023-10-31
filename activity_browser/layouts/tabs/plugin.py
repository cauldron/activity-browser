from activity_browser.layouts.base import ABTab


class PluginTab(ABTab):
    """Parent class of every plugin tab"""

    def __init__(self, plugin, panel, parent=None):
        """
        :param plugin: instance of the plugin class
        :param panel: "left" or "right"
        """
        super().__init__(parent)
        self.panel = panel
        self.plugin = plugin
        self.isPlugin = True
        self.setTabsClosable(True)
