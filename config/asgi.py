"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from fastapi import FastAPI
from src.tiny_voucher.shared.utils.logging import configure_structlog

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

application = get_asgi_application()

from config.settings_vars import settings
from src.tiny_voucher.presentation.fastapi.urls import voucher_admin_router
from src.tiny_voucher.presentation.fastapi.tags import VOUCHER_TAGS

fastapp = FastAPI(
    openapi_tags=[
        tag.dict(by_alias=True)
        for tag in VOUCHER_TAGS
    ]
)

fastapp.include_router(voucher_admin_router, prefix="/api/v1")


configure_structlog(debug=settings.DEBUG)