# 2026 seed cleaning — leaderboard

*Generated 2026-10-25 from `LEPA_SQL.db` by `seed_cleaners_report.py`. A **germplasm** is all the seeds of one mother plant (occurrence); each has exactly one cleaner, recorded from the initials on the event envelope (`Germplasm.personID`).*

**735 germplasm** cleaned and loaded for 2026; **491** have a known cleaner, **244** are not yet assigned (no initials on the envelope, or several initials written once for the whole envelope).

| Rank | Cleaner | Germplasm | Share of assigned | Seed (g) | Est. seeds | Locations | Envelopes (events) | Dates written on envelopes |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Ian Robertson | 181 | 37% | 35.41 | 83,102 | 11 | 70 | — |
| 2 | Sam Billingsley | 80 | 16% | 10.59 | 24,838 | 12 | 32 | 2026-08-12 → 2026-10-20 |
| 3 | Jayden Yun | 56 | 11% | 12.57 | 29,522 | 6 | 21 | 2026-10-12 → 2026-10-12 |
| 4 | Alex Scott | 42 | 9% | 17.49 | 41,082 | 5 | 22 | 2026-10-02 → 2026-10-19 |
| 5 | Lizzie Berrier | 41 | 8% | 13.51 | 31,736 | 3 | 13 | 2026-10-02 → 2026-10-22 |
| 6 | Peggy Martinez | 33 | 7% | 10.37 | 24,366 | 4 | 15 | 2026-10-16 → 2026-10-22 |
| 7 | Ashley Zahurak | 27 | 5% | 13.39 | 31,473 | 2 | 7 | 2026-10-02 → 2026-10-16 |
| 8 | Isaac Carretero | 18 | 4% | 3.92 | 9,195 | 3 | 5 | 2026-10-15 → 2026-10-15 |
| 9 | Kylie Stear | 12 | 2% | 2.51 | 5,893 | 2 | 4 | 2026-09-25 → 2026-10-16 |
| 10 | CR [unidentified - seed cleaning 2026] | 1 | 0% | 0.56 | 1,306 | 1 | 1 | 2026-10-19 → 2026-10-19 |
| — | *— not yet assigned —* | 244 | — | 55.49 | 130,289 | 11 | 64 | — |

## By location

| Location | Germplasm | Ian Robertson | Sam Billingsley | Jayden Yun | Alex Scott | Lizzie Berrier | Peggy Martinez | Ashley Zahurak | Isaac Carretero | Kylie Stear | CR [unidentified - seed cleaning 2026] | Not assigned |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| loc 1 (EO38) | 37 |  | 2 | 18 | 11 |  | 6 |  |  |  |  |  |
| loc 3 (EO52) | 1 | 1 |  |  |  |  |  |  |  |  |  |  |
| loc 5 (EO68-3) | 10 | 1 | 4 |  | 5 |  |  |  |  |  |  |  |
| loc 10 (EO27-3) | 7 | 4 | 3 |  |  |  |  |  |  |  |  |  |
| loc 11 (EO27-1) | 125 | 50 | 7 | 13 |  |  |  |  |  |  |  | 55 |
| loc 13 (EO30-1) | 16 |  |  |  |  |  |  |  |  |  |  | 16 |
| loc 16 (EO18-7) | 76 |  | 6 | 3 | 16 | 12 | 8 | 20 | 2 | 5 | 1 | 3 |
| loc 17 (EO18-7) | 103 |  | 16 | 4 |  |  |  |  |  |  |  | 83 |
| loc 18 (EO18-8) | 59 |  | 6 | 4 |  | 17 |  |  | 1 |  |  | 31 |
| loc 19 (EO18-7) | 1 | 1 |  |  |  |  |  |  |  |  |  |  |
| loc 20 (EO25-A) | 38 |  | 3 |  | 9 | 12 |  | 7 |  | 7 |  |  |
| loc 21 (EO25-B) | 8 | 5 | 1 |  |  |  |  |  |  |  |  | 2 |
| loc 24 (EO24) | 5 | 5 |  |  |  |  |  |  |  |  |  |  |
| loc 26 (EO70) | 42 | 19 | 8 |  |  |  |  |  | 15 |  |  |  |
| loc 27 (EO8) | 15 |  |  |  |  |  | 15 |  |  |  |  |  |
| loc 28 (EO8) | 122 | 77 |  | 14 | 1 |  | 4 |  |  |  |  | 26 |
| loc 39 (EO67) | 6 |  |  |  |  |  |  |  |  |  |  | 6 |
| loc 42 (EO30-2) | 34 | 16 | 8 |  |  |  |  |  |  |  |  | 10 |
| loc 51 (EO30-3) | 16 |  | 16 |  |  |  |  |  |  |  |  |  |
| loc 52 (EO30-4) | 7 | 2 |  |  |  |  |  |  |  |  |  | 5 |
| loc 53 (EO112) | 7 |  |  |  |  |  |  |  |  |  |  | 7 |

**Notes**
- *Est. seeds* comes from seed weight via the 1000-seed-weight equation (negative estimates for very light lots are counted as 0).
- *Dates written on envelopes* covers only envelopes where the cleaner wrote a date. Photo or posting dates used as stand-ins are excluded (see issue #20).
- Germplasm without initials were attributed from **handwriting samples** where possible (Ian; Peggy for location 27), and each match was confirmed by Sven. The rest are tracked in [issue #24](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/24).
- To assign the remaining germplasm, fill in `staging_2026/cleaner_assignment.csv` (one row per envelope) and run `germplasm_seeds.py --assign-cleaners`.
- Campaign context: [`REPORT_2026_campaign.md`](REPORT_2026_campaign.md).
