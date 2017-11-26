--- people creation
INSERT INTO person (username, password, first_name, last_name) VALUES ('ml4963', 'b993bec71f1c149afa3e4c0371be0fec', 'Michelle', 'Lam'),
('al4604', '3650a2f4542be3e3909356e7156f1eb4', 'Ammy', 'Lin'),
('cy986', '8ce9e6030847d935aa41b2d0f4bf4ec0', 'Corinna', 'Yong'),
('jy1906', '07d380f2853c965800dc2a1676717dda', 'Joanne', 'Yang'),
('jh383', 'b88408e274bf3f175b86ec0edc1631bf', 'James', 'Ha');

--- friend group
INSERT INTO friendgroup (group_name, username, description) VALUES ('MAC', 'ml4963', 'A group that started from Junior Year'),
('James the Bae', 'jy1906', 'Freshman year squad');

--- adding members to friend group
INSERT INTO member (username, group_name, username_creator) VALUES ('cy986', 'MAC', 'ml4963'),
('al4604', 'MAC', 'ml4963'),
('ml4963', 'James the Bae', 'jy1906'),
('jh383', 'James the Bae', 'jy1906');

-- adding content
INSERT INTO content (id, username, timest, file_path, content_name, public) VALUES
(1, 'ml4963', CURRENT_TIMESTAMP, "http://food.fnr.sndimg.com/content/dam/images/food/fullset/2009/4/5/1/IG1C17_30946_s4x3.jpg", "My birthday", 1),
(2, 'al4604', TIMESTAMP("2017-07-23",  "13:10:11"), "http://www.oceanmist.com/artichokes/wp-content/uploads/sites/2/2016/08/image006.png", "Cooking an artichoke", 0),
(3, 'cy986', CURRENT_TIMESTAMP, "http://www.dogbreedslist.info/uploads/allimg/dog-pictures/Pomeranian-1.jpg", "I want a fluffy dog.", 0)
