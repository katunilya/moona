import pytest

from mona import context


@pytest.fixture
def scope():
    return {
        "client": ("172.29.0.10", 34784),
        "headers": [
            [b"host", b"asgi-scope.now.sh"],
            [b"x-forwarded-host", b"asgi-scope.now.sh"],
            [b"x-real-ip", b"199.188.193.220"],
            [b"x-forwarded-for", b"199.188.193.220"],
            [b"x-forwarded-proto", b"https"],
            [b"x-now-id", b"fb6gw-1527863960919-mjYC9OJ9WTsfnw4EiRTDmMst"],
            [b"x-now-log-id", b"mjYC9OJ9WTsfnw4EiRTDmMst"],
            [b"x-zeit-co-forwarded-for", b"199.188.193.220"],
            [b"connection", b"close"],
            [
                b"user-agent",
                b"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko"
                b"/20100101 Firefox/60.0",
            ],
            [
                b"accept",
                b"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=" b"0.8",
            ],
            [b"accept-language", b"en-US,en;q=0.5"],
            [b"accept-encoding", b"gzip, deflate, br"],
            [b"upgrade-insecure-requests", b"1"],
        ],
        "asgi": {
            "version": "3.0",
            "spec_version": "2.2",
        },
        "http_version": "0.0",
        "method": "GET",
        "path": "/path",
        "raw_path": b"/path?qs=hello",
        "root_path": "",
        "query_string": b"qs=hello",
        "scheme": "http",
        "server": ("172.28.0.10", 8000),
        "type": "http",
    }


@pytest.fixture
def receive():
    async def receive() -> context.Message:
        return {"type": "http.receive.body", "body": b"body"}

    return receive


@pytest.fixture
def send():
    async def send(_: context.Message) -> None:
        return None

    return send


@pytest.fixture
def mock_context(scope, receive, send) -> context.Context:
    return context.from_asgi(scope, receive, send)
