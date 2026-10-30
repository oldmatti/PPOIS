# Лабораторная работа №2: Крупный ООП-проект (Домен: Деканат)

## Спецификация классов

| Класс | Поля | Методы | Ассоциации (связанные классы) |
| :--- | :--- | :--- | :--- |
| Person | 4 | 2 | — |
| Employee | 4 | 3 | Department |
| Student | 5 | 4 | StudyGroup, GradeBook |
| Professor | 4 | 4 | Department, Subject |
| Dean | 3 | 5 | Faculty, Employee |
| DeputyDean | 3 | 4 | Faculty, Student |
| Secretary | 2 | 4 | Document, Order |
| Curator | 2 | 3 | StudyGroup, Employee |
| HeadOfDepartment | 3 | 3 | Department, Professor |
| HeadStudent | 2 | 4 | StudyGroup, Student |
| University | 4 | 3 | Faculty, Building |
| Faculty | 4 | 4 | Department, Dean, Specialty |
| Department | 4 | 4 | Professor, HeadOfDepartment |
| Specialty | 4 | 3 | Curriculum, Faculty |
| StudyGroup | 5 | 5 | Subgroup, Curator, HeadStudent, Specialty |
| Subgroup | 4 | 3 | StudyGroup, Student |
| Classroom | 4 | 3 | Building |
| Building | 3 | 2 | Classroom |
| AcademicYear | 3 | 2 | Semester |
| Semester | 4 | 3 | AcademicYear, Curriculum |
| Subject | 4 | 2 | Curriculum |
| Curriculum | 4 | 4 | Subject, Specialty |
| Schedule | 3 | 4 | Lesson, StudyGroup, Classroom |
| Lesson | 5 | 3 | Subject, Professor, Classroom |
| Lecture | 2 | 2 | Lesson |
| Seminar | 2 | 2 | Lesson, Subgroup |
| LabWork | 3 | 2 | Lesson, Subgroup |
| Exam | 4 | 3 | Subject, StudyGroup, Professor |
| Credit | 4 | 2 | Subject, StudyGroup |
| Coursework | 4 | 3 | Student, Professor, Subject |
| Thesis | 4 | 3 | Student, Professor, Department |
| GradeBook | 3 | 4 | Student, Grade |
| Grade | 4 | 2 | Subject, Professor |
| AttendanceRecord | 4 | 3 | Student, Lesson |
| ExamTicket | 3 | 2 | Exam |
| Retake | 4 | 3 | Exam, Student, Professor |
| ExpulsionCandidateList | 3 | 4 | Student, Faculty |
| Document | 4 | 2 | — |
| Order | 4 | 3 | Document, Secretary |
| ExpulsionOrder | 2 | 2 | Order, Student |
| EnrollmentOrder | 2 | 2 | Order, Student |
| ScholarshipOrder | 2 | 2 | Order, Student |
| Certificate | 3 | 2 | Document, Student |
| StudentIDCard | 4 | 3 | Student, Faculty |
| Petition | 4 | 3 | Student, Document |
| Diploma | 4 | 2 | Student, Specialty |
| AcademicTranscript | 3 | 2 | Student, GradeBook |
| Dormitory | 4 | 3 | DormRoom, Building |
| DormRoom | 4 | 3 | Student, Dormitory |
| Scholarship | 4 | 3 | Student, ScholarshipOrder |

## Исключения (12)
* `DeaneryException`
* `StudentNotFoundException`
* `InvalidGradeException`
* `ScheduleConflictException`
* `InsufficientCreditsException`
* `InvalidGroupTransferException`
* `DormitoryFullException`
* `ScholarshipDeniedException`
* `ExpulsionRulesViolationException`
* `InvalidDocumentFormatException`
* `UnauthorizedAccessException`
* `RetakeLimitExceededException`

## Итоговая статистика
* Поля: 175
* Поведения: 146
* Ассоциации: 77
* Исключения: 12