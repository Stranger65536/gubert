# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from enum import Enum

from simple_term_menu import TerminalMenu

from GcloudManager import GcloudManager

SEARCH_HINT = " Press '/' to search across options"
MAIN_STATUS_HELP = "I'm Gubert. What do you want to do?"

ACTION = "action"
GO_BACK = "Go Back"


class Actions(Enum):
    SWITCH_GCLOUD_CONFIGURATION = \
        "Switch gcloud configuration"
    SWITCH_KUBECTL_CONTEXT = \
        "Switch kubectl context"
    DISCOVER_KUBERNETES_CLUSTERS = \
        "Discover kubernetes clusters from gcloud"
    EXIT = "Exit"

    @staticmethod
    def of(order: int) -> 'Actions':
        if order is None:
            return Actions.EXIT
        return [e for i, e in enumerate(Actions) if i == order][0]


def _gcloud_configuration_dialog() -> bool:
    """
    Handles gcloud configuration switch dialog.
    May throw exception if gcloud sub call failed
    :return: True if switched. False if cancelled or got back.
    """
    gcloud: GcloudManager = GcloudManager()
    options = gcloud.configurations_list()
    preselected_entry = \
        [i for i, o in enumerate(options) if o.is_active]
    cursor_index = preselected_entry[0] if preselected_entry else 0
    # align to table-like grid by max length
    name_length = max([len(i.name or '') for i in options] + [4])
    account_length = max([len(i.account or '') for i in options] + [7])
    project_length = max([len(i.project or '') for i in options] + [7])
    template = f"{{NAME:{name_length}}} " \
               f"{{ACTIVE:6}} " \
               f"{{ACCOUNT:{account_length}}} " \
               f"{{PROJECT:{project_length}}} "
    # shift by 2 spaces to align to selection list
    status = ["  " + template.format(
        NAME="Name", ACTIVE="Active",
        ACCOUNT="Account", PROJECT="Project"), SEARCH_HINT]
    rendered_options = \
        [template.format(NAME=str(i.name or ""),
                         ACTIVE=str(i.is_active) if i.is_active else "",
                         ACCOUNT=str(i.account or ""),
                         PROJECT=str(i.project or ""))
         for i in options] + [GO_BACK]
    chosen_config = TerminalMenu(
        status_bar=status,
        cursor_index=cursor_index,
        title="Choose a configuration to activate",
        menu_entries=rendered_options,
    ).show()
    if chosen_config is None or chosen_config >= len(options):
        return False
    gcloud.activate_configuration(options[chosen_config].name)
    return True


def main():
    while True:
        status = [SEARCH_HINT]
        action = Actions.of(TerminalMenu(
            status_bar=status,
            title=MAIN_STATUS_HELP,
            menu_entries=[e.value for e in Actions],
        ).show())
        if action == Actions.SWITCH_GCLOUD_CONFIGURATION:
            go_back = _gcloud_configuration_dialog()
            if not go_back:
                continue
        elif action == Actions.SWITCH_KUBECTL_CONTEXT:
            pass
        elif action == Actions.DISCOVER_KUBERNETES_CLUSTERS:
            gcloud = GcloudManager()
            pass
        elif action == Actions.EXIT:
            break
        else:
            raise ValueError(f"Uncovered action: {action}")


if __name__ == "__main__":
    # TODO argparse for verbose, timeout and gcloud path
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
