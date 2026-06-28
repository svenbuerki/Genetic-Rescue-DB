
## 20260627-153403 — 01_ingest_register --apply
- source `/Users/sven/Documents/Current_projects/LEPA_fieldwork_protocol/SQL_DB/Multimedia_images` years ['2025', '2026']; copied 948 new files into `Multimedia_main/` (948 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<year>_<sha8>.jpg`: 809; new registered: 139; ambiguous: 0
- DB backup `LEPA_SQL.db.bak-ingest-20260627-153403`; registry `Multimedia_main/file_registry.csv`

## 20260627-154223 — 01_ingest_register --apply
- source `/Users/sven/Documents/Current_projects/LEPA_fieldwork_protocol/SQL_DB/Multimedia_images` years ['2025', '2026']; copied 948 new files into `Multimedia_main/` (948 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<year>_<sha8>.jpg`: 809; new registered: 139; ambiguous: 0
- DB backup `LEPA_SQL.db.bak-ingest-20260627-154223`; registry `Multimedia_main/file_registry.csv`

## 20260627-161313 — 03_phenotype --load phenotype_results.csv --apply
- inserted 21 Phenotyping rows; skipped 0 already-measured; backup `LEPA_SQL.db.bak-pheno-20260627-161313`

## 20260627-161645 — DB correction (occ 226-230)
- occ 226-230 EOID 1->9 (EO38->EO27), locationID 1->9, occurrenceDate 06-17-2025->07-08-2025; Multimedia.createDate->07-08-2025. Data-entry error confirmed by board OCR + EXIF + neighbours. Backup `LEPA_SQL.db.bak-fix226-20260627-161645`

## 20260627-161703 — 03_phenotype --load phenotype_results_226-230.csv --apply
- inserted 4 Phenotyping rows; skipped 0 already-measured; backup `LEPA_SQL.db.bak-pheno-20260627-161703`

## 20260627-162631 — flag occ 220 image lost
- Multimedia (occ 220) remarks set to IMAGE LOST (deleted from Drive, no local copy). Backup `LEPA_SQL.db.bak-occ220-20260627-162631`

## 20260627-163254 — flag un-phenotyped images
- GitHub issue svenbuerki/Genetic-Rescue-DB#5 filed; Multimedia.remarks tagged on 18 'plant below board' images + occ 220. Backup `LEPA_SQL.db.bak-noplant-20260627-163254`

## 20260627-222520 — add Events.measurementValuePlantArea
- new columns measurementValuePlantArea(+Unit) on Events; Terms 69/70 (tableID 2). 2026 forms map the crown/area field here; measurementValueCrownAvg kept for 2025 (215 rows). Backup `LEPA_SQL.db.bak-plantarea-20260627-222520`
- 20260627-222609 — REVERTED measurementValuePlantArea add (user: leave unchanged for now, investigate later)

## 20260627-222825 — add Events.measurementValuePlantArea (re-applied)
- new columns measurementValuePlantArea(+Unit) on Events; Terms 69/70 (tableID 2). Recorded from 2026 field campaign; measurementValueCrownAvg kept for 2025 (215 rows). Backup `LEPA_SQL.db.bak-plantarea-20260627-222825`

## 20260627-224231 — field_forms_ocr --load field_forms_results.json
- staged 6 locations (5 revisit / 1 new), 17 events, 83 occurrences; occurrenceID collisions: 0. Review staging_2026/ before load.

## 20260627-225019 — field_forms_ocr --load field_forms_results.json
- staged 6 locations (5 revisit / 1 new), 17 events, 83 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260627-225645 — field_forms_ocr --load field_forms_results.json
- staged 6 locations (5 revisit / 1 new), 17 events, 83 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260627-231531 — field_forms_ocr --load field_forms_results.json
- staged 6 locations (5 revisit / 1 new), 17 events, 84 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260627-232050 — field_forms_ocr --load field_forms_results.json
- staged 6 locations (5 revisit / 1 new), 17 events, 84 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260627-232425 — field_forms_ocr --load field_forms_results.json
- staged 6 locations (5 revisit / 1 new), 17 events, 84 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260627-233418 — field_forms_ocr --load field_forms_results.json
- staged 6 locations (5 revisit / 1 new), 17 events, 84 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260627-233612 — field_forms_ocr --commit --apply
- inserted 1 Locations, 17 Events, 84 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260627-233612`.

## 20260627-233916 — field_forms_ocr --forms-mm --apply
- linked 40 field-form images to Multimedia (6 Location tableID 9, 34 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260627-233915`.

## 20260628-023623 — stageB_load --apply
- linked 80 2026 plant images to occurrences (Multimedia tableID 13) + 76 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260628-023623`.
