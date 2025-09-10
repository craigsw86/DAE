# learning/PLAN.md

> This is my one-page learning plan for the month. I will complete and commit this file during the 15-minute selection clinic. It records the technology I chose to learn, why I chose it for my capstone, the three focused tasks I will complete, and the proof I will capture to show I did the work.

---

## Student commitment

-   **Name:** Craig Weinstein
-   **Date created:** 2025-09-02

I commit to treat this plan as my personal roadmap: I will keep dates realistic, finish each small task, capture evidence of success, and update this file if anything changes.

---

## Chosen technology

-   **Technology name:** Black Duck
-   **Technology version (if applicable):** 2025.7.0

### Why I chose this technology

https://www.youtube.com/watch?v=SSFSwh9Uzu8

---

## First-day actions

1. Finalize the **Chosen technology** and **Why I chose this technology** fields above.
2. Draft three small integration tasks below with realistic start and target completion dates.
3. Commit this file to the repository at `learning/PLAN.md` before the end of the 15-minute clinic.
4. Record where I will start Task 1 (for example: local branch name or workspace folder) under Task 1.
5. If a task feels too large, I will make it smaller and update the dates here.

---

## My three integration tasks (small, testable, dated)


**Task 1 — Title:** Install and Configure Black Duck for Dependency Scans

-   **Description:** Set up Black Duck for the React + Django codebase and perform the first dependency vulnerability scan
-   **Start date:** 2025-09-02
-   **Target completion date:** 2025-09-03
-   **Success criterion (explicit):** Black Duck completes a scan of dependencies without errors and produces a results list.
-   **Proof method (what I will capture to show success):** Screenshot of scan output showing dependency analysis.
-   **Where I will start Task 1:** Local branch `blackduck-setup`

**Task 2 — Title:** Generate Initial Security & License Report

-   **Description:** Use Black Duck to generate a security and license compliance report summarizing vulnerabilities and risk levels.
-   **Start date:** 2025-09-03
-   **Target completion date:** 2025-09-04
-   **Success criterion (explicit):** Report lists all project dependencies, severity ratings, and license information.
-   **Proof method (what I will capture to show success):** Save report PDF/HTML in repo and screenshot the results summary.

**Task 3 — Title:** Integrate Black Duck Scan into Development Workflow

-   **Description:** Document and automate a repeatable scan step so future dependency updates can be checked quickly.
-   **Start date:** 2025-09-04
-   **Target completion date:** 2025-09-05
-   **Success criterion (explicit):** A single documented command runs Black Duck scan and outputs updated report.
-   **Proof method (what I will capture to show success):** Screenshot of automated scan run and new report saved in repo.

> Note: Keep each task small enough that one task = one focused change or one short demo.

---

## Risks, assumptions, and blockers (one-line each)

List any access or external requirements that could block completion. For example:

-   Requires remote DB credentials.
-   Needs API key for third-party service.
-   Depends on another repo update.

---

## My weekly timeline (one-line plan)

-   **Week 1:** Commit this PLAN and start Task 1.
-   **Week 2:** Continue Task 1; produce a draft PR or demo; start Task 2.
-   **Week 3:** Continue Task 2; add tests/logging and peer review; start Task 3.
-   **Week 4:** Finalize PR(s) or demo(s); draft `learning/README.md` and `learning/REFLECTION.md`.

## UPDATES (9/8/2025):
- Tried to download the Black Duck SCA program directly from the website, but encountered roadblocks there (the Black Duck website wouldn't accept messages from a Gmail address); now investigating free open-souce alternatives on GitHub from Black Duck themselves.
- Downloaded Detect as well as Black Duck Security Scan from GitHub.

