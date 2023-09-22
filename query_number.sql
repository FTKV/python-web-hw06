SELECT s.name, ROUND(AVG(g.grade), 2) as average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
GROUP BY g.student_id
ORDER BY average_grade DESC
LIMIT 5;

WITH average_grades as 
(SELECT s.name, c.title, ROUND(AVG(g.grade), 2) as average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN courses c ON c.id = g.course_id 
GROUP BY g.student_id, g.course_id
)
SELECT t.name, t.title, t.average_grade
FROM average_grades t
JOIN
(SELECT title, MAX(average_grade) as max_average_grade
FROM average_grades
GROUP BY title
) s ON s.title = t.title and s.max_average_grade = t.average_grade
ORDER BY t.title, t.average_grade;

SELECT g2.title, c.title, ROUND(AVG(g.grade), 2) as average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN courses c ON c.id = g.course_id
JOIN groups g2 ON g2.id = s.group_id
GROUP BY g2.id, g.course_id;

SELECT ROUND(AVG(g.grade), 2) as average_grade
FROM grades g;

SELECT l.name, group_concat(c.title, ', ') as title_list
FROM lecturers l
JOIN courses c ON c.lecturer_id = l.id
GROUP BY l.name;

SELECT g.title, s.name
FROM groups g
JOIN students s ON s.group_id = g.id
ORDER BY g.title, s.name;

SELECT g2.title, c.title, group_concat(g.grade, ', ') as grade_list
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN courses c ON c.id = g.course_id
JOIN groups g2 ON g2.id = s.group_id
GROUP BY g2.id, g.course_id;

SELECT l.name, ROUND(AVG(g.grade), 2) as average_grade
FROM grades g
JOIN courses c ON c.id = g.course_id
JOIN lecturers l ON l.id = c.lecturer_id
GROUP BY l.name;

SELECT s.name, group_concat(distinct c.title) as title_list
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN courses c ON c.id = g.course_id
GROUP BY g.student_id;

SELECT l.name, s.name, group_concat(distinct c.title) as title_list
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN courses c ON c.id = g.course_id
JOIN lecturers l ON l.id = c.lecturer_id
GROUP BY l.name, s.name;

SELECT l.name, s.name, ROUND(AVG(g.grade), 2) as average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN courses c ON c.id = g.course_id
JOIN lecturers l ON l.id = c.lecturer_id
GROUP BY l.name, s.name;

WITH gg as
(SELECT g3.course_id, MAX(g3.date_of) as max_date_of
FROM grades g3
GROUP BY g3.course_id
)
SELECT g2.title, c.title, g.date_of, group_concat(g.grade, ', ') as grade_list
FROM gg
JOIN grades g ON g.course_id = gg.course_id and g.date_of = gg.max_date_of
JOIN students s ON s.id = g.student_id
JOIN courses c ON c.id = g.course_id
JOIN groups g2 ON g2.id = s.group_id
GROUP BY g2.id, g.course_id;
