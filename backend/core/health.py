import redis
from django.conf import settings
from django.db import connection, Error as DBError
from django.core.cache import cache
from django.views.decorators.http import require_GET
from django.http.response import JsonResponse

def check_db() -> bool:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True
    except DBError:
        return False


def check_redis() -> bool:
    try:
        client = redis.Redis.from_url(
            url=settings.REDIS_URL,
            socket_connect_timeout=1,
            socket_timeout=1
        )
        return bool(client.ping())
    except redis.RedisError:
        return False


@require_GET
def is_alive(request):
    """Liveness: is process alive. Don't check any external dependencies."""
    return JsonResponse({"status": "alive"}, status=200)


@require_GET
def is_ready(request):
    """Readiness: can accept connections. Check db and redis are up."""
    checks = {
        "db": "ok" if check_db() else "fail",
        "redis": "ok" if check_redis() else "fail"
    }
    healthy = all(v == "ok" for v in checks.values())

    return JsonResponse(
        { "status": "ready" if healthy else "unavailable", "checks": checks },
        status=200 if healthy else 503,
    )