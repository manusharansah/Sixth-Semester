# Software Engineering Lab — Info

**Institute of Engineering, Advanced College of Engineering and Management (Tribhuvan University)**  
**Department of Electronics and Computer Engineering**  
**Subject:** Software Engineering  
**Submitted by:** Manu Sharan Kumar (ACE080BCT037)

This file summarizes the three lab sessions completed for the Software Engineering lab, all built around one running project: an **Examination Management System (EMS)** — a web application to digitize exam scheduling, hall/invigilator allocation, student registration, admit cards, mark entry, result publication, grade calculation, notifications, and transcripts for an academic institution.

The work followed the standard SE lab progression: first specify the system (SRS), then model it (UML diagrams), then build it (working full-stack implementation).

---

## Lab 1 — Software Requirement Specification (SRS)

**What was instructed:** Choose a software system, write out a formal problem statement and proposed solution, and produce a complete Software Requirement Specification covering functional requirements, non-functional requirements, and constraints.

**What was done:**
- Picked the **Examination Management System** as the subject system, since manual/spreadsheet-based exam administration is error-prone and hard to audit for institutions with many students.
- Wrote a **Problem Statement** describing the pain points: scheduling conflicts, hall over-allocation, late result publication, and no centralized student performance record.
- Wrote a **Proposed Solution** describing how EMS automates the exam lifecycle end-to-end (scheduling, conflict detection, invigilator assignment, self-service registration/admit-cards/results, permanent grade records, statistical reports, and notifications).
- Defined **15 Functional Requirements (R-1 to R-15)**, each with Description / Input / Process / Output:

  | ID | Requirement |
  |---|---|
  | R-1 | User registration and role assignment |
  | R-2 | User login and session management |
  | R-3 | Examination schedule creation |
  | R-4 | Hall allocation |
  | R-5 | Invigilator assignment |
  | R-6 | Student examination registration |
  | R-7 | Admit card generation |
  | R-8 | Mark entry and validation |
  | R-9 | Result publication |
  | R-10 | Grade calculation |
  | R-11 | Notification and alert system |
  | R-12 | Performance report generation |
  | R-13 | Academic transcript generation |
  | R-14 | Examination schedule publication and visibility |
  | R-15 | Role-based access control |

- Defined **5 Non-Functional Requirements**: page load performance (NR-1), scalability to 500 concurrent users (NR-2), data integrity/no overwrites (NR-3), role-based data privacy (NR-4), and password security via hashing (NR-5).
- Defined **4 Constraints**: grading policy must exist before results publish (C-1), the system requires internet with no offline mode (C-2), it only covers exams/marks/results — not a full SIS/LMS (C-3), and it supports a single institution/campus in v1.0 (C-4).

**Output of this lab:** a complete SRS document, later used as the single source of truth for both the diagrams (Lab 2) and the code (Lab 3).

---

## Lab 2 — UML Modelling (Use Case & Class Diagrams)

**What was instructed:** Translate the SRS from Lab 1 into UML diagrams — a use case diagram capturing actor/system interactions, and a class diagram capturing the system's data model and relationships.

**What was done:**

### Use Case Diagram
- Modelled **three actors**: Admin, Faculty, and Student, matching the roles from R-15.
- **Admin** use cases: Register or Login, Create Exam Schedule, Allocate Exam Hall, Assign Invigilator, Publish Schedule, Review and Publish Result, Generate Performance Report.
- **Faculty** use cases: Register or Login, Enter and Submit Marks, View Assigned Invigilations.
- **Student** use cases: Register for Exam, Download Admit Card, View Result & Transcript.
- Modelled `<<include>>` relationships to show dependent behavior — e.g., "Register for Exam" includes "Download Admit Card" becoming available; "Publish Schedule" and "Review and Publish Result" both include "Receive Notification"; "Review and Publish Result" includes "Generate Performance Report".

### Class Diagram
- Modelled a **User** base class (`userId`, `name`, `email`, `passwordHash`, `role`, `isVerified`) with `register()`, specialized into **Admin**, **Faculty**, and **Student** subclasses — matching R-1/R-15.
- **Admin** class: `publishSchedule()`, `approveResults()`, `assignRole()`.
- **Faculty** class: `enterMarks()`, `viewInvigilation()`.
- **Student** class: `rollNo`, `semester`, `registerForExam()`, `downloadAdmitCard()`.
- Modelled supporting entity classes and their relationships to the User hierarchy:
  - **ExamSchedule** (created by Admin) — subject, date, time, `isPublished`, `publish()`.
  - **ExamHall** — capacity, availability, `checkAvailability()`; allocated to a schedule.
  - **Invigilations** — links a Faculty member to a schedule/hall, with `assign()`.
  - **ExamRegistration** — links a Student to a schedule, with status Pending/Confirmed and `confirm()`.
  - **AdmitCard** — generated from a registration, with `generate()`.
  - **Result** — marks, total marks, `isPublished`, `publish()`; linked to Student and Schedule.
  - **Notification** — recipient, message, `isRead`, `send()`.
  - **PerformanceReport** — scope, generated data, `generate()`.
- This class diagram maps 1:1 onto the backend ORM models built in Lab 3.

**Output of this lab:** a use case diagram and class diagram consistent with every requirement defined in the SRS, used directly as the blueprint for implementation.

---

## Lab 3 — Implementation

**What was instructed:** Implement the system designed in Labs 1 and 2 as a working full-stack application, demonstrating that every SRS requirement is realized in the diagrammed data model.

**What was done:**
- Built a full-stack web app implementing all 15 functional requirements, organized by role (Admin / Faculty / Student / System) exactly as scoped in R-15:

  | Requirement(s) | Feature | Role |
  |---|---|---|
  | R-1, R-2 | Registration & login (JWT session) | All |
  | R-3, R-14 | Create, conflict-check, publish exam schedules | Admin |
  | R-4 | Allocate exam halls with capacity/booking checks | Admin |
  | R-5 | Assign invigilators, prevent double-booking | Admin |
  | R-6 | Student self-registration for published exams | Student |
  | R-7 | Downloadable PDF admit card | Student |
  | R-8 | Mark entry with full-marks validation | Faculty |
  | R-9 | Review, approve, publish results | Admin |
  | R-10 | Automatic grade/grade-point calculation | System |
  | R-11 | In-app notifications | All |
  | R-12 | Subject/batch performance reports (CSV export) | Admin |
  | R-13 | PDF academic transcript with CGPA | Student |
  | R-15 | Role-based access control on every endpoint | All |

- **Backend:** Python 3.12, FastAPI, SQLAlchemy ORM, SQLite; JWT auth (`python-jose`) with bcrypt password hashing; ReportLab for PDF generation (admit cards, transcripts). Code organized into `models.py` (matching the Lab 2 class diagram), `schemas.py`, `auth.py`, `utils.py`, and one router per requirement group (`auth`, `users`, `schedules`, `halls`, `invigilations`, `registrations`, `admit_cards`, `results`, `notifications`, `reports`, `transcripts`).
- **Frontend:** React 19 + TypeScript on TanStack Start (SSR)/TanStack Router, Vite 8, shadcn/ui + Tailwind CSS v4, TanStack Query, React Hook Form + Zod. Role-scoped dashboards (`admin.tsx`, `faculty.tsx`, `student.tsx`) with feature tabs (e.g., `SchedulesTab`, `HallsTab`, `ResultsTab`, `GradeScaleTab`, `ReportsTab`, `EnterMarksTab`, `ExamsTab`, `MyResultsTab`).
- **Non-functional requirements addressed in code:** stateless JWT for scalability (NR-2), bcrypt hashing (NR-5), server-side role checks on every request (NR-4), and DB-level uniqueness constraints against duplicate/overwritten records (NR-3).
- **Design decisions/assumptions recorded during build:** a student's `department` field doubles as their batch identifier for eligibility matching (R-6); results cannot be published until an admin configures at least one grade band (C-1); registration is open for any Published schedule whose date hasn't passed (R-6); email notification is stubbed for the demo, in-app notification is fully live (R-11); single-institution scope as per C-4.
- **Demo data:** seeded via `seed.py` with one Admin, one Faculty, and one Student account, plus a sample published exam (Software Engineering, SE401), used to walk through and screenshot the full workflow: login → schedule creation → hall allocation → invigilator assignment → student registration → admit card download → mark entry → result review/publish → grade display → notifications → performance report → transcript.
- **Source code:** published to GitHub at `https://github.com/manusharansah/Exam_Management_System.git`.

**Output of this lab:** a working EMS instance (FastAPI backend + TanStack Start frontend) that traces back to every requirement in the Lab 1 SRS and every class/use case in the Lab 2 diagrams, with a demo walkthrough and screenshots documenting each workflow stage.

---

## Summary

| Lab | Deliverable | Artifact |
|---|---|---|
| Lab 1 | Software Requirement Specification | Problem statement, 15 functional + 5 non-functional requirements, 4 constraints |
| Lab 2 | UML Diagrams | Use case diagram (3 actors), Class diagram (10 classes) |
| Lab 3 | Implementation | Full-stack EMS (FastAPI + TanStack Start), demo accounts, screenshots, GitHub repo |
