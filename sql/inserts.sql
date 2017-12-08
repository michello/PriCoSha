--- people creation
INSERT INTO person (username, password, first_name, last_name) VALUES ('ml4963', 'b993bec71f1c149afa3e4c0371be0fec', 'Michelle', 'Lam'),
('al4604', '3650a2f4542be3e3909356e7156f1eb4', 'Ammy', 'Lin'),
('cy986', '8ce9e6030847d935aa41b2d0f4bf4ec0', 'Corinna', 'Yong'),
('jy1906', '07d380f2853c965800dc2a1676717dda', 'Joanne', 'Yang'),
('jh383', 'b88408e274bf3f175b86ec0edc1631bf', 'James', 'Ha');

--- profile page
INSERT INTO profile (username, bio, file_path) VALUES 
('ml4963', '', ''),
('cy986','Hi I like sushi', '/static/posts_pic/image_1.jpg')


--- friend group
INSERT INTO friendgroup (group_name, username, description) VALUES ('MAC', 'ml4963', 'A group that started from Junior Year'),
('James the Bae', 'jy1906', 'Freshman year squad');

--- adding members to friend group
INSERT INTO member (username, group_name, username_creator) VALUES ('cy986', 'MAC', 'ml4963'),
('al4604', 'MAC', 'ml4963'),
('ml4963', 'James the Bae', 'jy1906'),
('jh383', 'James the Bae', 'jy1906');

--- adding content
INSERT INTO content (id, username, timest, file_path, content_name, public) VALUES
(1, 'ml4963', CURRENT_TIMESTAMP, "/static/posts_pic/image_1.jpg", "My birthday", 1),
(2, 'al4604', TIMESTAMP("2017-07-23",  "13:10:11"), "/static/posts_pic/image_2.png", "Cooking an artichoke", 0),
(3, 'cy986', CURRENT_TIMESTAMP, "/static/posts_pic/image_3.jpg", "I want a fluffy dog.", 0),
(4, 'jy1906', TIMESTAMP("2017-09-15",  "13:10:11"), "/static/posts_pic/image_4.jpg", "My first magikarp!", 0),
(5, 'jh383', TIMESTAMP("2016-12-25",  "13:10:11"), "/static/posts_pic/image_5.jpg", "I love pusheens~", 1);

--- tag
INSERT INTO tag (id, username_tagger, username_taggee, timest, status) VALUES
(1, 'ml4963', 'al4604', CURRENT_TIMESTAMP, 0),
(1, 'ml4963', 'cy986', CURRENT_TIMESTAMP, 0),
(4, 'jy1906', 'ml4963', TIMESTAMP("2017-09-16",  "13:10:11"), 0),
(3, 'cy986', 'ml4963', TIMESTAMP("2017-09-16",  "13:10:11"), 0),
(3, 'cy986', 'al4604', TIMESTAMP("2017-09-16",  "13:10:11"), 0);

--- adding comments
INSERT INTO comment (	id,	username,	timest, comment_text) VALUES
(2, 'ml4963', TIMESTAMP("2017-07-23",  "14:10:11"), "Artichokes are great! 8D");

--- adding to share
INSERT INTO share (	id, group_name, username) VALUES
(1, 'James the Bae', 'ml4963'),
(2, 'MAC', 'al4604'),
(3, 'MAC', 'cy986')


