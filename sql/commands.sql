SELECT content.id, content.username, content.timest, content.file_path, content.content_name
FROM CONTENT
WHERE content.public = 1 OR username = 'jy1906'
      OR username in (SELECT username FROM member
                      WHERE group_name in (SELECT group_name FROM member WHERE member.username = 'jy1906'))
      OR username in (SELECT username_creator FROM member WHERE username = 'jy1906')
      OR username in (SELECT username FROM member WHERE username_creator='jy1906')
ORDER BY timest DESC
