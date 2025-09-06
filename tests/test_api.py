def test_post_visited_links_and_get_domains(client, repo, monkeypatch):
    t1 = 1_700_000_000
    t2 = 1_700_000_100

    # First batch at t1
    monkeypatch.setattr("services.link_service.time.time", lambda: t1)

    payload = {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "google.com/search?q=123",
            "http://example.com:8080/x"
        ]
    }
    r = client.post("/links-tracker/visited_links", json=payload)
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

    # Second batch at t2
    monkeypatch.setattr("services.link_service.time.time", lambda: t2)
    r = client.post("/links-tracker/visited_links", json={"links": ["blog.example.com/page"]})
    assert r.status_code == 200

    # Interval t1..t1 (NOTE: API expects 'to_time' if router has no alias)
    r = client.get(f"/links-tracker/visited_domains?from={t1}&to_time={t1}")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert set(data["domains"]) == {"ya.ru", "funbox.ru", "google.com", "example.com"}

    # Interval t1..t2
    r = client.get(f"/links-tracker/visited_domains?from={t1}&to_time={t2}")
    assert r.status_code == 200
    data = r.json()
    assert set(data["domains"]) == {"ya.ru", "funbox.ru", "google.com", "example.com", "blog.example.com"}

def test_invalid_time_range_returns_400(client):
    # Here use 'to_time' because the router parameter likely has no alias for 'to'
    r = client.get("/links-tracker/visited_domains?from=100&to_time=50")
    assert r.status_code == 400

def test_validation_error_on_missing_body(client):
    r = client.post("/links-tracker/visited_links")
    assert r.status_code == 422
