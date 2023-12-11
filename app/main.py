from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

from app.screens.run import RunScreen
from app.screens.setup import SetupScreen
from misc.logger import logger


class BN(MDBottomNavigation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        run_tab = MDBottomNavigationItem(
            name="run",
            text="Run",
            icon="run"
        )
        run_tab.add_widget(RunScreen(name="run"))
        self.add_widget(run_tab)

        setup_tab = MDBottomNavigationItem(
            name="setup",
            text="Setup",
            icon="database-settings"
        )
        setup_tab.add_widget(SetupScreen(name="setup"))
        self.add_widget(setup_tab)


class SchoolHelpApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"

        return BN()


if __name__ == "__main__":
    try:
        SchoolHelpApp().run()
    except (KeyboardInterrupt, SystemExit):
        logger.info("App was stopped!")
