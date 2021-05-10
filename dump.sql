INSERT INTO `person` VALUES (1 , 'Faisal Rasool'  , '1111111111111', '03207047670', 'faisal@example.com'    , NULL);
INSERT INTO `person` VALUES (2 , 'Abdul Rafey'    , '2222222222222', '03207047691', 'rafey@example.com'     , NULL);
INSERT INTO `person` VALUES (3 , 'Manager 1'      , '3333333333333', '03207047692', 'manager@example.com'   , NULL);
INSERT INTO `person` VALUES (10, 'Employee 1'     , '4444444444444', '03207047695', 'employee1@example.com' , NULL);
INSERT INTO `person` VALUES (11, 'Employee 1'     , '5555555555555', '03207047623', 'employee2@example.com' , NULL);
INSERT INTO `person` VALUES (4 , 'Laraib Arjamand', '3840188588576', '03018109402', 'laraib@example.com'    , NULL);
INSERT INTO `person` VALUES (5 , 'Bushra Arjamand', '3840188888576', '03018109420', 'bushra@example.com'    , NULL);
INSERT INTO `person` VALUES (6 , 'Haider Ali'     , '3840188588571', '03018109401', 'haider@example.com'    , NULL);
INSERT INTO `person` VALUES (7 , 'Khizer Arif'    , '3840188588570', '03018109410', 'khizer@example.com'    , NULL);
INSERT INTO `person` VALUES (8 , 'Agent 1'        , '3840188588440', '03016109410', 'agent1@example.com'    , NULL);
INSERT INTO `person` VALUES (9 , 'Agent 2'        , '3740188588440', '03016309410', 'agent2@example.com'    , NULL);



INSERT INTO `user`
    (`id`, `password`, `rank`, `person_id`)
VALUES 
    (1, 'pop', 0, 1),
    (2, 'pop', 0, 2),
    (3, 'pop', 1, 3),
    (4, NULL , 2, 10),
    (5, NULL , 2, 11)
;



INSERT INTO `buyer`
VALUES
    (1, 'Bhera'  , 4),
    (2, 'Bhera'  , 5),
    (3, 'Lahore' , 6),
    (4, 'Karachi', 7)
;



INSERT INTO `commissionagent`
VALUES
    (8),
    (9)
;




INSERT INTO plot 
    (`id`, `type`, `address`, `status`,`price`, `size`, `comments`)
VALUES 
    (1 , "residential", "first"   , "in a deal", 100000, "7", "This is Plot# 1"),
    (2 , "residential", "second"  , "in a deal", 100000, "2", "This is Plot# 2"),
    (3 , "residential", "third"   , "in a deal", 100000, "5", "This is Plot# 3"),
    (4 , "residential", "fouth"   , "in a deal", 100000, "5", "This is Plot# 4"),
    (5 , "residential", "fifth"   , "in a deal", 100000, "7", "This is Plot# 5"),
    (6 , "residential", "sixth"   , "in a deal", 100000, "5", "This is Plot# 6"),
    (7 , "residential", "seventh" , "not sold" , NULL  , "7", "This is Plot# 7"),
    (11, "commercial" , "eleven"  , "in a deal", 100000, "5", "This is Plot# 11"),
    (12, "commercial" , "twelve"  , "in a deal", 100000, "5", "This is Plot# 12"),
    (13, "commercial" , "thirteen", "in a deal", 100000, "5", "This is Plot# 13"),
    (14, "commercial" , "fourteen", "in a deal", 100000, "5", "This is Plot# 14"),
    (15, "commercial" , "fifteen" , "in a deal", 100000, "5", "This is Plot# 15"),
    (16, "commercial" , "sixteen" , "not sold" , NULL  , "5", "This is Plot# 16")
;

INSERT INTO `expenditure`
VALUES
    (1, 'Salary'),
    (2, 'Commission'),
    (3, 'Office Expenses'),
    (4, 'Miscellaneous')
;


INSERT INTO `deal`
VALUES
    (1, 'on going', '10/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 1, 1 ),
    (2, 'on going', '15/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 1, 2 ),
    (3, 'on going', '20/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 1, 11),
    (4, 'on going', '25/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 2, 3 ),
    (5, 'on going', '30/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 2, 4 ),
    (6, 'on going', '10/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 2, 12),
    (7, 'on going', '15/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 3, 5 ),
    (8, 'on going', '20/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 3, 6 ),
    (9, 'on going', '25/03/2021 23:40:17',  2000, 4, NULL, NULL, NULL, 4, 15),
    (10, 'on going', '30/03/2021 23:40:17', 2000, 4, NULL, NULL, NULL, 4, 13),
    (11, 'on going', '10/03/2021 23:40:17', 2000, 4, NULL, NULL, NULL, 4, 14)
;
   



