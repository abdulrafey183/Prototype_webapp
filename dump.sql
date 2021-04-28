
INSERT INTO user 
VALUES 
    (1, "faisal@example.com", "Faisal Rasool", "pop", 0),
    (2, "rafey@example.com" , "Abdul Rafey"  , "pop", 0),
    (3, "munshi@example.com", "Manager 1"    , "pop", 1)
;

INSERT INTO `buyer`
VALUES
    (1, 'Laraib Arjamand', '3840188588576', '03018109400', 'laraib@example.com', 'Bhera','path1', 
    'path2', null),
    (2, 'Bushra Arjamand', '3840188588572', '03004264935', 'bushra@example.com', 'Bhera','path1', 
    'path2', null),
    (3, 'Hooria Arjamand', '3840188588579', '03015702001', 'hooria@example.com', 'Bhera','path1', 
    'path2', null),
    (4, 'Asma Arjamand', '3840188588571', '03018109401', 'asma@example.com', 'Bhera','path1', 
    'path2', null)
;

INSERT INTO `commissionagent`
    (`id`, `name`, `cnic`, `phone`, `email`, `cnic_front`, `cnic_back`, `comments`)
VALUES 
    (1, 'Abdul Rafey', '1234567890123', '03207047670', 'arafey@example.com', 'img/1234567890123.jpg', 'img/1234567890123.jpg', null),
    (2, 'Abdul Ahad', '1234567890122',  '03207047671', 'ahad@example.com',   'img/1234567890122.jpg', 'img/1234567890122.jpg', null);


INSERT INTO plot 
    (`id`, `type`, `address`, `status`,`price`, `size`)
VALUES 
    (1 , "residential", "first"   , "in a deal", 100000, "7"),
    (2 , "residential", "second"  , "in a deal", 100000, "2"),
    (3 , "residential", "third"   , "in a deal", 100000, "5"),
    (4 , "residential", "fouth"   , "in a deal", 100000, "5"),
    (5 , "residential", "fifth"   , "in a deal", 100000, "7"),
    (6 , "residential", "sixth"   , "in a deal", 100000, "5"),
    (7 , "residential", "seventh" , "not sold" , NULL  , "7"),
    (11, "commercial" , "eleven"  , "in a deal", 100000, "5"),
    (12, "commercial" , "twelve"  , "in a deal", 100000, "5"),
    (13, "commercial" , "thirteen", "in a deal", 100000, "5"),
    (14, "commercial" , "fourteen", "in a deal", 100000, "5"),
    (15, "commercial" , "fifteen" , "in a deal", 100000, "5"),
    (16, "commercial" , "sixteen" , "not sold" , NULL  , "5")
;


INSERT INTO `deal`
VALUES
    (1, 'on going', '10/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 1, 1),
    (2, 'on going', '15/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 1, 2),
    (3, 'on going', '20/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 1, 11),
    (4, 'on going', '25/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 2, 3),
    (5, 'on going', '30/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 2, 4),
    (6, 'on going', '10/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 2, 12),
    (7, 'on going', '15/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 3, 5),
    (8, 'on going', '20/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 3, 6),
    (9, 'on going', '25/03/2021 23:40:17',  NULL, NULL, NULL, NULL, NULL, 4, 15),
    (10, 'on going', '30/03/2021 23:40:17', NULL, NULL, NULL, NULL, NULL, 4, 13),
    (11, 'on going', '10/03/2021 23:40:17', NULL, NULL, NULL, NULL, NULL, 4, 14)
;
   



