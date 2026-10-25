# Android persistent signing — update in place

Status: VERIFIED on 2026-10-25 — persistent Android signing and physical update-in-place continuity confirmed.

## Goal

Internal Android APKs must be installable over the previous APK without uninstalling the app or deleting local data.

Android requires both:
- the same application ID;
- the same signing certificate.

This project already has a stable application ID:

`com.riccardopinato.animekitchen`

The previous CI lane regenerated the Flutter Android scaffold on every run and therefore used the runner's ephemeral debug keystore. That made APK signatures unstable between runs.

## Persistent identity

A private keystore has been generated outside the repository. It must never be committed.

Public certificate SHA-256:

`DE:E1:CC:45:2B:F6:08:9D:67:98:D9:23:1F:21:DD:A5:C8:88:81:16:8B:07:B3:58:9B:F6:4B:E1:99:A1:22:5A`

Required GitHub Actions Secrets:

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

The workflow restores the private keystore only inside the runner and writes an ignored `android/key.properties` file. The generated Gradle scaffold uses that persistent identity when all four secrets exist.

If none of the secrets exists, development CI falls back to ephemeral debug signing and labels the APK artifact accordingly. A partially configured secret set fails closed.

## Version code

The CI Android build passes:

`--build-number="$GITHUB_RUN_NUMBER"`

The Development checks workflow run number is monotonically increasing, so later APK artifacts have a higher Android versionCode than earlier artifacts from the same workflow.

## Verification

Every Android build publishes an identity report containing:
- source commit SHA;
- workflow run number;
- signing mode;
- signer certificate DN;
- signer SHA-256.

For persistent builds, the signer SHA-256 must equal the public fingerprint above.

## Migration boundary

APK versions already installed from the old ephemeral-signing lane cannot be upgraded by the new persistent key because the old private signing key is not recoverable.

Therefore one final uninstall/reinstall is required when moving to the first persistent-signed APK.

After that migration, future persistent-signed APKs can update in place as long as:
- the package ID remains unchanged;
- the same keystore is used;
- versionCode keeps increasing.

## Play Store boundary

If Google Play App Signing later uses a different app-signing certificate, a Play-installed build and a directly sideloaded GitHub APK may not be mutually updateable. Treat the persistent key generated here as the stable direct-distribution identity and, if desired, as a candidate Play upload key; verify the final Play signing architecture before production rollout.


## Verification evidence

Verified on GitHub Actions run `40148542064`:

- workflow run number: `83`;
- signing mode: `persistent`;
- artifact: `in-cucina-con-gli-anime-arm64-persistent`;
- certificate DN: `CN=RP Digital Studio, O=RP Digital Studio, C=IT`;
- certificate SHA-256: `DE:E1:CC:45:2B:F6:08:9D:67:98:D9:23:1F:21:DD:A5:C8:88:81:16:8B:07:B3:58:9B:F6:4B:E1:99:A1:22:5A`.

This matches the documented persistent certificate exactly.


## Physical device evidence — first persistent install

User-confirmed on 2026-10-25:

- the persistent-signed Android APK launches and works correctly on the physical phone;
- the newly added recipe artwork renders correctly on-device;
- no artwork defect was reported in the current twenty-recipe catalog.

This closes the first-install runtime check for the persistent signing lane, but it does **not** yet prove update-in-place continuity.

The next acceptance check is:

1. produce a later persistent-signed APK with a higher Android versionCode;
2. install it over the currently installed persistent-signed APK **without uninstalling**;
3. confirm launch succeeds and existing local user state remains available.

Only after that physical check may update-in-place be marked VERIFIED.


## Physical update-in-place verification — PASS

Verified by the user on 2026-10-25 using a later persistent-signed APK built with a higher Android versionCode:

- the newer APK installed over the existing app without uninstalling it;
- the app launched normally after the update;
- existing Favorites were preserved;
- the package/signing continuity therefore supports in-place updates for the current direct-distribution lane.

Result: **UPDATE-IN-PLACE VERIFIED**.

This evidence closes the persistent-signing continuity gate for direct APK updates. It does not by itself establish Play Store readiness, production AAB certification or Google Play App Signing continuity.
