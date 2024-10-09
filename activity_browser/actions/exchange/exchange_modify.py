from typing import Iterable
from bw2data import Node
from bw2data.proxies import ExchangeProxyBase

from activity_browser import signals
from activity_browser.actions.base import ABAction, exception_dialogs
from activity_browser.logger import log
from activity_browser.mod import bw2data as bd
from activity_browser.mod.bw2data.parameters import ActivityParameter
from activity_browser.ui.icons import qicons

from ..parameter.parameter_new_automatic import ParameterNewAutomatic


class ExchangeModify(ABAction):
    """
    ABAction to modify an exchange with the supplied data.
    """

    icon = qicons.delete
    text = "Modify exchange"

    @classmethod
    @exception_dialogs
    def run(cls, exchange: ExchangeProxyBase, data: dict):
        for key, value in data.items():
            if key == "functional" and value == True:
                if not cls.check_can_set_functional(exchange):
                    signals.new_statusbar_message.emit(
                        "Can not set exchange to functional, "
                        "product already referenced through a functional exchange."
                    )
                    log.error(f"Can not set exchange {exchange} to functional, "
                              "there is already a functional exchange.")
                    return
            exchange[key] = value

        exchange.save()

        if "formula" in data:
            cls.parameterize_exchanges(exchange.output.key)

    @staticmethod
    def parameterize_exchanges(key: tuple) -> None:
        """Used whenever a formula is set on an exchange in an activity.

        If no `ActivityParameter` exists for the key, generate one immediately
        """
        act = bd.get_activity(key)
        query = (ActivityParameter.database == key[0]) & (
            ActivityParameter.code == key[1]
        )

        if not ActivityParameter.select().where(query).count():
            ParameterNewAutomatic.run([key])

        group = ActivityParameter.get(query).group

        with bd.parameters.db.atomic():
            bd.parameters.remove_exchanges_from_group(group, act)
            bd.parameters.add_exchanges_to_group(group, act)
            ActivityParameter.recalculate_exchanges(group)

    @staticmethod
    def check_can_set_functional(target_exc: ExchangeProxyBase) -> bool:
        activity = target_exc.output
        all_other_exchanges: list[ExchangeProxyBase] = list(activity.exchanges())
        all_other_exchanges.remove(target_exc)
        for exc in all_other_exchanges:
            if exc.get("functional", False) and exc.input == target_exc.input:
                return False
        return True

