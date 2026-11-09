"""Non-network regressions for strict production/validation API separation."""
from __future__ import annotations

import unittest

from grading.quality.validation_credentials import (
    ValidationCredentialError,
    require_validation_key,
    validation_provider_environment,
)


class ValidationCredentialsTests(unittest.TestCase):
    def test_default_validation_is_offline_even_with_production_key(self):
        isolated = validation_provider_environment({
            "GEMINI_API_KEY": "expensive-production-key",
            "GOOGLE_API_KEY": "production-alias",
            "CLOVA_API_KEY": "production-clova",
            "VALIDATION_GEMINI_API_KEY": "independent-validation",
        })
        for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY",
                     "GOOGLE_GENERATIVE_AI_API_KEY", "CLOVA_API_KEY"):
            self.assertNotIn(name, isolated)
        self.assertEqual(isolated["VALIDATION_CREDENTIAL_CONTEXT"], "isolated")
        self.assertNotIn("VALIDATION_GEMINI_API_KEY", isolated)

    def test_validation_key_is_never_production_key_or_alias(self):
        for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY",
                     "GOOGLE_GENERATIVE_AI_API_KEY", "CLOVA_API_KEY"):
            with self.subTest(name=name):
                env = {
                    "VALIDATION_LIVE_API": "1",
                    "VALIDATION_GEMINI_API_KEY": "same-token",
                    name: "same-token",
                }
                with self.assertRaisesRegex(
                    ValidationCredentialError,
                    "validation_credential_reuses_production_key",
                ):
                    require_validation_key("gemini", env)
                with self.assertRaises(ValidationCredentialError):
                    validation_provider_environment(env)

    def test_distinct_validation_gemini_only_maps_to_provider_legacy_name(self):
        isolated = validation_provider_environment({
            "VALIDATION_LIVE_API": "1",
            "GEMINI_API_KEY": "production-gemini",
            "GOOGLE_API_KEY": "production-google",
            "CLOVA_API_KEY": "production-clova",
            "VALIDATION_GEMINI_API_KEY": "validation-gemini",
        })
        self.assertEqual(isolated["GEMINI_API_KEY"], "validation-gemini")
        self.assertNotIn("GOOGLE_API_KEY", isolated)
        self.assertNotIn("CLOVA_API_KEY", isolated)

    def test_no_validation_key_means_no_implicit_fallback(self):
        isolated = validation_provider_environment({
            "VALIDATION_LIVE_API": "1",
            "GEMINI_API_KEY": "prod-only",
            "CLOVA_API_KEY": "prod-only-2",
        })
        self.assertNotIn("GEMINI_API_KEY", isolated)
        self.assertNotIn("CLOVA_API_KEY", isolated)
        with self.assertRaisesRegex(
            ValidationCredentialError, "missing_validation_gemini_api_key",
        ):
            require_validation_key("gemini", {
                "VALIDATION_LIVE_API": "1",
                "GEMINI_API_KEY": "prod-only",
            })

    def test_clova_validation_uses_distinct_credential(self):
        isolated = validation_provider_environment({
            "VALIDATION_LIVE_API": "1",
            "CLOVA_API_KEY": "production-clova",
            "CLOVA_APIGW_API_KEY": "production-legacy",
            "VALIDATION_CLOVA_API_KEY": "validation-clova",
            "VALIDATION_CLOVA_APIGW_API_KEY": "validation-clova-legacy",
        })
        self.assertEqual(isolated["CLOVA_API_KEY"], "validation-clova")
        self.assertEqual(isolated["CLOVA_APIGW_API_KEY"], "validation-clova-legacy")


if __name__ == "__main__":
    unittest.main()
