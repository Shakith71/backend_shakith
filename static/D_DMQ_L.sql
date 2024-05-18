MariaDB [MOVIE]> Show tables;
+-----------------+
| Tables_in_movie |
+-----------------+
| movies          |
| screens         |
| theaters        |
| tm              |
| users           |
+-----------------+

MariaDB [MOVIE]> DESC USERS;
+-------------------+-------------------------------+------+-----+---------------------+----------------+
| Field             | Type                          | Null | Key | Default             | Extra          |
+-------------------+-------------------------------+------+-----+---------------------+----------------+
| user_id           | int(11)                       | NO   | PRI | NULL                | auto_increment |
| name              | varchar(100)                  | NO   |     | NULL                |                |
| EMAIL             | varchar(50)                   | YES  | UNI | NULL                |                |
| phone             | varchar(15)                   | NO   |     | NULL                |                |
| gender            | enum('male','female','other') | NO   |     | NULL                |                |
| age               | int(11)                       | NO   |     | NULL                |                |
| city              | varchar(100)                  | NO   |     | NULL                |                |
| registration_date | timestamp                     | NO   |     | current_timestamp() |                |
| PASSWORD          | varchar(128)                  | YES  |     | NULL                |                |
| SALT              | varchar(128)                  | YES  |     | NULL                |                |
+-------------------+-------------------------------+------+-----+---------------------+----------------+


MariaDB [MOVIE]> DESC THEATERS;
+--------------+--------------+------+-----+---------+-------+
| Field        | Type         | Null | Key | Default | Extra |
+--------------+--------------+------+-----+---------+-------+
| theater_id   | int(11)      | NO   | PRI | NULL    |       |
| theater_name | varchar(100) | NO   |     | NULL    |       |
| location     | varchar(255) | NO   |     | NULL    |       |
+--------------+--------------+------+-----+---------+-------+

MariaDB [MOVIE]> DESC MOVIES;
+-------------+--------------+------+-----+---------+-------+
| Field       | Type         | Null | Key | Default | Extra |
+-------------+--------------+------+-----+---------+-------+
| MOVIE_ID    | int(11)      | NO   | PRI | NULL    |       |
| MOVIE_NAME  | varchar(30)  | YES  |     | NULL    |       |
| GENRE       | varchar(30)  | YES  |     | NULL    |       |
| RATING      | varchar(5)   | YES  |     | NULL    |       |
| DESCRIPTION | varchar(50)  | YES  |     | NULL    |       |
| URL         | varchar(100) | YES  |     | NULL    |       |
| RUN_TIME    | int(11)      | YES  |     | NULL    |       |
+-------------+--------------+------+-----+---------+-------+

MariaDB [MOVIE]> DESC SCREENS;
+---------------+-------------+------+-----+---------+-------+
| Field         | Type        | Null | Key | Default | Extra |
+---------------+-------------+------+-----+---------+-------+
| THEATER_ID    | int(11)     | NO   | PRI | NULL    |       |
| SCREEN_ID     | int(11)     | NO   | PRI | NULL    |       |
| SCREEN_NAME   | varchar(30) | YES  |     | NULL    |       |
| ELITE_SEATS   | int(11)     | YES  |     | NULL    |       |
| PREMIUM_SEATS | int(11)     | YES  |     | NULL    |       |
+---------------+-------------+------+-----+---------+-------+

+------------+---------+------+-----+---------+-------+
| Field      | Type    | Null | Key | Default | Extra |
+------------+---------+------+-----+---------+-------+
| THEATER_ID | int(11) | NO   | PRI | NULL    |       |
| MOVIE_ID   | int(11) | NO   | PRI | NULL    |       |
| SCREEN_ID  | int(11) | NO   | PRI | NULL    |       |
| SHOW_DATE  | date    | NO   | PRI | NULL    |       |
| SHOW_TIME  | time    | NO   | PRI | NULL    |       |
+------------+---------+------+-----+---------+-------+

MariaDB [MOVIE]> SELECT * FROM USERS;
+---------+---------------+---------------------------+------------+--------+-----+-------+---------------------+------------------------------------------------------------------+------------------+
| user_id | name          | EMAIL                     | phone      | gender | age | city  | registration_date   | PASSWORD                                                         | SALT             |
+---------+---------------+---------------------------+------------+--------+-----+-------+---------------------+------------------------------------------------------------------+------------------+
|       1 | Balamurugan S | balamurugan16sa@gmail.com | 9150109948 | male   |  19 | AVADI | 2024-05-05 12:06:17 | dbf6ce89830f744e01236a5e5f267b1c81970bab3fa637fdb5846d46b9e1a0e6 | 50f7f48a51e31c0d |
+---------+---------------+---------------------------+------------+--------+-----+-------+---------------------+------------------------------------------------------------------+------------------+

MariaDB [MOVIE]> SELECT * FROM THEATERS;
+------------+--------------+------------+
| theater_id | theater_name | location   |
+------------+--------------+------------+
|          1 | KAMALA       | VADAPALANI |
|          2 | ROHINI       | VANAGARAM  |
|          3 | RAKKI        | AMBATTUR   |
|          4 | WOODLANDS    | EGMORE     |
|          5 | SATHYAM      | ROYAPETTAH |
|          6 | MEENAKSHI    | AVADI      |
+------------+--------------+------------+

MariaDB [MOVIE]> SELECT * FROM MOVIES;
+----------+--------------+----------+--------+-------------+-----------------------------------+----------+
| MOVIE_ID | MOVIE_NAME   | GENRE    | RATING | DESCRIPTION | URL                               | RUN_TIME |
+----------+--------------+----------+--------+-------------+-----------------------------------+----------+
|        1 | THUPPAKKI    | THRILLER | U/A    | EXCELLENT   | /static/images/THUPPAKKI.jpg      |      150 |
|        2 | GILLI        | ACTION   | U      | EXCELLENT   | /static/images/POOVE_UNAKKAGA.jpg |      180 |
|        3 | THERI        | ACTION   | U/A    | GOOD        | /static/images/THERI.jpg          |      160 |
|        4 | REMO         | ROMANTIC | U      | GOOD        | /static/images/REMO.jpg           |      140 |
|        5 | VIKRAM VEDHA | SUSPENSE | U/A    | NICE        | /static/images/VIKRAM_VEDHA.jpeg  |      170 |
|        6 | MAHAAN       | INTENSE  | U/A    | NICE        | /static/images/MAHAAN.jpg         |      180 |
+----------+--------------+----------+--------+-------------+-----------------------------------+----------+

MariaDB [MOVIE]> SELECT * FROM SCREENS;
+------------+-----------+-------------+-------------+---------------+
| THEATER_ID | SCREEN_ID | SCREEN_NAME | ELITE_SEATS | PREMIUM_SEATS |
+------------+-----------+-------------+-------------+---------------+
|          1 |         1 | SCREEN 1    |          30 |            20 |
|          1 |         2 | SCREEN 2    |          30 |            20 |
|          2 |         1 | SCREEN 1    |          30 |            20 |
|          2 |         2 | SCREEN 2    |          30 |            20 |
|          2 |         3 | SCREEN 3    |          30 |            20 |
|          3 |         1 | SCREEN 1    |          30 |            20 |
|          3 |         2 | SCREEN 2    |          30 |            20 |
|          3 |         3 | SCREEN 3    |          30 |            20 |
|          4 |         1 | SCREEN 1    |          30 |            20 |
|          4 |         2 | SCREEN 2    |          30 |            20 |
|          5 |         1 | SCREEN 1    |          30 |            20 |
|          5 |         2 | SCREEN 2    |          30 |            20 |
|          5 |         3 | SCREEN 3    |          30 |            20 |
|          6 |         1 | SCREEN 1    |          30 |            20 |
|          6 |         2 | SCREEN 2    |          30 |            20 |
+------------+-----------+-------------+-------------+---------------+

MariaDB [MOVIE]> SELECT * FROM TM;
+------------+----------+-----------+------------+-----------+
| THEATER_ID | MOVIE_ID | SCREEN_ID | SHOW_DATE  | SHOW_TIME |
+------------+----------+-----------+------------+-----------+
|          1 |        1 |         1 | 2024-04-11 | 09:00:00  |
|          1 |        1 |         2 | 2024-04-11 | 13:00:00  |
|          1 |        2 |         1 | 2024-04-11 | 13:00:00  |
|          1 |        2 |         2 | 2024-04-11 | 09:00:00  |
|          2 |        1 |         1 | 2024-04-11 | 09:00:00  |
|          2 |        1 |         2 | 2024-04-11 | 18:00:00  |
|          2 |        1 |         3 | 2024-04-11 | 13:00:00  |
|          2 |        2 |         1 | 2024-04-11 | 13:00:00  |
|          2 |        2 |         2 | 2024-04-11 | 09:00:00  |
|          2 |        2 |         3 | 2024-04-11 | 18:00:00  |
|          2 |        3 |         1 | 2024-04-11 | 18:00:00  |
|          2 |        3 |         2 | 2024-04-11 | 13:00:00  |
|          2 |        3 |         3 | 2024-04-11 | 09:00:00  |
|          3 |        3 |         1 | 2024-04-17 | 09:00:00  |
|          4 |        4 |         1 | 2024-04-17 | 09:00:00  |
|          5 |        5 |         1 | 2024-04-17 | 09:00:00  |
|          6 |        6 |         1 | 2024-04-17 | 09:00:00  |
+------------+----------+-----------+------------+-----------+

