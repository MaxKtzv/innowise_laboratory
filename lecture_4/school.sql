-- Ensure all changes are applied atomically
BEGIN;

-- Create table students
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

-- Create table grades
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL,
    CONSTRAINT fk_grades_student FOREIGN KEY (student_id) REFERENCES students (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_grade_range CHECK (grade BETWEEN 1 AND 100)
);

-- Create indexes on students.full_name and grades.student_id
CREATE INDEX IF NOT EXISTS idx_full_name ON students (full_name);
CREATE INDEX IF NOT EXISTS idx_student_id ON grades (student_id);

-- Insert students' information
INSERT INTO students (full_name, birth_year)
VALUES ('Alice Johnson', 2005),
       ('Brian Smith', 2004),
       ('Carla Reyes', 2006),
       ('Daniel Kim', 2005),
       ('Eva Thompson', 2003),
       ('Felix Nguyen', 2007),
       ('Grace Patel', 2005),
       ('Henry Lopez', 2004),
       ('Isabella Martinez', 2006);

-- Insert students' grades in the corresponding subjects
INSERT INTO grades (student_id, subject, grade)
VALUES (1, 'Math', 88),
       (1, 'English', 92),
       (1, 'Science', 85),
       (2, 'Math', 75),
       (2, 'History', 83),
       (2, 'English', 79),
       (3, 'Science', 95),
       (3, 'Math', 91),
       (3, 'Art', 89),
       (4, 'Math', 84),
       (4, 'Science', 88),
       (4, 'Physical Education', 93),
       (5, 'English', 90),
       (5, 'History', 85),
       (5, 'Math', 88),
       (6, 'Science', 72),
       (6, 'Math', 78),
       (6, 'English', 81),
       (7, 'Art', 94),
       (7, 'Science', 87),
       (7, 'Math', 90),
       (8, 'History', 77),
       (8, 'Math', 83),
       (8, 'Science', 80),
       (9, 'English', 96),
       (9, 'Math', 89),
       (9, 'Art', 92);

COMMIT;

-- Find all grades for Alice Johnson
SELECT s.id        AS "ID",
       s.full_name AS "Name",
       g.grade     AS "Grade"
FROM grades AS g
       INNER JOIN students AS s ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson';

-- Calculate the average grade for all students
SELECT s.id         AS "ID",
       s.full_name  AS "Name",
       AVG(g.grade) AS "Average Grade"
FROM students AS s
         INNER JOIN grades AS g ON s.id = g.student_id
GROUP BY s.id;

-- List all students born after 2004
SELECT id        AS "ID",
       full_name AS "Name"
FROM students
WHERE birth_year > 2004;

-- Calculate the average grade for all subjects
SELECT subject    AS "Subject",
       AVG(grade) AS "Average Grade"
FROM grades
GROUP BY subject;

-- Find top three students
SELECT s.id         AS "ID",
       s.full_name  AS "Name",
       AVG(g.grade) AS "Average Grade"
FROM students AS s
         INNER JOIN grades AS g ON s.id = g.student_id
GROUP BY s.id
ORDER BY "Average Grade" DESC
LIMIT 3;

-- Show all students who have scored below 80
SELECT DISTINCT s.id        AS "ID",
                s.full_name AS "Name"
FROM students AS s
         INNER JOIN grades AS g ON s.id = g.student_id
WHERE g.grade < 80;
