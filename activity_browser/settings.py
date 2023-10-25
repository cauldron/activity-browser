# -*- coding: utf-8 -*-
import json
import logging
import shutil
from pathlib import Path
from typing import Generator, Optional

import platformdirs
import bw2data
from PySide2.QtWidgets import QMessageBox

from activity_browser.logger import ABHandler
from activity_browser.signals import signals

logger = logging.getLogger("ab_logs")
log = ABHandler.setup_with_logger(logger, __name__)


class BaseSettings(object):
    """Base Class for handling JSON settings files."""

    def __init__(self, directory: str, filename: str = None):
        self.data_dir: str = directory
        self.filename: str = filename or "default_settings.json"
        self.settings_file: Path = Path(self.data_dir).joinpath(self.filename)
        self.settings: Optional[dict] = None
        self.initialize_settings()

    @classmethod
    def get_default_settings(cls) -> dict:
        """Returns dictionary containing the default settings for the file"""
        raise NotImplementedError

    def restore_default_settings(self) -> None:
        """Undo all user settings and return to original state."""
        self.settings = self.get_default_settings()
        self.write_settings()

    def initialize_settings(self) -> None:
        """Attempt to find and read the settings_file, creates a default
        if not found
        """
        if self.settings_file.is_file():
            self.load_settings()
        else:
            self.settings = self.get_default_settings()
            self.write_settings()

    def load_settings(self) -> None:
        with self.settings_file.open() as infile:
            self.settings = json.load(infile)

    def write_settings(self) -> None:
        with self.settings_file.open("w") as outfile:
            json.dump(self.settings, outfile, indent=4, sort_keys=True)


class ABSettings(BaseSettings):
    """
    Interface to the json settings file. Will create a userdata directory via platformdirs if not
    already present.
    """

    def __init__(self, filename: str):
        ab_dir = platformdirs.user_data_path("ActivityBrowser", "ActivityBrowser", ensure_exists=True)
        self._update_old_settings(ab_dir, filename)

        # Currently loaded plugins objects as:
        # {plugin_name: <plugin_object>, ...}
        # this list is generated at startup and never writen in settings.
        # it is filled by the plugin controller
        self.plugins = {}

        super().__init__(ab_dir, filename)

    @staticmethod
    def _update_old_settings(directory: Path, filename: str) -> None:
        """Update old settings, backwards compatibility method.

        This function is only required for compatibility with the old settings file
        and can be removed in a future release.

        Parameters
        ----------
        directory : Path
            Path to the directory containing the settings.
        filename : str
            Name of the settings file.
        """
        new_file = directory.joinpath(filename)
        if not new_file.exists():
            package_dir = Path(__file__).resolve().parents[1]
            old_settings = package_dir.joinpath("ABsettings.json")
            if old_settings.exists():
                shutil.copyfile(old_settings, new_file)
        if new_file.is_file():
            with new_file.open() as current:
                current_settings = json.load(current)
            if "current_bw_dir" not in current_settings:
                new_settings_content = {
                    "current_bw_dir": current_settings["custom_bw_dir"],
                    "custom_bw_dirs": [current_settings["custom_bw_dir"]],
                    "startup_project": current_settings["startup_project"],
                }
                with new_file.open("w") as new_file:
                    json.dump(new_settings_content, new_file)

    @classmethod
    def get_default_settings(cls) -> dict:
        """Using methods from the commontasks file to set default settings."""
        return {
            "current_bw_dir": str(bw2data.projects._base_data_dir),
            "custom_bw_dirs": [str(bw2data.projects._base_data_dir)],
            "startup_project": cls.get_default_project_name(),
        }

    @property
    def custom_bw_dir(self) -> str:
        """Returns the custom brightway directory, or the default."""
        return self.settings.get("custom_bw_dirs") or str(bw2data.projects._base_data_dir)

    @property
    def current_bw_dir(self) -> str:
        """Returns the current brightway directory."""
        return self.settings.get("current_bw_dir") or str(bw2data.projects._base_data_dir)

    @current_bw_dir.setter
    def current_bw_dir(self, directory: str) -> None:
        self.settings["current_bw_dir"] = directory
        self.write_settings()

    @custom_bw_dir.setter
    def custom_bw_dir(self, directory: str) -> None:
        """Sets the custom brightway directory to `directory`"""
        if directory not in self.settings["custom_bw_dirs"]:
            self.settings["custom_bw_dirs"].append(directory)
            self.write_settings()

    def remove_custom_bw_dir(self, directory: str) -> None:
        """Removes the brightway directory to 'directory'"""
        try:
            self.settings["custom_bw_dirs"].remove(directory)
            self.write_settings()
        except KeyError as e:
            QMessageBox.warning(
                self,
                f"Error while attempting to remove a brightway environmental dir: {e}",
            )

    @property
    def startup_project(self) -> str:
        """Get the startup project from the settings, or the default"""
        project = self.settings.get("startup_project", self.get_default_project_name())
        if project and project not in bw2data.projects:
            project = self.get_default_project_name()
        return project

    @startup_project.setter
    def startup_project(self, project: str) -> None:
        """Sets the startup project to `project`"""
        self.settings.update({"startup_project": project})

    @staticmethod
    def get_default_project_name() -> Optional[str]:
        """Returns the default project name."""
        if "default" in bw2data.projects:
            return "default"
        elif len(bw2data.projects):
            return next(iter(bw2data.projects)).name
        else:
            return None


class ProjectSettings(BaseSettings):
    """
    Handles user settings which are specific to projects. Created initially to handle read-only/writable database status
    Code based on ABSettings class, if more different types of settings are needed, could inherit from a base class

    structure: singleton, loaded dependent on which project is selected.
        Persisted on disc, Stored in the BW2 projects data folder for each project
        a dictionary1 of dictionaries2
        Dictionary1 keys are settings names (currently just 'read-only-databases'), values are dictionary2s
        Dictionary2 keys are database names, values are bools

    For now, decided to not include saving writable-activities to settings.
    As activities are identified by tuples, and saving them to json requires extra code
    https://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json
    This is currently not worth the effort but could be returned to later

    """

    def __init__(self, filename: str):
        # on selection of a project (signal?), find the settings file for that project if it exists
        # it can be a custom location, based on ABsettings. So check that, and if not, use default?
        # once found, load the settings or just an empty dict.
        self.connect_signals()
        super().__init__(bw2data.projects.dir, filename)

        # https://github.com/LCA-ActivityBrowser/activity-browser/issues/235
        # Fix empty settings file and populate with currently active databases
        if "read-only-databases" not in self.settings:
            self.settings.update(self.process_brightway_databases())
            self.write_settings()
        if "plugins_list" not in self.settings:
            self.settings.update({"plugins_list": []})
            self.write_settings()

    def connect_signals(self):
        """Reload the project settings whenever a project switch occurs."""
        signals.project_selected.connect(self.reset_for_project_selection)
        signals.plugin_selected.connect(self.add_plugin)

    @classmethod
    def get_default_settings(cls) -> dict:
        """Return default empty settings dictionary."""
        settings = cls.process_brightway_databases()
        settings["plugins_list"] = []
        return settings

    @staticmethod
    def process_brightway_databases() -> dict:
        """Process brightway database list and return new settings dictionary.

        NOTE: This ignores the existing database read-only settings.
        """
        return {"read-only-databases": {name: True for name in bw2data.databases.list}}

    def reset_for_project_selection(self) -> None:
        """On switching project, attempt to read the settings for the new
        project.
        """
        log.info("Reset project settings directory to:", bw2data.projects.dir)
        self.settings_file = bw2data.projects.dir.joinpath(self.filename)
        self.initialize_settings()
        # create a plugins_list entry for old projects
        self.settings.setdefault("plugins_list", [])
        self.write_settings()

    def add_db(self, db_name: str, read_only: bool = True) -> None:
        """Store new databases and relevant settings here when created/imported"""
        self.settings["read-only-databases"].setdefault(db_name, read_only)
        self.write_settings()

    def modify_db(self, db_name: str, read_only: bool) -> None:
        """Update write-rules for the given database"""
        self.settings["read-only-databases"].update({db_name: read_only})
        self.write_settings()

    def remove_db(self, db_name: str) -> None:
        """When a database is deleted from a project, the settings are also deleted."""
        self.settings["read-only-databases"].pop(db_name, None)
        self.write_settings()

    def db_is_readonly(self, db_name: str) -> bool:
        """Check if given database is read-only, defaults to yes."""
        return self.settings["read-only-databases"].get(db_name, True)

    def get_editable_databases(self) -> Generator[str, None, None]:
        """Return list of database names where read-only is false

        NOTE: discards the biosphere3 database based on name.
        """
        iterator = self.settings.get("read-only-databases", {}).items()
        return (name for name, ro in iterator if not ro and name != "biosphere3")

    def add_plugin(self, name: str, select: bool = True) -> None:
        """Add a plugin to settings or remove it"""
        if select:
            self.settings["plugins_list"].append(name)
            self.write_settings()
            return
        if name in self.settings["plugins_list"]:
            self.settings["plugins_list"].remove(name)
            self.write_settings()

    def get_plugins_list(self):
        """Return a list of plugins names"""
        return self.settings["plugins_list"]


ab_settings = ABSettings("ABsettings.json")
project_settings = ProjectSettings("AB_project_settings.json")
