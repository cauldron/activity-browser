from typing import Any

from activity_browser.actions.base import ABAction, exception_dialogs
from activity_browser.mod.bw2data.parameters import (
    ActivityParameter,
    Group,
    GroupDependency,
    parameters,
)
from activity_browser.ui.icons import qicons


class ParameterClearBroken(ABAction):
    """
    Take the given information and attempt to remove all the downstream parameter information.
    """

    icon = qicons.delete
    text = "Clear broken parameter"

    @staticmethod
    @exception_dialogs
    def run(parameter: Any):
        db = parameter.database
        code = parameter.code
        group = parameter.group

        # I'm not sure this is right, because you're removing all the exchanges from the group...
        parameters.remove_exchanges_from_group(group, None, False)
        # Compatible with bw2data events
        for ap in ActivityParameter.select().where(
            (ActivityParameter.database == db) & (ActivityParameter.code == code)
        ):
            ap.delete_instance()

        # Also clear Group if it is not in use anymore
        if (
            not ActivityParameter.select()
            .where(ActivityParameter.group == parameter.group)
            .exists()
        ):
            for obj in Group.select().where(Group.name == group):
                obj.delete_instance()
            GroupDependency.delete().where(GroupDependency.group == group).execute()
