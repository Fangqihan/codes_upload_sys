# 当前用户id=1

# 取出当前用户角色
select role from user_profile_role u_r where u_r.user =2

# 取出当前用户角色的所有权限

select permission_id from role_permission where role_id in (select role from user_profile_role u_r where u_r.user =2);

# 根据权限id确定对应的url列表
select url from permmision where id in (select permission_id from role_permission where role_id in (select role from user_profile_role u_r where u_r.user =2));



-- create table role (
--   id int primary key auto_increment,
--   title char(32) not null ,
--   menu_id int not null ,
--   foreign key(menu_id) references role(id)
--   on delete cascade
--   on update cascade
--   )

