from redis import Redis


class LinkRepository:
    """
    Репозиторий для работы с посещёнными доменами в Redis.

    Хранит домены в отсортированном множестве с метками времени
    в качестве score.

    Attributes:
        redis (Redis): Клиент Redis.
        key (str): Ключ для хранения множества доменов.
    """

    def __init__(self, redis: Redis):
        """
        Инициализирует репозиторий.

        Args:
            redis (Redis): Клиент Redis.
        """
        self.redis = redis
        self.key = "visited:domains"

    def add_domains(self, domains: set, timestamp: int):
        """
        Добавляет домены с указанным временным штампом.

        Args:
            domains (set): Множество доменов для добавления.
            timestamp (int): Метка времени, используемая как score.
        """
        score_map = {domain: timestamp for domain in domains}
        self.redis.zadd(self.key, score_map)

    def get_domains_in_interval(self, start: int, end: int) -> list:
        """
        Получает уникальные домены из интервала времени.

        Args:
            start (int): Начало интервала (включительно).
            end (int): Конец интервала (включительно).

        Returns:
            list: Отсортированный список уникальных доменов.
        """
        result = self.redis.zrangebyscore(self.key, start, end)
        return sorted(set(result))
