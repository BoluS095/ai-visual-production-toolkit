import json
import tempfile
import unittest
from pathlib import Path

from src.intake.parser import (
    DEFAULT_DIMENSIONS,
    extract_generation_params,
    load_brief,
    validate_brief,
)


VALID_BRIEF = {
    "client": "Example Client",
    "project": "Launch assets",
    "deliverables": [
        {
            "type": "social_post",
            "platform": "instagram",
            "dimensions": "1080x1080",
            "quantity": 2,
            "description": "A launch announcement",
            "color_palette": ["#112233", "#AABBCC"],
        }
    ],
    "brand_assets": {"logo_url": "https://example.test/logo.png"},
}


class BriefParserTests(unittest.TestCase):
    def write_json(self, directory: str, payload: object) -> Path:
        path = Path(directory) / "brief.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_loads_repository_sample_brief(self):
        sample = Path(__file__).resolve().parents[1] / "examples" / "sample_brief.json"
        brief = load_brief(sample)
        self.assertEqual(brief["client"], "Example Brand")
        self.assertEqual(len(extract_generation_params(brief)), 2)

    def test_extracts_normalized_generation_parameters(self):
        params = extract_generation_params(VALID_BRIEF)[0]
        self.assertEqual(params["type"], "social_post")
        self.assertEqual(params["platform"], "instagram")
        self.assertEqual(params["dimensions"], "1080x1080")
        self.assertEqual(params["quantity"], 2)
        self.assertEqual(params["color_palette"], ["#112233", "#AABBCC"])

    def test_applies_documented_defaults(self):
        brief = {**VALID_BRIEF, "deliverables": [{}]}
        params = extract_generation_params(brief)[0]
        self.assertEqual(params["type"], "generic")
        self.assertEqual(params["platform"], "universal")
        self.assertEqual(params["dimensions"], DEFAULT_DIMENSIONS)
        self.assertEqual(params["quantity"], 1)

    def test_missing_file_raises_clear_error(self):
        with self.assertRaisesRegex(FileNotFoundError, "Brief not found"):
            load_brief("this-file-does-not-exist.json")

    def test_invalid_json_reports_location(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.json"
            path.write_text('{"client":', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid JSON.*line"):
                load_brief(path)

    def test_rejects_non_object_root(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_json(directory, ["not", "an", "object"])
            with self.assertRaisesRegex(ValueError, "Brief must be a JSON object"):
                load_brief(path)

    def test_requires_non_empty_client_and_project(self):
        for field in ("client", "project"):
            with self.subTest(field=field):
                brief = {**VALID_BRIEF, field: "  "}
                with self.assertRaisesRegex(ValueError, field):
                    extract_generation_params(brief)

    def test_requires_deliverables_list_of_objects(self):
        with self.assertRaisesRegex(ValueError, "deliverables.*list"):
            extract_generation_params({**VALID_BRIEF, "deliverables": {}})
        with self.assertRaisesRegex(ValueError, "deliverables\[0\].*JSON object"):
            extract_generation_params({**VALID_BRIEF, "deliverables": ["bad"]})

    def test_quantity_must_be_a_positive_integer(self):
        for quantity in (0, -1, True, 1.5, "3"):
            with self.subTest(quantity=quantity):
                brief = {**VALID_BRIEF, "deliverables": [{"quantity": quantity}]}
                with self.assertRaisesRegex(ValueError, "quantity must be a positive integer"):
                    extract_generation_params(brief)

    def test_dimensions_must_be_positive_width_by_height(self):
        for dimensions in ("0x1080", "1080x0", "square", "1080", 1080):
            with self.subTest(dimensions=dimensions):
                brief = {**VALID_BRIEF, "deliverables": [{"dimensions": dimensions}]}
                with self.assertRaisesRegex(ValueError, "WIDTHxHEIGHT"):
                    extract_generation_params(brief)

    def test_color_palette_must_be_list_of_strings(self):
        for palette in ("#112233", [123], None):
            with self.subTest(palette=palette):
                brief = {**VALID_BRIEF, "deliverables": [{"color_palette": palette}]}
                with self.assertRaisesRegex(ValueError, "color_palette"):
                    extract_generation_params(brief)

    def test_quality_warnings_are_actionable(self):
        brief = {
            **VALID_BRIEF,
            "brand_assets": {},
            "deliverables": [{"quantity": 75, "description": ""}],
        }
        warnings = validate_brief(brief, max_batch_size=50)
        self.assertEqual(len(warnings), 3)
        self.assertTrue(any("No brand assets" in warning for warning in warnings))
        self.assertTrue(any("no description" in warning for warning in warnings))
        self.assertTrue(any("75 assets" in warning for warning in warnings))

    def test_empty_deliverables_are_a_warning_not_a_parse_error(self):
        brief = {**VALID_BRIEF, "deliverables": []}
        self.assertIn("No deliverables specified", validate_brief(brief))

    def test_batch_limit_must_be_a_positive_integer(self):
        with self.assertRaisesRegex(ValueError, "max_batch_size"):
            validate_brief(VALID_BRIEF, max_batch_size=0)


if __name__ == "__main__":
    unittest.main()
