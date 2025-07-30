from redis import Redis


class LinkRepository:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.key = "visited:domains"

    def add_domains(self, domains: set, timestamp: int):
        score_map = {domain: timestamp for domain in domains}
        self.redis.zadd(self.key, score_map)

    def get_domains_in_interval(self, start: int, end: int) -> list:
        result = self.redis.zrangebyscore(self.key, start, end)
        return sorted(set(result))
