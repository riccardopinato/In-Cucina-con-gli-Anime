# Content and rights policy

The app is intended to be monetizable, but editorial tracking must stay proportionate to the actual workflow.

## Recipe workflow

Production recipes may be:

- `original`: created for this app;
- `inspired`: created from a dish, scene, idea or culinary reference;
- `adapted`: developed from recipe/reference material supplied for editorial processing.

When reference material is supplied, it is treated as culinary/editorial input. Raw copied prose, scans, screenshots, PDFs or book/site text remain transient working material and should not be committed to the repository.

The committed authoring record contains normalized culinary facts and fresh app editorial wording rather than source prose reproduced or sentence-by-sentence paraphrased for publication.

The catalog records only `contentOrigin` plus an optional internal `sourceNote`; F2 does not introduce a heavy recipe-provenance database.

The project does not claim that rewriting/paraphrasing source expression automatically transfers copyright ownership.

## Duplicate/variant review

Similarity analysis compares normalized recipe structure to prevent accidental duplicate publication. It is not a rights determination.

A similarity score never authorizes automatic deletion, overwrite or publication. Ambiguous/blocking cases require an explicit review decision tied to the compared content fingerprints.

## Visual/media rule

Prefer:

- original food photography;
- original illustrations/branding;
- verified public-domain or rights-compatible source material;
- licensed third-party assets when intentionally acquired.

Authoring image references resolve through a small asset registry recording `original | public_domain | licensed`.

Do not ship anime screenshots, posters, manga panels, logos, music or modern character artwork without a rights basis.

F3C decorative characters use original procedural Flutter illustrations of traditional Japanese/Chinese archetypes. The implementation does not copy or reference a specific modern anime/game character design. Future imported character artwork must still be separately verified as original, public-domain/rights-compatible or licensed.

## References to works

Factual titles of anime/manga or traditional works may be stored as inspiration/reference metadata. The product should not imply official affiliation, sponsorship or endorsement.

## Current state

F3 ships all 10 production recipes from the user-provided reference document as fresh editorial rebuilds, plus original procedural recipe artwork and decorative folklore mascots. The synthetic authoring fixture remains preview/test-only and is restored out of the production catalog after preview builds.
