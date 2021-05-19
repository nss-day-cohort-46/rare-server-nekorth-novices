UPDATE rareapi_post
SET approved = 1
WHERE id = 1;

DELETE FROM rareapi_reaction WHERE id = 3
update auth_user
set is_active = 0
where id = 1
