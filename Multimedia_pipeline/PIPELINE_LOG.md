
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

## 20260628-214255 — EO118 occ 2395-2403 -> event 266 (issue #8)
- inserted 9 occurrences (not seed-collected; event assigned by Sven). Backup `LEPA_SQL.db.bak-eo118occ-20260628-214255`

## 20260628-214537 — stageB_load --apply
- linked 9 2026 plant images to occurrences (Multimedia tableID 13) + 9 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260628-214537`.

## 20260628-214848 — field_forms_ocr --load eo38_forms_results.json
- staged 1 locations (1 revisit / 0 new), 15 events, 39 occurrences; occ collisions 37. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260628-215025 — field_forms_ocr --load eo38_forms_results.json
- staged 1 locations (1 revisit / 0 new), 15 events, 39 occurrences; occ collisions 39. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260628-215114 — field_forms_ocr --load eo38_forms_results.json
- staged 1 locations (1 revisit / 0 new), 15 events, 36 occurrences; occ collisions 36. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260628-215114 — field_forms_ocr --commit --apply
- inserted 0 Locations, 15 Events, 36 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260628-215114`.

## 20260628-215155 — stageB_load --apply
- linked 33 2026 plant images to occurrences (Multimedia tableID 13) + 32 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260628-215155`.

## 20260628-215156 — field_forms_ocr --forms-mm --apply
- linked 0 field-form images to Multimedia (0 Location tableID 9, 0 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260628-215156`.

## 20260628-215808 — field_forms_ocr --load eo38_forms_results.json
- staged 1 locations (1 revisit / 0 new), 15 events, 37 occurrences; occ collisions 37. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260628-215831 — field_forms_ocr --forms-mm --apply
- linked 31 field-form images to Multimedia (1 Location tableID 9, 30 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260628-215831`.

## 20260628-215831 — stageB_load --apply
- linked 0 2026 plant images to occurrences (Multimedia tableID 13) + 0 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260628-215831`.

## 20260628-220108 — stageB_load --apply
- linked 1 2026 plant images to occurrences (Multimedia tableID 13) + 1 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260628-220108`.

## 20260628-230142 — Phenotyping occ 2404 from field board
- inserted H=23 W=30 cm (field tape, board-written; image senescent). Backup `LEPA_SQL.db.bak-pheno2404-20260628-230142`

## 20260630-201158 — Event renumber (barcode audit)
- Barcode-verified fixes (wrong->true): 265->263, 281->261, 282->262, 285->265, 288->269. Cascaded Events/Occurrences/Multimedia. Backup `LEPA_SQL.db.bak-eventfix-20260630-201158`

## 20260630-205756 — EO18-7 Stage A load
- +32 Events (270-302 gap 277), +103 Occurrences (2417-2519), loc 17 revisit, all 06-29-2026. Backup `LEPA_SQL.db.bak-eo18load-20260630-205756`

## 20260630-205852 — EO18-7 Stage B
- +103 Multimedia (tableID 13), +100 Phenotyping. Backup `LEPA_SQL.db.bak-eo18stageB-20260630-205849`

## 20260630-205946 — EO18-7 forms-mm
- +65 field-form images linked as evidence. Backup `LEPA_SQL.db.bak-eo18formsmm-20260630-205945`

## 20260630-210528 — EO18-7 no-plant boards phenotyped from field W/H
- occ 2444/2469/2482 entered from board values (field tape). Backup `LEPA_SQL.db.bak-eo18noplant-20260630-210528`

## 20260630-211242 — recovered occ 2379 (EO69) + Note on skipped 2387-2391
- +1 Occurrence, +1 Multimedia, +1 Phenotyping. Backup `LEPA_SQL.db.bak-recover2379-20260630-211242`

## 20260630-225501 — spelling fixes (locationRemarks)
- 4 fixes: hitoric/invasie/cracters/Plesant. Backup `LEPA_SQL.db.bak-spelling-20260630-225501`

## 20260630-232329 — associatedTaxa homogenization
- normalized 260 Events (34 standard names + group-a fixes; delimiter '; '). Backup `LEPA_SQL.db.bak-taxanorm-20260630-232329`

## 20260630-232813 — landscapeHealth spelling fixes
- 6 fixes: sagebrusgh/chetgrassland/encroched/encorched/encroching. Backup `LEPA_SQL.db.bak-locspell-20260630-232813`

## 20260630-233023 — understorey->understory (American)
- 5 rows. Backup `LEPA_SQL.db.bak-understory-20260630-233023`

## 20260630-234116 — Taxonomy populated + associatedTaxa->taxonID + associatedTaxaOriginal (Term 71)
- +34 Taxonomy rows. Backup `LEPA_SQL.db.bak-taxonomyload-20260630-234116`

## 20260701-025245 — Ian taxonomy corrections
- fescue merged into Vulpia (taxonID 19->18); globemallow->Sphaeralcea munroana; +squirreltail (Elymus elymoides, 36); 8 taxa confirmed-by-Ian; lexicon updated. Backup `LEPA_SQL.db.bak-iantaxa-20260701-025245`

## 20260701-025502 — Vulpia -> Vulpia microstachys (species) per Sven. Backup `LEPA_SQL.db.bak-vulpia-20260701-025502`

## 20260701-025644 — Note 9: EO18-7 field update (76 samples, EO18-8/EO25 plan). Backup `LEPA_SQL.db.bak-note-20260701-025644`

## 20260701-025945 — Leymus merge: wild rye(23) -> Leymus cinereus(13) per Sven. Backup `LEPA_SQL.db.bak-leymus-20260701-025945`

## 20260701-220750 — EO18-7 Location 16 Stage A (batch 2026-06-30)
- +25 Events (303-327, barcode-verified), +76 Occurrences (2520-2595), loc 16 revisit, associatedTaxa homogenized to taxonIDs. Backup `LEPA_SQL.db.bak-b0630A-20260701-220750`

## 20260701-220841 — EO18-7 Loc16 Stage B + forms-mm (batch 2026-06-30)
- +76 Multimedia plant images, +76 Phenotyping, +51 form-evidence images. Backup `LEPA_SQL.db.bak-b0630B-20260701-220841`

## 20260701-220932 — taxa fix ev306: run-together 'cheat sagebush tumble mustard' -> 2;4;7 (per Sven)

## 20260702-151516 — Genotyping foundation: +0 congener taxa, +1402 occurrences (lightweight). Artemisia/Astragalus deferred (Note 10). Backup `LEPA_SQL.db.bak-genofound-20260702-151516`

## 20260702-151840 — TissueBank + TissueTransactions (robust)
- +1699 TissueBank (131 Artemisia/Astragalus skipped), +33 TissueTransactions.

## 20260702-152059 — MolecularBank (DNA extractions)
- +662 MolecularBank (23 Artemisia/Astragalus skipped). Backup bak-molec-20260702-152059

## 20260702-152316 — occurrences: locationID from Master Sheet
- set locationID (+EOID) on 653 genotyping-import occurrences. Backup bak-occloc-20260702-152316

## 20260702-152520 — TissueBank tissueWeight backfill
- tissueWeight set on 1609 rows (604 computed from Weight+tube - tube_avg). Backup bak-tw-20260702-152520

## 20260702-153059 — Sequencing (+cols flowCellID/barcode/libraryNumber/ingroup/plate) + load
- +505 Sequencing from sampling_metadata; 0 had a DNA_Extraction not in MolecularBank (molecularID left NULL). Backup bak-seq-20260702-153059

## 20260702-154534 — MolecularBank fixes + tissue VOID weights
- [1] extractionProtocol<-Master Sheet Kit (580, 0 diffs); [2] recordedDate=2026-07-02; [3] 67 clone line IDs (66 w/ site_number); [4] 31 VOID tissueWeight=0 + 2 typo fixes; [5] 2 Notes. Backup bak-molfix-20260702-154534

## 20260702-155047 — MolecularBank Kit/buffer homogenization
- Omega variants->Omega; buffer DES->MP (68), EB->Omega (3); MP=DES, Omega=EB. Backup bak-kitbuffer-20260702-155047

## 20260702-155325 — MolecularBank quantity..remarks refreshed from DNA bank
- {'qty': 519, 'a280': 80, 'vol': 215, 'loc': 129, 'rem': 84}. Backup bak-molfill-20260702-155325

## 20260702-161018 — GenotypingStatus table (validated vs Peggy's Master; issue #11)
- +885 rows; derived stage flags + nextStep. Backup bak-genostatus-20260702-161018

## 20260702-162357 — Terms + TableModules for biobanking/genetics tables
- TableModules +2 (GenotypingStatus=Genetics, TissueTransactions=Biobanking); Terms +68 (TissueBank, MolecularBank, Sequencing, TissueTransactions, GenotypingStatus). Backup bak-terms-20260702-162357

## 20260702-171232 — TissueTransactions accurate-portrayal docs
- Honest TableModules/Terms definitions (derived table, snapshot not ledger, missing attribution) + provenance Note. Backup bak-ttprov-20260702-171232

## 20260702-171317 — TissueTransactions debit column
- +tissueWeightTaken (=start-remaining), backfilled 33; +Term; refined TableModules def. Backup bak-ttdebit-20260702-171317

## 20260702-172604 — vSequencingOccurrence view
- Sequencing LEFT JOIN MolecularBank -> exposes occurrenceID/tissueID/taxonID/kit off the library key (SampleID=libraryName). 505 rows, 491 occ resolved. Backup bak-vseqocc-20260702-172604

## 20260702-195507 — Event 265 occ-ID collision fix
- Renumber 2384/5/6->2894/5/6 (Occ/Multimedia/Pheno); detach 15 clone/outgroup GenotypingStatus rows; detach JCN_0050(occ2381)/JCN_0266(occ2385) mislinks; repoint 2381 pheno. TissueBank left intact. Backup bak-evt265fix-20260702-195507

## 20260702-202148 — Case 2 clone/outgroup occurrences + clone flags
- +Occ 2384(clone 26-3),2385/2386(fremontii); flagged 5 clones. Backup bak-clonesocc-20260702-202148

## 20260702-203450 — Event 265 wild renumber shift + BEA occ
- Cascade 2383->2894,2894->2895,2895->2896,2896->2897; BEA occ at 2383. Backup bak-cascade-20260702-203450

## 20260702-204902 — GenotypingStatus reconciled w/ new master + issue #12
- 4 rows updated (1708,1584,1714,1532); 1134 held. Backup bak-msreconcile-20260702-204902

## 20260702-205142 — fix occ 1532 dup rows (split to 2 distinct master entries)
- Backup bak-1532fix-20260702-205142

## 20260702-210111 — occ 1134 identity fix (montanum)
- mol 93 taxon->37, occ->1134, clone flag removed. Backup bak-mol93fix-20260702-210111

## 20260702-211258 — clone tissue links supplied
- mol 116->48,103->1821,128->1822 from master. Backup bak-tissuelink-20260702-211258

## 20260703-205423 — field_forms_ocr --load forms0703_results.json
- staged 6 locations (6 revisit / 0 new), 45 events, 173 occurrences; occ collisions 173. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260703-210136 — field_forms_ocr --load forms0703_results.json
- staged 6 locations (6 revisit / 0 new), 45 events, 172 occurrences; occ collisions 172. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260703-210224 — field_forms_ocr --commit --apply
- inserted 0 Locations, 45 Events, 172 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260703-210224`.

## 20260703-210253 — field_forms_ocr --forms-mm --apply
- linked 96 field-form images to Multimedia (6 Location tableID 9, 90 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260703-210252`.

## 20260703-210522 — 01_ingest_register --apply
- source `/Users/sven/Documents/Current_projects/LEPA_fieldwork_protocol/SQL_DB/Multimedia_images` years ['2025', '2026']; copied 172 new files into `Multimedia_main/` (1299 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 1083; new registered: 188; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260703-210522`; registry `Multimedia_main/file_registry.csv`

## 20260703-220737 — 02_ocr --load ocr_results.csv
- staged 172 provisional occurrences (IDs 2898-3069); NEW_EO: 0; review staging_2026/ before load

## 20260703-221051 — stageB_load --apply
- linked 172 2026 plant images to occurrences (Multimedia tableID 13) + 172 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260703-221051`.

## 20260703-221142 — field_forms_ocr --load forms0703_results.json
- staged 6 locations (6 revisit / 0 new), 45 events, 172 occurrences; occ collisions 172. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260703-221650 — field_forms_ocr --load forms0703_results.json
- staged 6 locations (6 revisit / 0 new), 45 events, 172 occurrences; occ collisions 172. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260703-222057 — re-scored 15 unclassed July1-2 occ from field board h/w
- 15 re-scored from board-written measurements; 0 no board h/w. Backup bak-rescore-20260703-222057

## 20260703-222730 — occ 2714 moved event 362->363 (issue #14, board evidence)
- Event 362=2710-2713, Event 363=2714-2717. Backup bak-2714move-20260703-222730
