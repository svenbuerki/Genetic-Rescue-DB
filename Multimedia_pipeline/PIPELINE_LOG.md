
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

## 20260704-190620 — taxonRemarks updated w/ Ian's 2026-07-03 feedback (Descurainia genus confirmed; Physaria/Lesqu -> Teo)
- Backup bak-taxaremark-20260704-190620

## 20260706-231306 — field_forms_ocr --load forms0706_results.json
- staged 1 locations (1 revisit / 0 new), 36 events, 137 occurrences; occ collisions 125. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260706-232636 — field_forms_ocr --load forms0706_results.json
- staged 1 locations (1 revisit / 0 new), 36 events, 137 occurrences; occ collisions 125. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260707-044950 — field_forms_ocr --load forms0706_results.json
- staged 1 locations (1 revisit / 0 new), 36 events, 137 occurrences; occ collisions 125. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260707-045000 — field_forms_ocr --commit --apply
- inserted 0 Locations, 36 Events, 137 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260707-045000`.

## 20260707-045011 — field_forms_ocr --forms-mm --apply
- linked 73 field-form images to Multimedia (1 Location tableID 9, 72 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260707-045011`.

## 20260707-045347 — 01_ingest_register --apply
- source `/Users/sven/Documents/Current_projects/LEPA_fieldwork_protocol/SQL_DB/Multimedia_images` years ['2025', '2026']; copied 137 new files into `Multimedia_main/` (1436 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 1255; new registered: 153; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260707-045347`; registry `Multimedia_main/file_registry.csv`

## 20260707-051333 — stageB_load --apply
- linked 137 2026 plant images to occurrences (Multimedia tableID 13) + 137 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260707-051333`.

## 20260707-174835 — field_forms_ocr --load forms0706_EO30_results.json
- staged 2 locations (1 revisit / 1 new), 11 events, 50 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260707-174911 — field_forms_ocr --commit --apply
- inserted 1 Locations, 11 Events, 50 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260707-174911`.

## 20260707-174912 — field_forms_ocr --forms-mm --apply
- linked 24 field-form images to Multimedia (2 Location tableID 9, 22 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260707-174912`.

## 20260707-175000 — 01_ingest_register --apply
- source `/Users/sven/Documents/Current_projects/LEPA_fieldwork_protocol/SQL_DB/Multimedia_images` years ['2025', '2026']; copied 137 new files into `Multimedia_main/` (1573 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 1392; new registered: 153; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260707-175000`; registry `Multimedia_main/file_registry.csv`

## 20260707-180358 — stageB_load --apply
- linked 50 2026 plant images to occurrences (Multimedia tableID 13) + 50 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260707-180358`.

## 20260708-214151 — field_forms_ocr --load forms0607_results.json
- staged 2 locations (1 revisit / 1 new), 43 events, 159 occurrences; occ collisions 159. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260708-214422 — field_forms_ocr --load forms0607_results.json
- staged 2 locations (1 revisit / 1 new), 43 events, 159 occurrences; occ collisions 159. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260708-214448 — field_forms_ocr --commit --apply
- inserted 1 Locations, 43 Events, 159 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260708-214448`.

## 20260708-214450 — field_forms_ocr --forms-mm --apply
- linked 88 field-form images to Multimedia (2 Location tableID 9, 86 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260708-214449`.

## 20260708-214847 — 01_ingest_register --apply
- source `/Users/sven/Documents/Current_projects/LEPA_fieldwork_protocol/SQL_DB/Multimedia_images` years ['2025', '2026']; copied 74 new files into `Multimedia_main/` (1647 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 1442; new registered: 177; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260708-214847`; registry `Multimedia_main/file_registry.csv`

## 20260708-214918 — stageB_load --apply
- linked 159 2026 plant images to occurrences (Multimedia tableID 13) + 159 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260708-214918`.

## 20260709-191042 — field_forms_ocr --load forms0708_results.json
- staged 3 locations (2 revisit / 1 new), 32 events, 103 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260709-191230 — field_forms_ocr --load forms0708_results.json
- staged 3 locations (2 revisit / 1 new), 32 events, 103 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260709-191240 — field_forms_ocr --commit --apply
- inserted 1 Locations, 32 Events, 103 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260709-191240`.

## 20260709-191252 — field_forms_ocr --forms-mm --apply
- linked 67 field-form images to Multimedia (3 Location tableID 9, 64 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260709-191252`.

## 20260709-191837 — 01_ingest_register --apply
- source `../Multimedia_images` years ['2025', '2026']; copied 103 new files into `Multimedia_main/` (1750 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 1603; new registered: 119; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260709-191837`; registry `Multimedia_main/file_registry.csv`

## 20260709-191949 — stageB_load --apply
- linked 103 2026 plant images to occurrences (Multimedia tableID 13) + 103 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260709-191949`.

## 20260710-200602 — field_forms_ocr --load forms0709fw_results.json
- staged 1 locations (1 revisit / 0 new), 32 events, 125 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260710-200730 — field_forms_ocr --load forms0709fw_results.json
- staged 1 locations (1 revisit / 0 new), 32 events, 125 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260710-200742 — field_forms_ocr --commit --apply
- inserted 0 Locations, 32 Events, 125 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260710-200742`.

## 20260710-200748 — field_forms_ocr --forms-mm --apply
- linked 0 field-form images to Multimedia (0 Location tableID 9, 0 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260710-200748`.

## 20260710-200931 — field_forms_ocr --load forms0709fw_results.json
- staged 1 locations (1 revisit / 0 new), 32 events, 125 occurrences; occ collisions 125. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260710-200932 — field_forms_ocr --forms-mm --apply
- linked 65 field-form images to Multimedia (1 Location tableID 9, 64 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260710-200931`.

## 20260710-201002 — 01_ingest_register --apply
- source `../Multimedia_images` years ['2025', '2026']; copied 125 new files into `Multimedia_main/` (1875 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 1706; new registered: 141; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260710-201002`; registry `Multimedia_main/file_registry.csv`

## 20260710-201023 — stageB_load --apply
- linked 125 2026 plant images to occurrences (Multimedia tableID 13) + 125 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260710-201022`.

- 2026-07-10 TAXA FIX (July-9 load): 'Ernst'→crust(35) on ev 507/509/510/511/512; 'stiff flax'→Atriplex(25) on ev 500. OCR artifacts confirmed against forms (Sven). 'blanketflower' (ev 503) still pending Teo. Backup LEPA_SQL.db.bak-taxafix-20260710-142312.

- 2026-07-10 TAXA FIX cont'd: 'blanketflower'→bur buttercup(9) on ev 503 (OCR artifact, Sven read the form). ALL 3 July-9 'unknown' taxa were OCR misreads of known taxa — no new Taxonomy rows needed. Backup LEPA_SQL.db.bak-taxafix503-20260710-142448.

## 20260713-210858 — field_forms_ocr --load forms0710fw_results.json
- staged 3 locations (1 revisit / 2 new), 11 events, 37 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260713-211118 — field_forms_ocr --load forms0710fw_results.json
- staged 3 locations (1 revisit / 2 new), 11 events, 37 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260713-211150 — field_forms_ocr --commit --apply
- inserted 2 Locations, 11 Events, 37 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260713-211150`.

## 20260713-211226 — field_forms_ocr --forms-mm --apply
- linked 25 field-form images to Multimedia (3 Location tableID 9, 22 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260713-211226`.

## 20260713-211246 — 01_ingest_register --apply
- source `../Multimedia_images` years ['2025', '2026']; copied 37 new files into `Multimedia_main/` (1912 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 1831; new registered: 53; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260713-211246`; registry `Multimedia_main/file_registry.csv`

## 20260716-201520 — stageB_load --apply
- linked 37 2026 plant images to occurrences (Multimedia tableID 13) + 37 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260716-201520`.

## 20260716-204832 — field_forms_ocr --load forms0713fw_results.json
- staged 1 locations (1 revisit / 0 new), 54 events, 123 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260716-204919 — field_forms_ocr --load forms0713fw_results.json
- staged 1 locations (1 revisit / 0 new), 54 events, 123 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260716-205003 — field_forms_ocr --commit --apply
- inserted 0 Locations, 54 Events, 123 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260716-205003`.

## 20260716-205014 — field_forms_ocr --forms-mm --apply
- linked 109 field-form images to Multimedia (1 Location tableID 9, 108 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260716-205014`.

## 20260716-205043 — 01_ingest_register --apply
- source `../Multimedia_images` years ['2025', '2026']; copied 208 new files into `Multimedia_main/` (2120 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 1868; new registered: 224; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260716-205043`; registry `Multimedia_main/file_registry.csv`

## 20260716-205119 — stageB_load --apply
- linked 123 2026 plant images to occurrences (Multimedia tableID 13) + 123 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260716-205119`.

## 20260720-100812 — field_forms_ocr --load forms0714fw_LOAD.json
- staged 2 locations (2 revisit / 0 new), 28 events, 55 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260720-100935 — field_forms_ocr --commit --apply
- inserted 0 Locations, 28 Events, 55 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260720-100935`.

## 20260720-101047 — field_forms_ocr --forms-mm --apply
- linked 57 field-form images to Multimedia (1 Location tableID 9, 56 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260720-101047`.

## 20260720-101539 — stageB_load --apply
- linked 55 2026 plant images to occurrences (Multimedia tableID 13) + 55 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260720-101539`.

## 20260720-1020 — manual EOID cleanup (EO8 occurrences)
- The Stage-A loader stages EO8 occurrences with `EOID='?'` (locationCode "EO8" ≠ EOs.EOCode "EO08"). Set July-14 EO8 occurrences (3506–3560) to the correct EOID 15 in staging, and ran `UPDATE Occurrences SET EOID='15' WHERE locationID IN (27,28,29) AND EOID='?'` to sweep the 123 July-13 loc-28 occurrences (3383–3505) in the same load. Backup `LEPA_SQL.db.bak-eoidfix-20260720-*`. All EO8 occurrences now carry EOID 15; `Occurrences.locationID → Locations.EOID` remains the authoritative join.

## 20260720-1030 — manual GPS corrections (Teo, manilla-verified)
- Corrected the event GPS on 12 events flagged by Teo while map-making and cross-checked against the field manilla envelopes (and prior-year points): events 242, 249, 255, 256, 258, 259, 260, 272, 293, 431, 432, 454. Each was a single- or two-field transcription slip (a wrong leading digit, a transposed digit, or a dropped sign). Backup `LEPA_SQL.db.bak-teo-gpsfix-20260720-*`. Values live in the DB only.

## 20260720-111440 — field_forms_ocr --load forms0715fw_LOAD.json
- staged 3 locations (2 revisit / 1 new), 40 events, 138 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260720-111828 — field_forms_ocr --load forms0715fw_LOAD.json
- staged 3 locations (2 revisit / 1 new), 40 events, 138 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260720-111920 — field_forms_ocr --commit --apply
- inserted 1 Locations, 40 Events, 138 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260720-111920`.

## 20260720-112011 — field_forms_ocr --forms-mm --apply
- linked 82 field-form images to Multimedia (3 Location tableID 9, 79 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260720-112011`.

## 20260720-112207 — 01_ingest_register --apply
- source `/Users/sven/Documents/Current_projects/LEPA_fieldwork_protocol/SQL_DB/Multimedia_images` years ['2025', '2026']; copied 108 new files into `Multimedia_main/` (2228 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 2046; new registered: 154; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260720-112207`; registry `Multimedia_main/file_registry.csv`

## 20260720-112659 — stageB_load --apply
- linked 138 2026 plant images to occurrences (Multimedia tableID 13) + 138 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260720-112659`.

## 20260721-194823 — field_forms_ocr --load forms161720_LOAD.json
- staged 8 locations (5 revisit / 3 new), 56 events, 143 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260721-200031 — field_forms_ocr --load forms161720_LOAD.json
- staged 8 locations (5 revisit / 3 new), 56 events, 143 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260721-200110 — field_forms_ocr --commit --apply
- inserted 3 Locations, 56 Events, 143 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260721-200110`.

## 20260721-200128 — field_forms_ocr --forms-mm --apply
- linked 120 field-form images to Multimedia (8 Location tableID 9, 112 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260721-200128`.

## 20260721-200219 — 01_ingest_register --apply
- source `/Users/sven/Documents/Current_projects/LEPA_fieldwork_protocol/SQL_DB/Multimedia_images` years ['2025', '2026']; copied 143 new files into `Multimedia_main/` (2371 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 2184; new registered: 159; ambiguous: 28
- DB backup `LEPA_SQL.db.bak-ingest-20260721-200219`; registry `Multimedia_main/file_registry.csv`

## 20260721-200836 — stageB_load --apply
- linked 143 2026 plant images to occurrences (Multimedia tableID 13) + 143 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260721-200836`.

## 20260722-001146 — field_forms_ocr --load forms0721fw_LOAD.json
- staged 3 locations (0 revisit / 3 new), 8 events, 30 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260722-001449 — field_forms_ocr --commit --apply
- inserted 3 Locations, 8 Events, 30 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260722-001449`.

## 20260722-001457 — field_forms_ocr --forms-mm --apply
- linked 19 field-form images to Multimedia (3 Location tableID 9, 16 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260722-001457`.

## 20260722-001910 — 01_ingest_register --apply
- source `Multimedia_images/2026/2026-07-21` (scoped to the July-21 boards) years ['2026']; copied 30 new files into `Multimedia_main/` (30 unique, 0 duplicate bytes)
- Multimedia identifiers migrated to `LEPA_<YYYY-MM-DD>_<sha8>.jpg`: 0; new registered: 30; ambiguous: 0
- DB backup `LEPA_SQL.db.bak-ingest-20260722-001910`; registry `Multimedia_main/file_registry.csv`

## 20260722-003246 — stageB_load --apply
- linked 30 2026 plant images to occurrences (Multimedia tableID 13) + 30 Phenotyping rows. Backup `LEPA_SQL.db.bak-stageB-20260722-003246`.

## 20260723-172619 — field_forms_ocr --load forms0721_ev718.json
- staged 1 locations (1 revisit / 0 new), 1 events, 0 occurrences; occ collisions 0. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.

## 20260723-172646 — field_forms_ocr --commit --apply
- inserted 0 Locations, 1 Events, 0 Occurrences from Stage A staging. Backup `LEPA_SQL.db.bak-formsload-20260723-172646`.

## 20260723-172646 — field_forms_ocr --forms-mm --apply
- linked 2 field-form images to Multimedia (0 Location tableID 9, 2 Event tableID 11); copied to Multimedia_main. Backup `LEPA_SQL.db.bak-formsmm-20260723-172646`.

## 20260723-175040 — DB correction: loc-50 event latitudes finalized (issue #18)
- Events 687/688/689 (EO27 loc 50) latitudes reviewed by Sven against the field forms/manilla. 687 & 688 confirmed correct (values unchanged); 689 corrected from its earlier provisional value (single-digit field-transcription error on the latitude). Longitudes unchanged throughout. eventRemarks promoted from 'provisional' to 'verified'. Backups `LEPA_SQL.db.bak-ev689lat-*`, `LEPA_SQL.db.bak-ev687-8verify-*`. Closes #18.

## 20261004-202450 — germplasm_seeds --load germplasm_results_20261004.json
- staged 123 rows (OK 120, FLAG 3, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'photo': 123}; 1 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-202502 — germplasm_seeds --load germplasm_results_20261004.json
- staged 123 rows (OK 120, FLAG 3, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'photo': 123}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-202540 — germplasm_seeds --load germplasm_results_20261004.json
- staged 123 rows (OK 122, FLAG 1, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'photo': 123}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004 — Stage C pilot (seed sheets PXL_20261004_*, location 28) — READ + VALIDATED, NOT YET LOADED
- 55 sheet photos moved from Multimedia_images/2026/2026-10-04 → Field_forms/2026 (checksums verified; they are event page-2 form pages).
- Read-only 5-agent sweep → work/germplasm_results_20261004.json (54 sheets; idx 51 = burst duplicate of idx 50, excluded). 123 rows.
- All rows resolve to location 28 (events 541–591 range read; events 592–610 = occ 3506–3545 not yet imaged). No sheet from locations 11/52/53 in this batch.
- Overrides: 4324→3424, 4325→3425 (digits transposed; event 553 = exactly 3424+3425). Held: occ 3412 weight 0.1317 g, no germplasmID → issue #21.
- Registry check: 0 duplicate germplasmIDs, 0 occurrences with >1 ID; IDs 1137–1273; acquisitionDate = photo date proxy (issue #20).

## 20261004-204228 — germplasm_seeds --load germplasm_results_20261004.json
- staged 123 rows (OK 122, FLAG 1, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'photo': 123}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-204240 — germplasm_seeds --commit --apply
- inserted 122 Germplasm rows (seed sheets → occurrenceID FK); 1 held as FLAG; 2 seed-quality notes appended to Events.eventRemarks; acquisitionDate = photo-date proxy for 122 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-204240`.

## 20261004-204240 — germplasm_seeds --sheets-mm --apply
- linked 54 seed-sheet / location-form images to Multimedia (Event tableID 11 / Location tableID 9), copied as LEPA_<date>_<sha8>.jpg. Backup `LEPA_SQL.db.bak-germplasmmm-20261004-204240`.

## 20261004-204558 — germplasm_seeds --load germplasm_results_20261004b.json
- staged 49 rows (OK 49, FLAG 0, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'sheet': 11, 'photo': 38}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-204644 — germplasm_seeds --load germplasm_results_20261004b.json
- staged 49 rows (OK 47, FLAG 2, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'sheet': 11, 'photo': 38}; 1 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-204658 — germplasm_seeds --load germplasm_results_20261004b.json
- staged 49 rows (OK 47, FLAG 2, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'sheet': 11, 'photo': 38}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-204709 — germplasm_seeds --commit --apply
- inserted 47 Germplasm rows (seed sheets → occurrenceID FK); 2 held as FLAG; 3 seed-quality notes appended to Events.eventRemarks; acquisitionDate = photo-date proxy for 36 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-204709`.

## 20261004-204709 — germplasm_seeds --sheets-mm --apply
- linked 20 seed-sheet / location-form images to Multimedia (Event tableID 11 / Location tableID 9), copied as LEPA_<date>_<sha8>.jpg. Backup `LEPA_SQL.db.bak-germplasmmm-20261004-204709`.

## 20261004 — Stage C batch 2 (PXL_20261004_202*, locations 3/10/19/39/42) — LOADED
- 20 photos = 5 location forms (first rule-compliant batch) + 15 seed sheets = all 15 events / 49 occurrences of these locations in the DB.
- +47 Germplasm (IDs 1171–1328); 11 rows with acquisitionDate written on the sheet (08-12/08-13/08-14-2026, initials SB), 36 photo-date proxy.
- Held (HOLD override): occ 3377 (.1794 vs .1774) and occ 3379 (.1044 vs .1844), overwritten weight digits on PXL_20261004_202403715 — check envelopes.
- Seed-quality notes appended to Events.eventRemarks: events 242, 493, 494. 20 images copied to Multimedia_main (5 Location tableID 9, 15 Event tableID 11).
- Issue #21 updated: germplasmID 1175 = occ 2318, not occ 3412.

## 20261004-205209 — germplasm_seeds --load germplasm_results_20261004b.json
- staged 49 rows (OK 2, FLAG 0, NO_SEED 0, LOADED 47, SKIP 0); acquisitionDate sources {'photo': 2}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-205224 — germplasm_seeds --commit --apply
- inserted 2 Germplasm rows (seed sheets → occurrenceID FK); 0 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; acquisitionDate = photo-date proxy for 2 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-205224`.

## 20261004 — Stage C held rows resolved
- occ 3377 weight 0.1194 g and occ 3379 0.1044 g confirmed by Sven from the envelopes; loaded (germplasmID 1319/1324). All 956 Germplasm rows verified against the 1000-seed-weight equation (0 off).

## 20261004-205938 — germplasm_seeds --load germplasm_results_20261004c.json
- staged 127 rows (OK 127, FLAG 0, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'photo': 127}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-210136 — germplasm_seeds --load germplasm_results_20261004c.json
- staged 127 rows (OK 122, FLAG 5, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'photo': 127}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-210136 — germplasm_seeds --commit --apply
- inserted 122 Germplasm rows (seed sheets → occurrenceID FK); 5 held as FLAG; 2 seed-quality notes appended to Events.eventRemarks; acquisitionDate = photo-date proxy for 122 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-210136`.

## 20261004-210137 — germplasm_seeds --sheets-mm --apply
- linked 36 seed-sheet / location-form images to Multimedia (Event tableID 11 / Location tableID 9), copied as LEPA_<date>_<sha8>.jpg. Backup `LEPA_SQL.db.bak-germplasmmm-20261004-210136`.

## 20261004 — Stage C batch 3 (PXL_20261004_1939–1945, re-transferred pilot: locs 11/52/53 + loc 28 form) — LOADED
- 36 photos = 4 location forms (11, 52, 53, 28 — the loc-28 form missing from batch 1) + 32 seed sheets. +122 Germplasm (IDs 1012–1353). Seed notes "many broken plants" → events 521, 524.
- Held (HOLD, ambiguous overwritten digits, check envelopes): occ 3248 (germ 1095/1085), 3276 (germ 1108/1109), 3293 (1.0402/1.0902 g), 3295 (1.1771/1.1741 g), 3299 (0.0657/0.6657 g).
- Loc 11: only 29/32 envelopes exist (Sven) → issue #22 (events 504, 516, 523; 12 plants; germplasmID leads 1053–1055, 1020–1022+1024, 1132–1136).
- 2026 Germplasm total 293; 0 occurrences with >1 accession; all estimates match the 1000-seed equation.

## 20261004-210851 — germplasm_seeds --load germplasm_results_20261004c.json
- staged 127 rows (OK 2, FLAG 3, NO_SEED 0, LOADED 122, SKIP 0); acquisitionDate sources {'photo': 5}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-210851 — germplasm_seeds --commit --apply
- inserted 2 Germplasm rows (seed sheets → occurrenceID FK); 3 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; acquisitionDate = photo-date proxy for 2 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-210851`.

## 20261004 — Stage C held rows resolved
- occ 3293 = 1.042 g, occ 3295 = 1.1741 g (Sven, from envelope of event 517); loaded with germplasmID 1016/1018.

## 20261004-211013 — germplasm_seeds --load germplasm_results_20261004c.json
- staged 127 rows (OK 1, FLAG 2, NO_SEED 0, LOADED 124, SKIP 0); acquisitionDate sources {'photo': 3}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-211013 — germplasm_seeds --commit --apply
- inserted 1 Germplasm rows (seed sheets → occurrenceID FK); 2 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; acquisitionDate = photo-date proxy for 1 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-211013`.

## 20261004 — Stage C held row resolved
- occ 3248 germplasmID = 1095 (Sven, from envelope of event 501); loaded.

## 20261004-211121 — germplasm_seeds --load germplasm_results_20261004c.json
- staged 127 rows (OK 1, FLAG 1, NO_SEED 0, LOADED 125, SKIP 0); acquisitionDate sources {'photo': 2}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-211121 — germplasm_seeds --commit --apply
- inserted 1 Germplasm rows (seed sheets → occurrenceID FK); 1 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; acquisitionDate = photo-date proxy for 1 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-211121`.

## 20261004 — Stage C held row resolved
- occ 3276 germplasmID = 1108 (Sven, from envelope of event 512); loaded.

## 20261004-211215 — germplasm_seeds --load germplasm_results_20261004c.json
- staged 127 rows (OK 1, FLAG 0, NO_SEED 0, LOADED 126, SKIP 0); acquisitionDate sources {'photo': 1}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-211215 — germplasm_seeds --commit --apply
- inserted 1 Germplasm rows (seed sheets → occurrenceID FK); 0 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; acquisitionDate = photo-date proxy for 1 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-211215`.

## 20261004 — Stage C held row resolved
- occ 3299 weight = 0.0657 g (Sven, from envelope of event 518); loaded. All envelope-check holds now resolved; only occ 3412 (issue #21) remains held.

## 20261004-211455 — germplasm_seeds --load germplasm_results_20261004.json
- staged 0 rows (OK 0, FLAG 0, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-211522 — germplasm_seeds --load germplasm_results_20261004.json
- staged 123 rows (OK 0, FLAG 1, NO_SEED 0, LOADED 122, SKIP 0); acquisitionDate sources {'photo': 1}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004 — occ 3412 weight confirmed; issue #21 image
- occ 3412 weight = 0.1314 g (Sven, envelope); still HELD (no germplasmID). Seed-sheet photo (EXIF/GPS stripped, rotated) posted to issue #21 via branch `issue-assets` (not main).
- germplasm_seeds --load now resolves sheets of earlier batches directly from Field_forms/<year>/ (re-running an old results file no longer drops its rows from the registry).

## 20261004 — Germplasm.personID + seed-cleaner initials
- Added Germplasm.personID (FK Persons; Terms 141). Placeholder Persons JY (6), AS (7). SB = Sam Billingsley (Persons 4, Sven confirmed); fixed swapped first/last name on Persons 4. Mapping in staging_2026/initials_persons.csv (PM->2, IR->3 assumed).

## 20261004-224541 — germplasm_seeds --load germplasm_results_20261004d.json
- staged 40 rows (OK 39, FLAG 1, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'sheet': 12, 'photo': 28}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-224630 — germplasm_seeds --commit --apply
- inserted 39 Germplasm rows (seed sheets → occurrenceID FK); 1 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 0 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 27 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-224630`.

## 20261004-224630 — germplasm_seeds --sheets-mm --apply
- linked 15 seed-sheet / location-form images to Multimedia (Event tableID 11 / Location tableID 9), copied as LEPA_<date>_<sha8>.jpg. Backup `LEPA_SQL.db.bak-germplasmmm-20261004-224630`.

## 20261004-224712 — germplasm_seeds --load germplasm_results_20261004d.json
- staged 40 rows (OK 0, FLAG 1, NO_SEED 0, LOADED 39, SKIP 0); acquisitionDate sources {'photo': 1}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-224712 — germplasm_seeds --sheets-mm --apply
- linked 1 seed-sheet / location-form images to Multimedia (Event tableID 11 / Location tableID 9), copied as LEPA_<date>_<sha8>.jpg. Backup `LEPA_SQL.db.bak-germplasmmm-20261004-224712`.

## 20261004-224956 — germplasm_seeds --load germplasm_results_20261004.json
- staged 123 rows (OK 0, FLAG 1, NO_SEED 0, LOADED 122, SKIP 0); acquisitionDate sources {'photo': 1}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-224956 — germplasm_seeds --commit --apply
- inserted 0 Germplasm rows (seed sheets → occurrenceID FK); 1 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 16 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 0 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-224956`.

## 20261004-224956 — germplasm_seeds --load germplasm_results_20261004b.json
- staged 49 rows (OK 0, FLAG 0, NO_SEED 0, LOADED 49, SKIP 0); acquisitionDate sources {}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-224956 — germplasm_seeds --commit --apply
- inserted 0 Germplasm rows (seed sheets → occurrenceID FK); 0 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 11 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 0 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-224956`.

## 20261004-224956 — germplasm_seeds --load germplasm_results_20261004c.json
- staged 127 rows (OK 0, FLAG 0, NO_SEED 0, LOADED 127, SKIP 0); acquisitionDate sources {}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-224956 — germplasm_seeds --commit --apply
- inserted 0 Germplasm rows (seed sheets → occurrenceID FK); 0 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 12 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 0 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-224956`.

## 20261004 — Stage C batch 4 (locs 13/21/24/51) + who/when backfill
- Batch 4 (PXL_20261004_2135–2138): 4 location forms + 12 sheets; +39 Germplasm (IDs 1166–1369); held occ 3003 (0.1064 vs 0.0064 g). Loc 51 event 719 (occ 3847–3851) has no envelope (ID gap 1358–1362). Event 718 sheet (no plants) linked to its event; its note reads "cows", eventRemarks says "Lewisia" — asked Sven.
- Dedicated initials/date re-read of the 101 earlier sheets → 39 rows backfilled with personID (Sam Billingsley 30 incl. new batch, JY 16, PM 4, AS 1) and written dates. JY written after barcodes on PXL_20261004_194041304 (occ 3297–3300) left unassigned (collector or cleaner? asked Sven).
- 2026 Germplasm = 337; 0 duplicate IDs; 0 bad personID FKs; all estimates match the equation.

## 20261004-231107 — germplasm_seeds --load germplasm_results_20261004c.json
- staged 127 rows (OK 0, FLAG 0, NO_SEED 0, LOADED 127, SKIP 0); acquisitionDate sources {}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-231107 — germplasm_seeds --commit --apply
- inserted 0 Germplasm rows (seed sheets → occurrenceID FK); 0 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 4 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 0 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-231107`.

## 20261004 — initials confirmed
- PM = Peggy Martinez, IR = Ian Robertson (Sven confirmed). JY = cleaner for occ 3297–3300 (Sven) -> backfilled personID 6.

## 20261004-231149 — germplasm_seeds --load germplasm_results_20261004d.json
- staged 40 rows (OK 1, FLAG 0, NO_SEED 0, LOADED 39, SKIP 0); acquisitionDate sources {'photo': 1}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-231149 — germplasm_seeds --commit --apply
- inserted 1 Germplasm rows (seed sheets → occurrenceID FK); 0 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 0 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 1 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-231149`.
- occ 3003 = 0.1064 g (Sven); loaded.

## 20261004-231515 — germplasm_seeds --load germplasm_results_20261004e.json
- staged 59 rows (OK 57, FLAG 0, NO_SEED 2, LOADED 0, SKIP 0); acquisitionDate sources {'sheet': 5, 'photo': 52}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-231558 — germplasm_seeds --load germplasm_results_20261004e.json
- staged 59 rows (OK 54, FLAG 3, NO_SEED 2, LOADED 0, SKIP 0); acquisitionDate sources {'sheet': 5, 'photo': 52}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-231558 — germplasm_seeds --commit --apply
- inserted 54 Germplasm rows (seed sheets → occurrenceID FK); 3 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 0 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 49 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-231558`.

## 20261004-231558 — germplasm_seeds --sheets-mm --apply
- linked 19 seed-sheet / location-form images to Multimedia (Event tableID 11 / Location tableID 9), copied as LEPA_<date>_<sha8>.jpg. Backup `LEPA_SQL.db.bak-germplasmmm-20261004-231558`.

## 20261004 — Stage C location 18 (EO18) — LOADED
- 19 photos (1 location form + 18 sheets = all 18 events / 59 plants). +54 Germplasm (IDs 1507–1578); SB-dated sheets 09/24 and 09/25/2026 (Sam Billingsley).
- Event 328 (occ 2596, 2597): envelope in hand but seeds NOT cleaned (no Germ/Weight) → new issue #23 (general: uncleaned events by location).
- Held (HOLD): occ 2611 (0.0325 vs 0.6325), 2612 (0.1379 vs 0.379), 2604 (0.8210 vs 0.8240).
- Issue #22 generalised to missing envelopes by location (+ loc 51 event 719). 2026 Germplasm = 392.

## 20261004-233859 — germplasm_seeds --load germplasm_results_20261004e.json
- staged 59 rows (OK 3, FLAG 0, NO_SEED 2, LOADED 54, SKIP 0); acquisitionDate sources {'photo': 3}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-233859 — germplasm_seeds --commit --apply
- inserted 3 Germplasm rows (seed sheets → occurrenceID FK); 0 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 0 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 3 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-233859`.
- Loc 18 holds resolved (Sven): 2604 = 0.8210 g, 2611 = 0.0325 g, 2612 = 0.1379 g; loaded.

## 20261004-234003 — germplasm_seeds --load germplasm_results_20261004f.json
- staged 15 rows (OK 15, FLAG 0, NO_SEED 0, LOADED 0, SKIP 0); acquisitionDate sources {'photo': 15}; 0 events incomplete. Review staging_2026/germplasm_staging.csv.

## 20261004-234003 — germplasm_seeds --commit --apply
- inserted 15 Germplasm rows (seed sheets → occurrenceID FK); 0 held as FLAG; 0 seed-quality notes appended to Events.eventRemarks; 0 loaded rows backfilled (personID/acquisitionDate); new placeholder Persons none; acquisitionDate = photo-date proxy for 15 rows (issue #20). Backup `LEPA_SQL.db.bak-germplasm-20261004-234003`.

## 20261004-234003 — germplasm_seeds --sheets-mm --apply
- linked 10 seed-sheet / location-form images to Multimedia (Event tableID 11 / Location tableID 9), copied as LEPA_<date>_<sha8>.jpg. Backup `LEPA_SQL.db.bak-germplasmmm-20261004-234003`.

## 20261004 — Stage C location 27 (EO8) — LOADED
- 10 photos (1 location form + 9 sheets = all 9 events / 15 plants). +15 Germplasm (IDs 1523–1537), no holds, no initials/dates on sheets. 2026 Germplasm = 410.

## 20261004 — REPORT_2026_campaign.md updated
- Added Stage C: per-location seed-accession tally (cleaned 410 / remaining 1,171; loc 17 cleaned-not-imaged per Sven), cleaning priorities from SRK_bioinformatics Phase 5 (76-mother gap across 35 demes; pilot B1 anchor loc 8), §3b method, open issues #20–#23, data-product counts.
- Report: added Fertile plants column (Events.organismQuantityFertile) to the per-location events/occurrences tally and to the cleaning-priority table (Sven, 2026-10-04).
- Report: occurrence tally now separates Fertile plants (counted, all plants per event) from Occurrences (sampled) and adds % sampled (Sven).
- Report: per-location tally gains Completion (accessions/occurrences) and Priority (rank by fertile plants counted; done / finish / image only / blocked); cleaning-priority list re-ordered by size with Phase 5 gap as supporting info (Sven: prioritise large locations).
