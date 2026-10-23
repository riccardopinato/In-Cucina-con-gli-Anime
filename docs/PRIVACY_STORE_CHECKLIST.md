# Privacy / consent / store checklist

This document is intentionally separate from runtime logic.

## F4A runtime boundary

- [x] Local ad-privacy preference is persisted.
- [x] Provider consent eligibility is not persisted as trusted runtime truth.
- [x] Every app launch starts with provider consent unresolved until a provider adapter resolves it.
- [x] Ad requests are fail-closed unless both the local preference and provider gate allow them.
- [x] Core recipe browsing/cooking remains available with consent unresolved or blocked.
- [x] No account is required for the core catalog.
- [x] Development/tests do not depend on live ad inventory.
- [x] No AdMob or billing SDK is mounted in F4A.

## Before native advertising is enabled

- [ ] Add a provider adapter behind the consent seam.
- [ ] For Google UMP, refresh consent information on every launch.
- [ ] Read provider ad eligibility only after the refresh/form flow resolves.
- [ ] Keep Privacy Options reachable when the provider requires an entry point.
- [ ] Use test traffic only for debug, QA, automation and manual validation.
- [ ] Keep Web Preview on a no-op/stub provider boundary.
- [ ] Verify denied/unresolved/failure paths never block app startup or cooking.

## Before store candidate

- [ ] Publish a real privacy policy URL and verify it is reachable.
- [ ] Complete store privacy/data-safety declarations from actual runtime behaviour.
- [ ] Configure and publish the required provider privacy/consent message.
- [ ] Verify targeting/languages match the app markets and supported locales.
- [ ] Confirm age/audience treatment explicitly; do not inherit donor settings.
- [ ] Add app-ads.txt / provider readiness checks when required.
- [ ] Re-test privacy-choice revocation on a physical Android device.
- [ ] Keep production IDs/secrets outside source control.
