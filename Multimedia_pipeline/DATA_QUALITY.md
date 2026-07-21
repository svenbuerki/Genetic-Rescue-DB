# LEPA database — data-quality status

Single source of truth for the data-quality state of `LEPA_SQL.db`. Last QA pass: **2026-07-21**
(July-16/17/20 loaded + verified — EO26 complete, EO27 loc 37/50, EO61 loc 38 + EO29 loc 8; the 2026 collection season is essentially complete).
Tracked issues live on GitHub (**svenbuerki/Genetic-Rescue-DB**); each item below links to its issue.

## Integrity — clean ✅

A full audit (2026-06-27) found no structural problems:

| Check | Result |
|---|---|
| Orphan/broken FKs (Multimedia, Phenotyping, Germplasm → Occurrences) | **0** |
| `Phenotyping.multimediaID` → missing Multimedia | **0** |
| Duplicate Phenotyping rows (per occurrence) | **0** |
| Duplicate images (same SHA-256 content) | **0** |
| Locations missing GPS (`locationDecimalLatitude/Longitude`) | **0** of 39 |
| Locations with null `EOID` | **0** |
| Tables documented in `TableModules` | **30 / 30** (all real tables) |
| Photo-date (EXIF) vs `occurrenceDate`, where EXIF present | **0 mismatches** of 77 checkable |
| Genotyping FK chain: `GenotypingStatus`/`TissueBank` → Occurrences; `MolecularBank` → TissueBank; `Sequencing` → MolecularBank | **0** orphans |

## Coverage

- **Occurrences:** 3767. **Events:** 714. **Locations:** 49.
- **Phenotyping:** 2282. **Multimedia:** 3352 (incl. field-form images).

## July 16 / 17 / 20 2026 — EO26 complete + EO27 (loc 37/50) + EO61/EO29 (loaded 2026-07-21)

Three field days loaded together (forms all imaged 07-21; boards day-foldered). **143 occurrences (3700–3842, fully contiguous), 0-orphan, 143/143 imaged + phenotyped. 56 events (660–715), 3 new locations.** Heavily board-driven (noisy forms); all 56 events reconciled.

- **Stage A:** loc **33, 34** (EO26-3) + loc **37** (EO27-1) revisits; **+3 new locations** — **48, 49** (EO26) and **50** (EO27); **+56 Events** (barcode-decoded) incl. 4 data-only events with 0 occurrences (below); **+143 Occurrences** (3700–3842). +120 form images.
- **Stage B:** +143 Multimedia + 143 Phenotyping (size class 49 small / 65 medium / 29 large).
- **By day:** 07-16 EO26 Rabbit Creek (loc 33/34/48/49, 54 plants) — EO26 completed; 07-17 EO27 "Region 3" (new loc 50 + loc 37, 55 plants); 07-20 Mountain Home (loc 38 EO61 + loc 8 EO29, 34 plants).

### Corrections / notes
- **EO61 (loc 38) data-only slick spots:** events **709, 710, 711, 713** carry full slick-spot data (area, coverage, fruiting/rosette counts, GPS, associated veg) but **0 seed collections** — intentional, for effective-population-size analysis (Sam's protocol). Loaded as events with no occurrences.
- **event 691:** OCR read it on the loc-48 sheet, but its sticker **barcode decodes to 681** (loc 48); 691 is a genuine separate loc-37 event. No real reuse.
- **occurrence 3753:** its board was mis-labeled event 686 (a July-17 loc-50 event) → corrected to event **685** (loc 49) per the form and the off-by-one board write.
- **loc-50 event latitudes (687/688/689):** field-recording errors (well off the loc-50 cluster) → set to a provisional cluster latitude with an `eventRemarks` note; longitude as recorded. **Tracked as [#18](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/18) — verify against the manilla and finalize.**
- **loc 36 (EO26-4) & loc 35:** visited-but-not-sampled / not-visited on 07-16 → **0 records by design** (matches Ian's email).
- **New candidate taxa flagged for Teo** (held out of `Taxonomy`, verbatim kept): **horsebrush** (*Tetradymia*), **sand dropseed** (*Sporobolus*), **bluebunch wheatgrass** ("bluebun", *Pseudoroegneria*). Resolved to known taxa via the lexicon: *Tragopogon dubius* (48), squirreltail (36), basin wild rye (13), mustard (27).
- **July 17 had no field email** — the day's records were reconstructed from the forms + boards and loaded cleanly (EO27, new loc 50 + loc 37).

## Manilla-verified event-GPS corrections (Teo, applied 2026-07-20)

Teo found bad event coordinates while map-making and cross-checked each against the field manilla envelopes (and prior-year points). **12 events corrected** — 242, 249, 255, 256, 258, 259, 260, 272, 293, 431, 432, 454 — each a single- or two-field transcription slip (wrong leading digit, transposed digit, or dropped sign). Every DB value matched Teo's reported "current" value before the change (sanity-checked). Coordinates live in the DB only; see `PIPELINE_LOG.md` for the qualitative log.

## July 15 2026 — EO8 loc 47 (new, completed) + EO26 loc 31 & 32 (loaded 2026-07-20)

The crew completed **EO8** by finishing the new **location 47** (started 07-14) and moved to **EO26 (Glenns Ferry)**. **138 occurrences loaded** — 30 deferred loc-47 boards from 07-14 + 108 from 07-15. **0-orphan, 138/138 imaged + phenotyped.** Heavily board-driven: the loc-47 forms were captured badly out of order (an orphan/crossed-out page-2, one event with no page-2), so occurrences came from the boards and all 40 events reconciled.

- **Stage A:** **+1 new location 47** (EO8, EOID 15, GPS from its sheet) + loc 31 & 32 (EO26-3) revisits; **+40 Events** (620–659, barcode-decoded); **+138 Occurrences** (3561–3699 — contiguous except occ **3608 skipped by the crew**, confirmed by both boards and form event 635 which lists 3606/3607/**3609**). +82 form images.
- **Stage B:** +138 Multimedia + 138 Phenotyping (image scale cross-checked the field-written board H/W; size class 65 small / 52 medium / 21 large).
- **loc 47 spanned two field days** (events 620–628 = 07-14, 30 plants; events 629–646 = 07-15, 64 plants) — loaded whole today to keep Stage A/B consistent. loc 47 total = 94 plants.

### Corrections recorded
- **loc 30 (EO26-1) visited, not sampled:** all plants too far gone → **0 records by design** (like loc 29 on 07-14). No loc-30 form or boards.
- **event 634 & event 636 latitude** (both loc 47): the field-recorded latitudes sit ~9 km north of every sibling event (longitude fine) — set to a provisional loc-47 cluster latitude with an `eventRemarks` note; longitude as recorded. Event 626's "7/4" date slip corrected to 07-14.
- **New candidate taxa flagged for Teo** (held out of `Taxonomy`, verbatim kept): **ephedra** (*Ephedra* / Mormon tea, event 629), **hedgehog cactus** (event 643). Other OCR "unknowns" were spelling variants of known taxa (Sandberg, sagebrush, Sisymbrium, burr buttercup, L. perfoliatum, crested wheatgrass, green rabbitbrush, crust, and **bottlebrush squirreltail = Elymus elymoides, taxonID 36**) — added to the lexicon.

## July 14 2026 — EO8 loc 27 + loc 28 (loaded 2026-07-20); new loc 47 deferred

Second EO8 day: the crew completed **loc 28** (continuing from July 13), completed **loc 27**, and opened a **new location 47**. **55 samples loaded** (loc 28 = 40, loc 27 = 15); **0-orphan, 55/55 imaged + phenotyped.** 85 boards imaged in-field 07-14 (JCN_1433–1524); 57 Peggy HEIC forms → JPG imaged 07-15.

- **Stage A:** loc 27 revisit (first 2026 location sheet) + loc 28 continuation; **+28 Events** (592–619, all CODE128-decoded, no gaps); **+55 Occurrences** (3506–3560, contiguous from the July-13 max 3505); +57 form images.
- **Stage B:** +55 Multimedia + 55 Phenotyping (image scale cross-checked the field-written board H/W to ~±1 cm; size class 24 medium / 21 small / 10 large).
- **Board-driven load; forms + boards reconciled on all 28 events.**

**New location 47 (30 plants, occ 3561–3590, events 620–628) deferred to the July-15 load.** loc 47 was boarded in-field Tuesday (boards JCN_1495–1524, already ingested to `Multimedia_main`) but its **event/location forms were not in this batch** — loc 47 completes on Wednesday (07-15) and all its forms were imaged together with the 15th. Loading loc 47 whole on July 15 keeps Stage A/B consistent. Ian's reported "87 (or 84)" samples = 55 loaded + 30 deferred = 85 boarded.

### Corrections recorded (settled by the plant boards)
- **loc 29 visited, not sampled:** Ian reported reaching loc 29 (Rye Grass Rd) but all plants had dropped their seeds → **0 seed samples, no event/occurrence records by design** (the boards carry only loc 28 and loc 27).
- **event 602 location:** form location-barcode OCR read "0029"; the form itself reads **0028**, its GPS sits in the loc-28 cluster, and all three of its boards say loc 28 → event 602 = **loc 28** (there is no loc-29 event — this was the "loc 29" phantom).
- **event 604 occurrences:** form p2 OCR read 3552/3553/3554 (colliding with event 614's genuine 3552/3553); the boards read **3532/3533/3534**, which makes the whole day contiguous 3506–3560 with no gaps or duplicates. Board values used.
- **taxonomy:** event 609's "sandburgs bluegrass" = a misspelling of Sandberg's bluegrass (taxonID 12); homogenized via the lexicon, no new `Taxonomy` rows. No candidate taxa for Teo this day.
- **EOID consistency:** the loader stages EO8 occurrences with `EOID='?'` because `locationCode` "EO8" ≠ `EOs.EOCode` "EO08". July-14 EO8 occurrences were set to the correct **EOID 15**, and the 123 July-13 loc-28 occurrences ('?' → 15) were swept in the same load so all EO8 occurrences now carry EOID 15 (`Occurrences.locationID` → `Locations.EOID` remains the authoritative join regardless).

## July 13 2026 — EO8 Hammett Hills, loc 28 (loaded 2026-07-16): first eastern-population load

The crew's move east after finishing the OCTC. **123 samples, one location, one day — the biggest single-day load of the season.** loc 28 (EO8, Hammett Hills) is a **revisit** (sampled 2025). **0-orphan, 123/123 imaged + phenotyped.** Peggy's 109 HEIC forms → JPG (`sips`), imaged 2026-07-15 (form images datestamp `LEPA_2026-07-15_*`). 123 boards (JCN_1308–1432).

- **Stage A:** loc 28 revisit; **+54 Events** (538–591, all CODE128-decoded, no gaps); **+123 Occurrences** (3383–3505, contiguous — continuing straight from the OCTC max 3382); +109 form images.
- **Stage B:** +123 Multimedia + 123 Phenotyping (every board field-tape H/W + image scale).
- **Board-driven load; forms + boards reconciled on all 54 events.** The forms' OCR'd occurrence lists were noisy (rotated pages, looped-9→4, and several agents second-guessing the 4-digit numbers), so occurrences were taken from the boards and cross-checked; every event matched.

### The whiteboard-duplicate that resolved itself
Ian pre-declared (email 07-13): *"after occurrence 4321 I forgot to update the occurrence number, so it appears twice. The second should be 4322."* On inspection: the numbering is actually **3421/3422** (Ian's "43xx" was a leading-digit slip — both forms and boards read the 3300s–3500s), and because the boards were imaged 07-15 (two days later), **Isaac had already applied the correction** — the boards show 3421 and 3422 each exactly once, and event 551's form even carries the handwritten note *"change to 3422."* Nothing to fix on load; both occurrences link to distinct plants (JCN_1346 = 3421, JCN_1347 = 3422).

**Four new candidate taxa flagged for Teo** (new to this eastern habitat; verbatim kept, held out of `Taxonomy`): **snakeweed** (*Gutierrezia*?, events 552/553), **lupine** (*Lupinus*?, event 552), **penstemon** (event 559), **rush** (*Juncus*?, event 559). Other OCR "unknowns" were artifacts of known taxa (rabbitbrush=17, crested wheatgrass=15, tumble mustard=5, Descurainia=46).

## July 10 2026 — OCTC wrap-up (loaded 2026-07-16): EO27-1 loc 45 & 46 (new) + EO67 loc 39 (revisit)

Ian's final OCTC day, mostly in Range-Fire-burned ground (low numbers expected). **0-orphan, 37/37 imaged + phenotyped.** Board-driven occurrence assignment; forms and boards reconciled on all 11 events. Forms were Peggy's HEIC (→JPG via `sips`), imaged 2026-07-13 (Sven traveling), so form images datestamp `LEPA_2026-07-13_*`.

- **Stage A:** **+2 new Locations** (**45** = EO27-1, east of the Red Tie exclosure loc 12; **46** = EO27-1, western edge) + **loc 39 EO67 revisit**; **+11 Events** (527–537); **+37 Occurrences** (3346–3382, contiguous); +25 form images.
  - Split: loc 45 → 7 events / 21 occ; loc 46 → 2 events / 10 occ; loc 39 (EO67) → 2 events / 6 occ. *(Ian's email estimated ~7 for EO67; forms + boards agree on 6 — his rough field count.)*
  - Burned-area events (528–533, 536, 537) legitimately have **size 0 and condition N/A** (no differentiable slick spot in the burn); recorded as such with the crew's burn notes in `eventRemarks`.
- **Stage B:** +37 Multimedia + 37 Phenotyping (every board field-tape H/W + image scale).

### Corrections recorded (each carries an `eventRemarks`/`locationRemarks` note)

| Item | Correction | Basis |
|---|---|---|
| **Loc 46 latitude** | Location sheet's latitude had a single-digit slip inconsistent with its own two events by ~6.6 km; corrected to match the events. Longitude as written. | direct read + event consistency |
| **Events 527, 528, 530** | Latitude OCR outliers (off by whole tenths/hundredths of a degree from the site) re-read to the loc-45 cluster; flagged PROVISIONAL. | direct read |
| **ev 536 occ list** | Form page-2 read "5377–5379"; boards give **3377–3379** (5→3 misread). | boards |

**Two taxa flagged for Teo** (verbatim kept in `associatedTaxaOriginal`): **"Helianthus sp."** (event 528 — a legible, genuine new candidate = annual sunflower, plausible in burned/disturbed ground; not in `Taxonomy` yet) and **"thistle mangt?"** (event 536 — genuinely illegible, not guessed). All other OCR "unknowns" this load were bracket-annotation artifacts of known taxa (cheatgrass, Poa→Sandberg).

This closes the **OCTC / EO27 season** (Ian's crew moves to eastern populations next). **EO77 was searched and empty → no `EOs` row created**, as expected.

## EO27-1 "Red Tie South" (loc 11) — July 9 2026 (loaded 2026-07-10)

Ian's full day across a new area of **EO27-1 "Red Tie South"** (the "Location 13" the field plan named, corrected to **loc 11** after the collision was flagged — see below). Per Ian: EO27-1 "Red Tie South" comprises **locations 11, 12, 37**; the bare term "Red Tie" is reserved for **loc 12** (the exclosure). Single location, 32 events. **0-orphan, 125/125 imaged + phenotyped.** The occurrence assignment was **board-driven** (the boards ran perfectly sequential 3221–3345), with the forms supplying event metadata; the two crew-flagged occurrence corrections were confirmed by the boards.

- **Stage A:** loc 11 **revisit** (no insert; `EO27-1`, Orchard, previously sampled 2025 only), **+32 Events** (495–526, all CODE128-decoded — one sticker, 525, didn't scan and was placed by capture order + confirmed by its boards), **+125 Occurrences** (3221–3345, contiguous), **+65 form images** (Sven's Pixel, `PXL_20260710` → datestamped `LEPA_2026-07-10_*`, the imaging date).
- **Stage B:** +125 Multimedia + 125 Phenotyping. Every board carried field-written H/W and an image scale; no stray/other-day images; no missing plants.

### Corrections recorded (each carries an `eventRemarks` note)

| Event | Correction | Authority |
|---|---|---|
| **515** (occ 3288) | Form page-2 occurrence number illegible (read like "528/5286"); board reads **3288** cleanly. | **Board** (matches Sven's pre-load correction) |
| **512** (occ 3274–3276) | Confirmed 3274/3275/3276. | Board + form + Sven's pre-load note |
| **501** | Latitude illegible/inconsistent on the form; filled with the **midpoint of bracketing events 500 & 502**, flagged PROVISIONAL (longitude was legible). | post-hoc, per the [#16](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/16) convention |
| **519–524** | Event GPS **re-read directly from the forms** — a subagent OCR batch systematically misread the longitude prefix (a looped "11" as "4", giving spurious −116.48xx) and shifted several latitudes. Direct reads restored the true −116.11–12xx values. | direct read |
| **503** | Slick-spot condition hand-written `1.5`; recorded as **1** (integer 1–4 scale). | convention |

**Taxa flagged as "unknown" — all resolved by reading the forms (2026-07-10):** the OCR sweep produced three unknown tokens; reading the actual sheets (Sven transcribing) showed **all three were OCR misreads of taxa already in `Taxonomy`** — no new taxa were needed. Each corrected in place (taxonID added, verbatim fixed, `eventRemarks` note):
- **"Ernst" → crust** (biological soil crust, taxonID 35) on events 507/509/510/511/512.
- **"stiff flax" → Atriplex** (saltbush, genus-level taxonID 25; species not determined) on event 500.
- **"blanketflower" → bur buttercup** (*Ceratocephala testiculata*, taxonID 9) on event 503.

*Lesson: an OCR "unknown taxon" is usually a misread of a common known one (here crust, Atriplex, bur buttercup all appear on nearly every sheet) — read the form before treating it as a new species.*

**Location-13 → loc 11 (resolved 2026-07-09, loaded here):** the field plan named "Location 13" for this new EO27-1 area, but loc 13 is **EO30-1** (a different EO). Ian confirmed the crew is in **location 11**; loaded as the loc-11 revisit. (EO27-1 "Red Tie South" spans loc 11, 12, 37; the boards all read L11.)

**Ian's weekly confirmation (2026-07-10):** "125 samples… no white board corrections" — consistent with the clean, sequential board sweep loaded here. Sven's two pre-load corrections matched the boards (they fixed illegible *form* readings, not whiteboards). Loc 37 (also EO27-1) burned in the 2025 Range Fire and may not be sampled in 2026.

## EO27 Figgins (loc 9) + new EO27 site (loc 44) + Pleasant Valley (loc 10) — July 8 2026 (loaded 2026-07-09)

Ian's ~104-sample day across three EO27 sites. **0-orphan, 103/103 imaged + phenotyped**, and — for the first time this season — the **forms and the boards agreed on every one of the 32 events** once two isolated digit errors were corrected.

- **Stage A:** +1 new Location (**44 = EO27**, GPS recorded from the location sheet; loc 9 Figgins + loc 10 Pleasant Valley revisits), **+32 Events** (463–494, all CODE128-verified, no gaps), **+103 Occurrences** (3118–3220), **+67 form images** (Peggy's iPhone HEIC → JPG; datestamped `LEPA_2026-07-09_*` = the imaging date).
  - Event split: loc 9 → 24 events / 79 occ; loc 44 → 6 events / 17 occ; loc 10 → 2 events / 7 occ.
- **Stage B:** +103 Multimedia + 103 Phenotyping. Every board carried field-written H/W and a usable image scale; no stray/other-day images (date cross-check clean), no missing plants.
- **Form-set completeness audit (pre-load):** 3 location pages + 32 event p1 + 32 event p2 = **67, a complete set** — nothing to request from the field crew.

### Corrections recorded (each carries an `eventRemarks` note)

| Event | Correction | Authority |
|---|---|---|
| **472** (occ 3143) | Board **JCN_1052** hand-written `3142` — a duplicate of event 471's last plant. Corrected to **3143**. | **Form** (Ian: "no errors with the occurrence-number envelopes… just a white-board photo mistake") |
| **494** (occ 3218–3220) | Page-2 occurrence numbers hand-written `3118/3119/3120` (2-read-as-1). Corrected to **3218/3219/3220**. | **Boards** |
| **472** | Longitude illegible and inconsistent with the site (the read value breaks the longitude pattern of every bracketing event). Filled with the **midpoint of bracketing events 471 & 473**, flagged PROVISIONAL. | post-hoc, per the [#16](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/16) convention |
| **464, 489, 492** | Form dates hand-written `07-09`, `08-07` (transposed), `07-09`. Normalized to **07-08-2026**. | event-sticker sequence + Ian's report |
| **471** | Slick-spot condition hand-written `2.5`. Recorded as **2** (scale is integer 1–4). | convention |

**Note the inversion:** on July 6 the *boards* were authoritative over garbled forms; here the *form* was authoritative over a mis-written board. Neither source is categorically reliable — the two must always be cross-checked, and the physical envelope number is the tie-breaker.

**Flagged, not blocking:** the Pleasant Valley (loc 10) location sheet carries a hand-written barcode `500010` where the printed barcode reads `0010`, and its lat/long are recorded at low precision (3 decimal places, vs 6-7 elsewhere). Worth a word to the field crew.

**Location-13 clash — averted, resolved 2026-07-09.** The field plan named "Location 13" for a new EO27-1 area, but loc 13 is already **EO30-1** (a different EO, 39 occurrences over two seasons). Flagged before any load; **Ian confirmed the crew is in location 11** (`EO27-1`, sampled 2025 only) and that the sample records are correct. No data change was required — loc 11 will load as a revisit. *(EO27-1 exists at two locationIDs, 11 and 37; the boards should read L11.)*

## EO27 Red Tie (loc 12) + EO27-5 (loc 43) — July 6/7 2026 (loaded 2026-07-08; closes [#15](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/15))

The held July-6 Red Tie boards + the July-7 completion + the new EO27-5 site, loaded together once the loc-12 forms arrived. **0-orphan, 159/159 imaged + phenotyped.**
- **Board-driven reconciliation:** the July-6 Red Tie **form** occurrence lists were badly OCR-garbled (looped-9→4, overlaps, a stray "2133"); resolved by sweeping **all 159 boards** (held Red Tie 0800-0893 + July-7 0947-1020) for the authoritative OC↔EV mapping. The July-7 form occurrence lists matched the boards exactly. All 43 event stickers CODE128-verified.
- **Stage A:** +1 new Location (**43 = EO27-5**; loc 12 EO27RT revisit), **+43 Events** (409-430, 433-448, 458-462), **+159 Occurrences** (Red Tie 2909-2995 + 3046-3084; EO27-5 3085-3117), +88 form images (Sven's Pixel, `PXL_20260708`).
- **Stage B:** +159 Multimedia + 159 Phenotyping (field-tape H/W on every board). +2 "New Location Truck Images" (JCN_0946, JCN_1021) linked to loc 43 as context (`NEEDS CURATION`).
- **occ-2909/2897 fully resolved ([#17](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/17) closed):** the real Red Tie plant took **2909**; the EO32 event-404 plant (board+form read 2897) was parked at 9001, then **restored to its true number 2897** after we found EO69's 2897 was *spurious* — the EO69 event-265 field sheet stops at 2896, and its 2897 had no image/tissue/DNA (a synthetic over-assignment from the July event-265 reconciliation). Removed the phantom EO69 2897 (EO69 event 265 now = 2379-2382, 2894-2896) and reassigned the EO32 plant 9001→**2897**; 9001 retired. (Lesson: synthetic/lab reassignments must draw from a **reserved high block**, never the live field-number range.)

## EO30 complex — July 6 2026 (loaded 2026-07-07)

Simco Rd, sampled after EO27 Red Tie the same morning (Red Tie held — see below). Two-stage load, verified **0-orphan, 50/50 imaged + phenotyped**:
- **Stage A** (`field_forms_ocr.py`): 24 forms (Peggy's phone, **HEIC→JPG via `sips`**) → **+1 new Location** (42 = EO30-2; loc 13 EO30-1 is a revisit), **+11 Events** (431, 432, 449–457, all **CODE128 barcode-verified**), **+50 Occurrences** (2996–3045), +24 form images. Event 449's form OCR read loc "0044" → **plant boards confirm loc 42** (OCR slip); remark added. Event 457 condition 2.5→2. `associatedTaxa` homogenized, no new taxa.
- **Stage B** (`stageB_load.py`): 50 EO30 boards (JCN_0896–0945) → **+50 Multimedia + 50 Phenotyping** (22 small / 28 medium; all field-tape H/W). Board OC/EV/EO/L# all matched the forms exactly.
- **Missing event GPS — [#16](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/16):** events **405** (EO32) and **451** (EO30-2) had NULL lat/long (**blank on the forms**; boards carry no GPS). Per Ian's guidance (event numbers run sequentially along the travel route), each is filled with a **post-hoc midpoint of its bracketing events** (405 = mid of 404/406; 451 = mid of 450/452). **PROVISIONAL** — flagged in `eventRemarks`; true fix needs a **site revisit** (EO30 easier than EO32). *Process fix going forward: confirm lat/long is written on every event form.* (Older: event 13, 2025, still NULL.)
- **Form-image datestamp fix:** Peggy's iPhone writes `IMG_####` (no date in filename) vs the Pixel's `PXL_<date>`; `--forms-mm` was falling back to a stale hardcoded date. Fixed to derive the datestamp from **EXIF capture = the imaging date** (forms are photographed ~1 day after fieldwork; these = 2026-07-07). The 24 already-loaded form images were renamed to `LEPA_2026-07-07_*`.

### HELD — EO27 Red Tie (loc 12), July 6 — [#15](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/15)

The 137-image board upload also contained **~87 Red Tie plants** (JCN_0800–0893, occ 2909–2995, events 0409–0430) with **no field forms** — the crew is completing Red Tie and the loc-12 forms arrive next batch. Boards are **ingested (provenance saved) but not linked** (no Multimedia/Phenotyping rows). When the forms arrive: load Stage A → link the held boards → **resolve the occ-2909 collision** (the EO32 event-404 plant, synthetically reassigned to 2909 last session, must move to a reserved ID — the field's real roll used 2909 for a Red Tie plant).

## EO32 "10 Mile Creek" — July 3 2026 campaign (loaded 2026-07-06)

Revisit of existing location 6 (EO32). Two-stage load, both stages verified **0-orphan; 137/137 occurrences imaged + phenotyped**:
- **Stage A** (`field_forms_ocr.py`): 73 forms → **+36 Events** (373–408, **CODE128 barcode-verified**, 36/36 decoded clean), **+137 Occurrences** (2768–2909), +73 form images. Occurrence OCR digit-errors caught by reading the physical forms + boards: `2404→2904`, `2405–2408→2905–2908`, `2744–2749→2794–2799` (all looped-9 misread as 4 — confirmed on the plant boards). `associatedTaxa` auto-homogenized; **+2 taxa** (Tragopogon 48, prickly mustard 49, both provisional — flag Ian/Teo) + 6 lexicon variants. Event 385's form mis-dated 07-04 corrected to 07-03 (+remark); 8 events' condition `1.5→1`.
- **Reused envelope:** occ **2897** written on event 404's 7th plant (form + board both read 2897) was already the wild EO69 plant (event 265) → reassigned to fresh **2909**; board image title retains verbatim 2897; provenance in `Occurrences.occurrenceRemarks`.
- **Stage B** (`stageB_load.py`): 137 boards ingested (content-addressed `LEPA_2026-07-03_<sha8>.jpg`) → **+137 Multimedia** (tableID 13) **+137 Phenotyping** (112 medium / 14 small / 11 large; 136 field-tape H/W, 1 image-scale). No stray/other-day images (date cross-check clean; one board mis-dated 07-04-2024 noted).

## July 1–2 2026 campaign (EO18-8 / EO18-7 / EO25 / EO24 — loaded 2026-07-03)

Revisit of existing locations 18–25 (2025 data already present). Two-stage load, both stages verified 0-orphan:
- **Stage A** (`field_forms_ocr.py`): 96 forms → **+45 Events** (328–372, **CODE128 barcode-verified**, 44/45 decoded), **+172 Occurrences** (2596–2767), +96 form images. Counts matched Ian's field emails exactly (loc 20 = 98, loc 18 = 59, loc 21 = 8, EO24 = 6, loc 19 = 1). `associatedTaxa` auto-homogenized; **+2 taxa** (Descurainia 46, Physaria 47) + 14 lexicon variants added for the new tokens.
- **Stage B** (`stageB_load.py` — NOT `02_ocr --load`; see the guide's "which loader" note): 172 boards ingested → **+172 Multimedia** (tableID 13) **+172 Phenotyping** (48 large / 107 medium / 17 small). 15 board-only-unclassed re-scored from field-written h/w (field tape, high confidence). No stray/other-day images (date cross-check clean).
- **[#14](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/14) (CLOSED)** — occ 2714 reused across events 362 & 363 (field envelope reused); resolved by moving occ 2714 → event 363, so both events hold 4 plants matching the whiteboards.
- **Images:** unique `LEPA_<date>_<sha8>.jpg` scheme in `Multimedia_main/`; raw in `Multimedia_images/<year>/<date>/`.

## Genotyping & biobanking (integrated 2026-07-02)

Biobanking→genetics pipeline loaded and **validated against Peggy's master sheet** (full multiset match, 0 diffs):

- **TissueBank** 1,699 · **TissueTransactions** 33 · **MolecularBank** 662 DNA extractions (MP/Omega) ·
  **Sequencing** 505 Nanopore libraries (497 ingroup / 8 outgroup) · **GenotypingStatus** 885 rows.
- **Pipeline status** (885 rows): **Complete 259 · Failed 225 · Incomplete 401** (883 distinct occurrences; 258 Complete).
- **Taxonomy:** +9 *Lepidium* congeners (outgroups). **6 clone occurrences** flagged (`occurrenceRemarks LIKE '%CLONE%'`).
- **View** `vSequencingOccurrence` joins each library to its `occurrenceID` (SRK-pipeline entry point; `SampleID` = `libraryName`).
- **Terms** now document every genotyping field (140 total); `TissueTransactions` (Biobanking) + `GenotypingStatus` (Genetics) registered.
- **Issues:** #9–#13 filed for the lab team; **#12 closed** (status gaps reconciled; occ 1134 resolved to *L. montanum*). Open: **#10** (57 tissues no weight), **#11** (6 master-sheet tissue cells), **#13** (5 negative tissue weights).
- **Event-265 occurrence-ID collision fixed** — wild EO69 plants renumbered off the genotyping-bank IDs (2384/2385/2386→2894/2895/2896); clones/outgroups now hold 2383–2386; three board images annotated with corrected OccIDs. *(A 4th wild plant "2897" added here was later found **spurious** — not on the EO69 field sheet, no image/data — and removed 2026-07-08; see [#17](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/17). occ 2897 now correctly = the EO32 event-404 plant.)* See `Notes` (Data Correction rows) + `PIPELINE_LOG.md`.

## 2026 campaign (processed June 2026) — see [`REPORT_2026_campaign.md`](REPORT_2026_campaign.md)

Two-stage load: **forms → records** (1 new Location EO69, 17 Events, 84 Occurrences, 40 form images as
evidence), then **plant images → multimedia + phenotyping** (80 linked, 76 phenotyped). **h/w validation:**
on the 23 boards with field-written h/w, image measurement matched the field tape to **median ±1 cm
(20/21 within ±2 cm)** for both height and width — the technique is validated against ground truth.
Reused-barcode collisions caught + fixed (event sticker `0098`→`268`).

**Follow-up load (2026-06-28) — closed [#7](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/7) + [#8](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/8):**
EO38 forms came in → +15 Events (239–241, 249–260), +37 Occurrences (2281–2317) on a **revisit of location 1**,
34 plant images + 33 phenotyped, 31 form images as evidence. EO118 envelope event located → occ 2395–2403
attached to **event 266**, 9 images + phenotyping linked. OCR section-4 fixes confirmed against plant boards
(234→2314, 2205→2285, 2708→2308, 7310→2310; Event 255 = 2292–2299 per review).

**EO18-7 load (2026-06-30):** +32 Events (270–302, gap at 277), +103 Occurrences (2417–2519) on a **revisit
of location 17**, +103 plant images, +103 phenotyped (3 from board-written W/H), +65 form sheets. Event
numbers **barcode-verified** (no collisions after the 5-event fix). Occurrence numbers anchored on the board
reads, which resolved the noisy form OCR (e.g. 7470→2430, 24465→2465, 501→2501). Also recovered occ **2379**
(EO69, collected + imaged but missed in the original load) and flagged occ **2386** as a no-image gap;
occ 2387–2391 confirmed as skipped barcodes.

**EO18-7 Location 16 load (2026-07-01, fieldwork 06-30):** +25 Events (303–327, barcode-verified — one "630"
was really 324), +76 Occurrences (2520–2595), all imaged + phenotyped, +51 form sheets, on a **revisit of
location 16**. Board reads corrected 4 form-OCR slips. **First live run of `associatedTaxa` auto-homogenization**
→ `Taxonomy` taxonIDs (verbatim kept in `associatedTaxaOriginal`); 1 run-together token reviewed by Sven.

## Standing items (known; not integrity faults)

| # | Item | Detail | GitHub |
|---|---|---|---|
| 0b | **2026 collected occ without image** | 7 occurrences (EO76 ×5, EO69 ×1, EO118 ×1) have no linked plant photo — un-photographed or a board# mis-read. | [#6](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/6) |
| 0d | **EO38 image residuals** | occ **2282** not photographed (board **2202** is an image with no occurrence — likely a 2282 misread, in `stageB_unmatched_review.csv` for a human check); occ **2288 & 2292** photographed but no plant in frame → linked board-only, tagged `NOT PHENOTYPED`. | (within #7) |
| 1 | **Un-phenotyped: plant below board** | 18 occurrence images where the plant was photographed on the ground below/beside the board (no scale reference) → size indeterminate. Tagged in `Multimedia.remarks` (`NOT PHENOTYPED`). | [#5](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/5) |
| 2 | **Un-phenotyped: image lost** | occ 220 (`EO27 Figgins - Occurrence 220.jpg`) deleted from Drive, no copy. Record retained, `IMAGE LOST` in remarks. | [#5](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/5) |
| 3 | **No-board context images** | 48 location-level images (transit/landscape/crew) auto-attached to the nearest site; need a human to confirm content + locationID. `Multimedia.remarks LIKE 'NEEDS CURATION%'`. | [#4](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/4) |
| 4 | **Image coverage gaps** | 50 occurrences with no image: **45 ex-situ** greenhouse accessions (image later, by design) + **5 in-situ** field gaps (occ 213, 214, 215, 236, 379 — no photo taken). View `vUnimagedOccurrences`. | [#3](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/3) |
| 5 | **Board-vs-DB mismatches (2025)** | 56 boards where board-date ≠ `occurrenceDate` (some are observed-vs-photographed next day; some may be entry errors) + 26 location-label candidates. **Not currently re-checkable** — see limitation below. | [#2](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/2) |
| 6 | **Board number 289 reused** | Board 289 used on two 2025 plants; one image (`JCN_0360`, now in `Multimedia_images/2025/unknown-date/`) needs the correct occurrenceID. | [#1](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/1) |

## Resolved this session (2026-06)

- **Event-barcode audit** (2026-06-30) — new protocol: decode the **CODE128 barcode** on each Event
  sticker instead of trusting digit-OCR (`Multimedia_pipeline/verify_event_barcodes.py`). The audit
  found **5 mis-entered 2026 events** (stored `265/281/282/285/288` → true `263/261/262/265/269`); all
  corrected by a backed-up two-phase renumber cascading Events/Occurrences/Multimedia. Now `32/32`
  loaded 2026 events match their barcode. (Setup: see "Requirements & setup" in the pipeline guide.)
- **#7 EO38 forms & #8 EO118 event** (2026-06-28) — both closed. EO38 forms OCR'd and loaded (revisit of
  location 1; +15 Events, +37 Occurrences, plant images + form evidence); EO118 occ 2395–2403 attached to
  event 266. See the 2026-campaign follow-up note above and the GitHub issues.
- **Filename collisions** — camera `JCN_####` numbering resets yearly; 2026 frames had overwritten 56
  of the 2025 images. Recovered all 56 from `work/full/`; root-caused and fixed by a content-addressed
  naming scheme. See [`ISSUE_filename_collision.md`](ISSUE_filename_collision.md).
- **occ 226–230 EO mis-entry** — were `EO38 / loc1 / 06-17-2025`; corrected to `EO27 / loc9 / 07-08-2025`
  (board OCR + EXIF capture 2025-07-08 + neighbours all agree). Audit note in `occurrenceRemarks`.
- **occ 220** — image confirmed lost and documented (above).

## Known limitation — date re-validation

The EXIF-vs-`occurrenceDate` cross-check (which caught the 226–230 error) only covers the **77 of 760**
occurrence images that still carry EXIF; the rest are EXIF-stripped 2025 crop-pipeline copies. So issue
**#2** (board-date mismatches) cannot be revisited from EXIF alone — it would need a re-OCR pass of the
boards (`02_ocr.py`). All 77 EXIF-bearing images currently agree with their `occurrenceDate`.

## How to query the flags

```sql
SELECT * FROM Multimedia WHERE remarks LIKE '%NOT PHENOTYPED%';   -- 18 below-board images (#5)
SELECT * FROM Multimedia WHERE remarks LIKE 'IMAGE LOST%';        -- occ 220 (#5)
SELECT * FROM Multimedia WHERE remarks LIKE 'NEEDS CURATION%';    -- 48 no-board images (#4)
SELECT * FROM vUnimagedOccurrences;                               -- 50 image-coverage gaps (#3)
```

Provenance of every image (original camera name, year, field-day date, EXIF capture, SHA-256) is in the
new `Multimedia` columns and in `Multimedia_main/file_registry.csv`; all renames are logged in
[`PIPELINE_LOG.md`](PIPELINE_LOG.md).
