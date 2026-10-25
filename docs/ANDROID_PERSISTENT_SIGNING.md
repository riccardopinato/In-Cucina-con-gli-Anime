# Android persistent signing — update in place

Status: VERIFIED on 2026-10-25 — persistent Android signing active in CI.

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
