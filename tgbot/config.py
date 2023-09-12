
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBotConfig:
    bot_token: str
    group_id: int
    admins: list[int]

@dataclass
class MiscConfig:
    other_params = None

@dataclass
class Config:
    tgbot: TgBotConfig
    misc: MiscConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tgbot = TgBotConfig(
            bot_token=env.str('BOT_TOKEN'),
            group_id=env.int('GROUP_ID'),
            admins=list(map(lambda x: int(x), env.str('ADMINS').split(' '))),
        ),
        misc = MiscConfig()
    )