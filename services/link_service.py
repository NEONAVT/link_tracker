import time
from typing import List
from urllib.parse import urlparse
from exceptions import DomainValidationError
from repository.link_repository import LinkRepository
import logging

logger = logging.getLogger(__name__)


class LinkService:
    """
    Сервис для работы с посещёнными ссылками и доменами.

    Атрибуты:
        repository (LinkRepository): Репозиторий для хранения данных.
    """

    def __init__(self, repository: LinkRepository):
        """
        Инициализация сервиса.

        Args:
            repository (LinkRepository): Репозиторий для хранения данных.
        """
        self.repository = repository
        logger.info("LinkService initialized")

    def add_visited_links(self, links: List[str]):
        """
        Добавляет посещённые ссылки, извлекая домены и сохраняя их.

        Args:
            links (List[str]): Список посещённых ссылок.

        Raises:
            Exception: При ошибках добавления или валидации.
        """
        timestamp = int(time.time())
        logger.debug(f"Adding links at {timestamp}: {links}")
        try:
            domains = self.extract_domains(links)
            self.repository.add_domains(domains, timestamp)
            logger.info(f"Added {len(domains)} domains")
        except Exception as e:
            logger.error(f"Error adding links: {str(e)}")
            raise

    def get_visited_domains(self, from_time: int, to_time: int) -> list:
        """
        Получает домены, посещённые в заданном интервале времени.

        Args:
            from_time (int): Начало интервала (включительно).
            to_time (int): Конец интервала (включительно).

        Returns:
            list: Список доменов.

        Raises:
            Exception: При ошибках получения данных.
        """
        logger.debug(f"Getting domains from {from_time} to {to_time}")
        try:
            domains = self.repository.get_domains_in_interval(
                from_time, to_time)
            logger.info(f"Found {len(domains)} domains in time range")
            return domains
        except Exception as e:
            logger.error(f"Error getting domains: {str(e)}")
            raise

    def extract_domains(self, links: List[str]) -> set:
        """
        Извлекает уникальные домены из списка ссылок.

        Args:
            links (List[str]): Список URL.

        Returns:
            set: Множество доменов.
        """
        domains = set()
        for link in links:
            domain = self.extract_domain(link)
            if domain:
                domains.add(domain)
        return domains

    def extract_domain(self, url: str) -> str:
        """
        Извлекает домен из URL.

        Если в URL отсутствует схема, добавляет "http://".

        Args:
            url (str): URL для обработки.

        Returns:
            str: Домен в нижнем регистре.

        Raises:
            DomainValidationError: Если домен невалиден.
        """
        try:
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            parsed = urlparse(url)
            domain = parsed.netloc.split(":")[0].lower().strip()
            if not domain:
                raise DomainValidationError(url)
            return domain
        except Exception:
            raise DomainValidationError(url)
