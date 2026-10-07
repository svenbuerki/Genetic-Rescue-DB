# 2026 seed cleaning — leaderboard

*Generated 2026-10-06 from `LEPA_SQL.db` by `seed_cleaners_report.py`. A **germplasm** is all the seeds of one mother plant (occurrence); each has exactly one cleaner, recorded from the initials on the event envelope (`Germplasm.personID`).*

**611 germplasm** cleaned and loaded for 2026; **344** have a known cleaner, **267** are not yet assigned (no initials on the envelope, or several initials written once for the whole envelope).

| Rank | Cleaner | Germplasm | Share of assigned | Seed (g) | Est. seeds | Locations | Envelopes (events) | Dates written on envelopes |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Ian Robertson | 179 | 52% | 35.18 | 82,585 | 11 | 70 | — |
| 2 | Sam Billingsley | 70 | 20% | 6.75 | 15,809 | 10 | 27 | 2026-08-12 → 2026-09-25 |
| 3 | Jaden Yun | 39 | 11% | 7.44 | 17,464 | 4 | 16 | — |
| 4 | Peggy Martinez | 25 | 7% | 6.79 | 15,946 | 3 | 12 | — |
| 5 | Alex Scott | 17 | 5% | 8.98 | 21,108 | 3 | 8 | — |
| 6 | Isaac Carretero | 14 | 4% | 2.54 | 5,969 | 1 | 3 | — |
| — | *— not yet assigned —* | 267 | — | 57.55 | 135,110 | 10 | 69 | — |

## By location

| Location | Germplasm | Ian Robertson | Sam Billingsley | Jaden Yun | Peggy Martinez | Alex Scott | Isaac Carretero | Not assigned |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| loc 1 (EO38) | 32 |  | 2 | 13 | 6 | 11 |  |  |
| loc 3 (EO52) | 1 | 1 |  |  |  |  |  |  |
| loc 5 (EO68-3) | 10 | 1 | 4 |  |  | 5 |  |  |
| loc 10 (EO27-3) | 7 | 4 | 3 |  |  |  |  |  |
| loc 11 (EO27-1) | 125 | 50 | 7 | 13 |  |  |  | 55 |
| loc 13 (EO30-1) | 16 |  |  |  |  |  |  | 16 |
| loc 17 (EO18-7) | 103 |  | 16 | 2 |  |  |  | 85 |
| loc 18 (EO18-8) | 57 |  | 5 |  |  |  |  | 52 |
| loc 19 (EO18-7) | 1 | 1 |  |  |  |  |  |  |
| loc 21 (EO25-B) | 8 | 5 | 1 |  |  |  |  | 2 |
| loc 24 (EO24) | 5 | 5 |  |  |  |  |  |  |
| loc 26 (EO70) | 39 | 17 | 8 |  |  |  | 14 |  |
| loc 27 (EO8) | 15 |  |  |  | 15 |  |  |  |
| loc 28 (EO8) | 122 | 77 |  | 11 | 4 | 1 |  | 29 |
| loc 39 (EO67) | 6 |  |  |  |  |  |  | 6 |
| loc 42 (EO30-2) | 34 | 16 | 8 |  |  |  |  | 10 |
| loc 51 (EO30-3) | 16 |  | 16 |  |  |  |  |  |
| loc 52 (EO30-4) | 7 | 2 |  |  |  |  |  | 5 |
| loc 53 (EO_NEW2026) | 7 |  |  |  |  |  |  | 7 |

**Notes**
- *Est. seeds* comes from seed weight via the 1000-seed-weight equation (negative estimates for very light lots are counted as 0).
- *Dates written on envelopes* covers only envelopes where the cleaner wrote a date. Photo or posting dates used as stand-ins are excluded (see issue #20).
- Germplasm without initials were attributed from **handwriting samples** where possible (Ian Robertson; Peggy Martinez for location 27), and each match was confirmed by the PI. The rest are tracked in [issue #24](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/24).
- To assign the remaining germplasm, fill in `staging_2026/cleaner_assignment.csv` (one row per envelope) and run `germplasm_seeds.py --assign-cleaners`.
- Campaign context: [`REPORT_2026_campaign.md`](REPORT_2026_campaign.md).
