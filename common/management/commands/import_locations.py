import json
import os
from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from common.models.common_region_models import (
    City,
    Country,
    GeographicalTarget,
)


def _default_fixture_path() -> str:
    common_app_path = apps.get_app_config("common").path
    return os.path.join(common_app_path, "fixtures", "common_locations.json")


class Command(BaseCommand):
    help = "Import continents / countries / states / cities into Country + City."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            dest="path",
            default=None,
            help="Path to a locations JSON file (defaults to common/fixtures/common_locations.json).",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Hard-delete existing Country and City rows before importing.",
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
            raise CommandError(f"Locations file not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                payload: dict[str, Any] = json.load(f)
        except json.JSONDecodeError as e:
            raise CommandError(f"Invalid JSON in {path}: {e}") from e

        continents = payload.get("continents", [])
        if continents is None:
            continents = []
        if not isinstance(continents, list):
            raise CommandError(
                'Invalid schema: expected top-level key "continents" as a list.'
            )

        countries = payload.get("countries")
        if not isinstance(countries, list):
            raise CommandError(
                'Invalid schema: expected top-level key "countries" as a list.'
            )

        created = {"continent": 0, "country": 0, "state": 0, "city": 0}
        updated = {"continent": 0, "country": 0, "state": 0, "city": 0}

        with transaction.atomic():
            if clear:
                self.stdout.write("Clearing existing locations...")
                if not dry_run:
                    GeographicalTarget._base_manager.all().delete()
                    City._base_manager.all().delete()
                    Country._base_manager.all().delete()

            # 1) Continents (stored as Country rows with parent=None)
            continent_by_code: dict[str, Country] = {}
            for cont in continents:
                if not isinstance(cont, dict):
                    raise CommandError(
                        'Invalid schema: each item in "continents" must be an object.'
                    )
                cont_name = (cont.get("name") or "").strip()
                cont_code = (cont.get("code") or "").strip()
                if not cont_name or not cont_code:
                    raise CommandError(
                        'Invalid continent: each continent needs non-empty "name" and "code".'
                    )

                continent, was_created = Country._base_manager.update_or_create(
                    code=cont_code,
                    defaults={
                        "name": cont_name,
                        "phone_code": None,
                        "parent": None,
                        "is_active": True,
                        "is_deleted": False,
                    },
                )
                (created if was_created else updated)["continent"] += 1
                continent_by_code[cont_code] = continent

            # 2) Countries (may optionally link to a continent via continent_code)
            for c in countries:
                if not isinstance(c, dict):
                    raise CommandError(
                        "Invalid schema: each item in countries must be an object."
                    )

                name = (c.get("name") or "").strip()
                code = (c.get("code") or "").strip()
                phone_code = c.get("phone_code", None)
                continent_code = (c.get("continent_code") or "").strip() or None

                if not name or not code:
                    raise CommandError(
                        'Invalid country: each country needs non-empty "name" and "code".'
                    )

                parent_continent = None
                if continent_code:
                    parent_continent = continent_by_code.get(continent_code)
                    if parent_continent is None:
                        raise CommandError(
                            f'Invalid country {code}: unknown continent_code "{continent_code}".'
                        )

                country, was_created = Country._base_manager.update_or_create(
                    code=code,
                    defaults={
                        "name": name,
                        "phone_code": phone_code,
                        "parent": parent_continent,
                        "is_active": True,
                        "is_deleted": False,
                    },
                )
                (created if was_created else updated)["country"] += 1

                states = c.get("states", [])
                if states is None:
                    states = []
                if not isinstance(states, list):
                    raise CommandError(
                        f'Invalid schema for country {code}: "states" must be a list.'
                    )

                for s in states:
                    if not isinstance(s, dict):
                        raise CommandError(
                            f"Invalid schema for country {code}: each state must be an object."
                        )

                    state_name = (s.get("name") or "").strip()
                    state_code = s.get("code", None)
                    if state_code is not None:
                        state_code = str(state_code).strip() or None

                    if not state_name:
                        raise CommandError(
                            f'Invalid state for country {code}: missing non-empty "name".'
                        )

                    state, was_created = City._base_manager.update_or_create(
                        country=country,
                        name=state_name,
                        parent=None,
                        defaults={
                            "code": state_code,
                            "is_active": True,
                            "is_deleted": False,
                        },
                    )
                    (created if was_created else updated)["state"] += 1

                    cities = s.get("cities", [])
                    if cities is None:
                        cities = []
                    if not isinstance(cities, list):
                        raise CommandError(
                            f'Invalid schema for country {code} state {state_name}: "cities" must be a list.'
                        )

                    for city_item in cities:
                        if isinstance(city_item, str):
                            city_name = city_item.strip()
                            city_code = None
                        elif isinstance(city_item, dict):
                            city_name = (city_item.get("name") or "").strip()
                            city_code = city_item.get("code", None)
                            if city_code is not None:
                                city_code = str(city_code).strip() or None
                        else:
                            raise CommandError(
                                f"Invalid city for country {code} state {state_name}: expected string or object."
                            )

                        if not city_name:
                            raise CommandError(
                                f'Invalid city for country {code} state {state_name}: missing non-empty "name".'
                            )

                        _city, was_created = City._base_manager.update_or_create(
                            country=country,
                            name=city_name,
                            parent=state,
                            defaults={
                                "code": city_code,
                                "is_active": True,
                                "is_deleted": False,
                            },
                        )
                        (created if was_created else updated)["city"] += 1

            if dry_run:
                transaction.set_rollback(True)

        self.stdout.write(
            self.style.SUCCESS(
                "Import complete"
                + (" (dry-run; rolled back)" if dry_run else "")
                + f". Continents: +{created['continent']}/~{updated['continent']}, "
                + f"Countries: +{created['country']}/~{updated['country']}, "
                + f"States: +{created['state']}/~{updated['state']}, "
                + f"Cities: +{created['city']}/~{updated['city']}."
            )
        )
