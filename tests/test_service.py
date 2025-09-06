from services.link_service import LinkService
from repository.link_repository import LinkRepository

class DummyRepo(LinkRepository):
    def __init__(self):
        self.saved = []

    def add_domains(self, domains, timestamp):
        self.saved.append((timestamp, list(domains)))

    def get_domains_in_interval(self, start, end):
        return []

def test_extract_domain_variants():
    svc = LinkService(repository=DummyRepo())
    assert svc.extract_domain("https://ya.ru") == "ya.ru"
    assert svc.extract_domain("https://ya.ru?q=123") == "ya.ru"
    assert svc.extract_domain("funbox.ru") == "funbox.ru"
    assert svc.extract_domain("google.com/search?q=123") == "google.com"
    assert svc.extract_domain("http://example.com:8080/path") == "example.com"

def test_add_visited_links_normalizes_and_saves(monkeypatch):
    svc = LinkService(repository=DummyRepo())
    monkeypatch.setattr("services.link_service.time.time", lambda: 1_700_000_000)
    svc.add_visited_links(["ya.ru", "https://ya.ru?q=1", "EXAMPLE.COM"])
    ts, domains = svc.repository.saved[0]
    assert ts == 1_700_000_000
    assert set(domains) == {"ya.ru", "example.com"}
