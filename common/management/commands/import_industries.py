import json
import os
from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from common.models.common_industry_models import Industry


def _default_fixture_path() -> str:
    common_app_path = apps.get_app_config("common").path
    return os.path.join(common_app_path, "fixtures", "common_industries.json")


class Command(BaseCommand):
    help = "Import industries into common.Industry."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            dest="path",
            default=None,
            help="Path to an industries JSON file (defaults to common/fixtures/common_industries.json).",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Hard-delete existing Industry rows before importing.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run import in a DB transaction and roll it back (prints what would happen).",
        )

    def handle(self, *args, **options):
        path = options.get("path") or _default_fixture_path()
        clear = bool(options.get("clear"))
        dry_run = bool(options.get("dry_run"))

        if not os.path.exists(path):
            raise CommandError(f"Industries file not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                payload: dict[str, Any] = json.load(f)
        except json.JSONDecodeError as e:
            raise CommandError(f"Invalid JSON in {path}: {e}") from e

        industries = payload.get("industries")
        if not isinstance(industries, list):
            raise CommandError(
                'Invalid schema: expected top-level key "industries" as a list.'
            )

        created = 0
        updated = 0

        with transaction.atomic():
            if clear:
                self.stdout.write("Clearing existing industries...")
                if not dry_run:
                    Industry._base_manager.all().delete()

            for item in industries:
                if isinstance(item, str):
                    name = item.strip()
                elif isinstance(item, dict):
                    name = (item.get("name") or "").strip()
                else:
                    raise CommandError(
                        "Invalid industry item: expected string or object."
                    )

                if not name:
                    raise CommandError('Invalid industry: missing non-empty "name".')

                _industry, was_created = Industry._base_manager.update_or_create(
                    name=name,
                    defaults={
                        "is_active": True,
                        "is_deleted": False,
                    },
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

            if dry_run:
                transaction.set_rollback(True)

        self.stdout.write(
            self.style.SUCCESS(
                "Import complete"
                + (" (dry-run; rolled back)" if dry_run else "")
                + f". Industries: +{created}/~{updated}."
            )
        )
