-- ---------- 초기화 ----------

DROP TABLE IF EXISTS sql_query_log;
DROP TABLE IF EXISTS user_activity;
DROP TABLE IF EXISTS spams;
DROP TABLE IF EXISTS users;

-- ---------- 본 테이블 ----------

CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE NOT NULL,
    age   INT NOT NULL
);

CREATE TABLE spams (
    id         SERIAL PRIMARY KEY,
    email      VARCHAR(100) NOT NULL REFERENCES users(email),
    spam_count INT NOT NULL DEFAULT 0
);

CREATE TABLE user_activity (
    id                       SERIAL PRIMARY KEY,
    user_name                VARCHAR(100) NOT NULL REFERENCES users(name),
    internet_usage_gb        DECIMAL(10, 2) NOT NULL,
    spam_filter_subscription BOOLEAN NOT NULL DEFAULT FALSE
);

-- ---------- 로그 테이블 ----------

CREATE TABLE sql_query_log (
    id            SERIAL PRIMARY KEY,
    sql_query     TEXT      NOT NULL,
    success       BOOLEAN   NOT NULL,
    error_message TEXT,
    rows_returned INT,
    logged_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------- 초기 데이터 ----------

INSERT INTO users (name, email, age) VALUES
('김지민','jimin.kim@example.com',28),
('이승우','seungwoo.lee@example.com',35),
('박소연','soyeon.park@example.com',24),
('정민준','minjun.jung@example.com',42),
('최예린','yerin.choi@example.com',31),
('강현우','hyunwoo.kang@example.com',29),
('윤서연','seoyeon.yoon@example.com',26),
('임준호','junho.lim@example.com',38),
('한지영','jiyoung.han@example.com',33),
('송태민','taemin.song@example.com',27),
('권나영','nayoung.kwon@example.com',30),
('오동현','donghyun.oh@example.com',45),
('백서진','seojin.baek@example.com',22),
('황민석','minseok.hwang@example.com',39),
('조은지','eunji.jo@example.com',32),
('노현주','hyunju.noh@example.com',36),
('유지훈','jihoon.yoo@example.com',41),
('신미래','mirae.shin@example.com',25),
('장도윤','doyoon.jang@example.com',37),
('문서현','seohyun.moon@example.com',29);

INSERT INTO spams (email, spam_count) VALUES
('jimin.kim@example.com',12),
('seungwoo.lee@example.com',5),
('soyeon.park@example.com',24),
('minjun.jung@example.com',3),
('yerin.choi@example.com',18),
('hyunwoo.kang@example.com',7),
('seoyeon.yoon@example.com',31),
('junho.lim@example.com',9),
('jiyoung.han@example.com',0),
('taemin.song@example.com',42),
('nayoung.kwon@example.com',15),
('donghyun.oh@example.com',6),
('seojin.baek@example.com',27),
('minseok.hwang@example.com',4),
('eunji.jo@example.com',19),
('hyunju.noh@example.com',8),
('jihoon.yoo@example.com',11),
('mirae.shin@example.com',36),
('doyoon.jang@example.com',2),
('seohyun.moon@example.com',14);

INSERT INTO user_activity (user_name, internet_usage_gb, spam_filter_subscription) VALUES
('김지민',125.5,TRUE),
('이승우',87.2,FALSE),
('박소연',210.8,TRUE),
('정민준',45.3,FALSE),
('최예린',156.7,TRUE),
('강현우',92.4,FALSE),
('윤서연',178.9,TRUE),
('임준호',63.1,FALSE),
('한지영',105.6,TRUE),
('송태민',235.2,TRUE),
('권나영',73.8,FALSE),
('오동현',142.5,TRUE),
('백서진',189.3,TRUE),
('황민석',56.7,FALSE),
('조은지',112.4,TRUE),
('노현주',84.9,FALSE),
('유지훈',165.3,TRUE),
('신미래',197.6,TRUE),
('장도윤',38.2,FALSE),
('문서현',129.7,TRUE);
