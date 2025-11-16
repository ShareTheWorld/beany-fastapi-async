------------------------------------user表-----------------------------------

create table "user"
(
    id        varchar(36)  default ''::character varying not null,
    name      varchar(32)  default ''::character varying not null,
    email     varchar(32)  default ''::character varying not null,
    phone     varchar(12)  default ''::character varying not null,
    avatar    varchar(255) default ''::character varying not null,
    create_at timestamp    default now() not null,
    update_at timestamp    default now() not null
);

comment
on table "user" is '用户表';

comment
on column "user".id is 'id';

comment
on column "user".name is '昵称';

comment
on column "user".email is '邮箱';

comment
on column "user".phone is '手机号';

comment
on column "user".avatar is '头像';

comment
on column "user".create_at is '创建时间';

comment
on column "user".update_at is '更新时间';

alter table "user"
    owner to postgres;



create table captcha
(
    id        bigserial
        primary key,
    account   varchar(64)  default ''::character varying not null,
    channel   varchar(10)  default ''::character varying not null,
    scene     varchar(20)  default ''::character varying not null,
    code      varchar(10)  default ''::character varying not null,
    expire_at timestamp                  not null,
    used      boolean      default false not null,
    used_at   timestamp,
    status    varchar(16)  default ''::character varying not null,
    remark    varchar(255) default ''::character varying not null,
    create_at timestamp    default now() not null,
    update_at timestamp    default now() not null
);

alter table captcha
    owner to postgres;


------------------------------------captcha表-----------------------------------

-- auto-generated definition
create table captcha
(
    id        bigserial
        primary key,
    account   varchar(64)  default ''::character varying not null,
    channel   varchar(10)  default ''::character varying not null,
    scene     varchar(20)  default ''::character varying not null,
    code      varchar(10)  default ''::character varying not null,
    expire_at timestamp                  not null,
    used      boolean      default false not null,
    used_at   timestamp,
    status    varchar(16)  default ''::character varying not null,
    remark    varchar(255) default ''::character varying not null,
    create_at timestamp    default now() not null,
    update_at timestamp    default now() not null
);

comment
on column captcha.id is 'id';

comment
on column captcha.account is '账号';

comment
on column captcha.channel is '渠道email、sms';

comment
on column captcha.scene is '场景';

comment
on column captcha.code is '验证码';

comment
on column captcha.expire_at is '过期时间';

comment
on column captcha.used is '是否使用';

comment
on column captcha.used_at is '使用时间';

comment
on column captcha.status is '发送状态';

comment
on column captcha.remark is '备注';

comment
on column captcha.create_at is '创建时间';

comment
on column captcha.update_at is '更新时间';

alter table captcha
    owner to postgres;

