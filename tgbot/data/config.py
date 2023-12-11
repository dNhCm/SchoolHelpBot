from dataclasses import dataclass
from environs import Env

from misc.root import get_root


@dataclass
class Tgbot:
    token: str
    admins: list[int]
    group_id: int
    use_redis: bool


@dataclass
class Redis:
    host: str
    port: int
    password: str


@dataclass
class Payment:
    token: str
    currency: str


@dataclass
class Misc:
    tz: str


@dataclass
class Config:
    tgbot: Tgbot
    redis: Redis
    payment: Payment
    misc: Misc


def get_config() -> Config:
    env = Env()
    path = get_root() + '/tgbot/.env'
    env.read_env(path)

    return Config(
        tgbot=Tgbot(
            token=env.str("TOKEN"),
            admins=list(map(int, env.str("ADMINS").split(' '))),
            group_id=env.int("GROUP_ID"),
            use_redis=env.bool("USE_REDIS"),
        ),
        redis=Redis(
            host=env.str("REDIS_HOST"),
            port=env.int("REDIS_PORT"),
            password=env.str("REDIS_PASSWORD"),
        ),
        payment=Payment(
            token=env.str("PAYMENT_PROVIDER_TOKEN"),
            currency=env.str("PAYMENT_CURRENCY"),
        ),
        misc=Misc(
            tz=env.str("SCHEDULER_TZ")
        )
    )
