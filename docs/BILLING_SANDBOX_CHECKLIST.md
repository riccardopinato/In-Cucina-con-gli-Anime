# F4B Billing sandbox proof

F4B code is not considered PASS until one real store sandbox purchase and one restore are observed.

## Fixed app-side configuration

- package: `com.riccardopinato.animekitchen`
- one-time product ID: `remove_ads_lifetime`
- production/default billing: OFF
- sandbox verification: OFF by default
- Web: no-op adapter
- native transport: `in_app_purchase`

The dedicated sandbox APK is built with:

```text
ANIME_KITCHEN_BILLING_ENABLED=true
ANIME_KITCHEN_BILLING_SANDBOX=true
ANIME_KITCHEN_LIFETIME_PRODUCT_ID=remove_ads_lifetime
```

Never ship a production candidate with `ANIME_KITCHEN_BILLING_SANDBOX=true`.

## Google Play Console setup required

- [ ] Create/select the Play Console app with package `com.riccardopinato.animekitchen`.
- [ ] Create a one-time product with ID `remove_ads_lifetime`.
- [ ] Choose the commercial price in Play Console.
- [ ] Activate/publish the one-time product so it can be queried by testers.
- [ ] Add the test Google account under Play Console license testing.
- [ ] Keep the test account signed into Google Play on the Android test device.

Google recommends internal testing for pre-distribution validation. License testers can also sideload debug builds for billing testing when the package matches the Play Console app.

## Evidence required for F4B PASS

On an Android device with Google Play:

1. Install the CI artifact `anime-kitchen-billing-sandbox-debug`.
2. Open Settings -> Remove ads forever.
3. Verify the real store title/price loads.
4. Complete the test purchase.
5. Verify the app reports Lifetime active.
6. Restart the app offline and verify Lifetime remains active from the offline cache.
7. Reinstall/clear app data.
8. Use Restore purchase.
9. Verify Lifetime becomes active again.
10. Record the tested app version, commit SHA and result in the PR.

Expected safety checks:
- cancel does not grant Lifetime;
- failed/unverified purchase does not grant Lifetime;
- Lifetime makes `ProductLimits.canRequestAds` false;
- Web Preview never invokes native billing.
