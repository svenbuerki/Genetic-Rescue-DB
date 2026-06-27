
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
