create database if not exists ai_code_reviewer;

use ai_code_reviewer;


-- =========================
-- Users Table
-- =========================

create table if not exists users(

    id int auto_increment primary key,

    fullname varchar(100) not null,

    username varchar(50) unique not null,

    email varchar(100) unique not null,

    password varchar(255) not null,

    role varchar(20) default 'user',

    last_login datetime null,

    created_at timestamp default current_timestamp,

    updated_at timestamp default current_timestamp
    on update current_timestamp,

    is_active boolean default true

);



-- =========================
-- Code Reviews Table
-- =========================

create table if not exists code_reviews(

    id int auto_increment primary key,

    user_id int not null,

    filename varchar(255),

    language varchar(50),

    code_text longtext,

    ai_feedback longtext,

    score int default 0,

    created_at timestamp default current_timestamp,


    foreign key(user_id)
    references users(id)
    on delete cascade

);



-- =========================
-- Reports Table
-- =========================

create table if not exists reports(

    id int auto_increment primary key,

    review_id int not null,

    report_file varchar(255),

    report_type varchar(50),

    created_at timestamp default current_timestamp,


    foreign key(review_id)
    references code_reviews(id)
    on delete cascade

);



-- =========================
-- Activity Logs
-- =========================

create table if not exists activity_logs(

    id int auto_increment primary key,

    user_id int,

    activity varchar(255),

    created_at timestamp default current_timestamp,


    foreign key(user_id)
    references users(id)
    on delete cascade

);