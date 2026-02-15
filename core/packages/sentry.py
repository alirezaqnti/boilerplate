"""
Sentry (error monitoring and performance). Init only when SENTRY_DSN is set.
"""

from __future__ import annotations

import os


def init_sentry(*, environment: str | None = None) -> None:
    dsn = os.getenv("SENTRY_DSN", "").strip()
    if not dsn:
        return

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    env = environment or os.getenv("ENVIRONMENT", "local")
    traces_sample_rate_str = os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")
    try:
        traces_sample_rate = float(traces_sample_rate_str)
    except ValueError:
        traces_sample_rate = 0.1

    send_default_pii = os.getenv("SENTRY_SEND_DEFAULT_PII", "false").lower() in (
        "true",
        "1",
        "yes",
    )

    sentry_sdk.init(
        dsn=dsn,
        environment=env,
        integrations=[DjangoIntegration()],
        send_default_pii=send_default_pii,
        traces_sample_rate=traces_sample_rate,
    )
