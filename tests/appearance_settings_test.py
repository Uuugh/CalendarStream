"""Fast, database-free tests for appearance validation; also run by suite 81."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.services.appearance_settings import appearance_values


class Refused(ValueError):
    def __init__(self, text, *fields):
        super().__init__(text)
        self.fields = fields


class Upload:
    def __init__(self, data):
        self.data, self.limit = data, None

    async def read(self, size):
        self.limit = size
        return self.data[:size]


class AppearanceTests(unittest.IsolatedAsyncioTestCase):
    async def prepare(self, form, brand=None):
        return await appearance_values(form, brand=brand, image_kind=lambda data: "image/png" if data == b"png" else "",
                                       field_error=Refused, max_bytes=8)

    async def test_invalid_percentages_do_not_mutate_brand(self):
        brand = {"logo": {"b64": "old"}}
        for value in ("bad", "201", "-1"):
            with self.assertRaises(Refused):
                await self.prepare({"remove_logo": "1", "intensity": value}, brand)
        self.assertEqual(brand, {"logo": {"b64": "old"}})

    async def test_bounded_upload_and_bad_type(self):
        upload = Upload(b"x" * 100)
        with self.assertRaises(Refused): await self.prepare({"logo": upload})
        self.assertEqual(upload.limit, 9)
        with self.assertRaises(Refused): await self.prepare({"favicon": Upload(b"bad")})

    async def test_upload_remove_reset(self):
        values = await self.prepare({"logo": Upload(b"png"), "remove_favicon": "1", "reset": "1"},
                                    {"favicon": {"b64": "old"}})
        self.assertEqual(values, ({"logo": {"mime": "image/png", "b64": "cG5n"}}, "left", {"i": 100, "d": 100}))
        with self.assertRaises(Refused): await self.prepare({"grips": "unknown"})


if __name__ == "__main__": unittest.main()
