INSERT INTO `person` VALUES (1 , 'Faisal Rasool'  , '1111111111111', '03207047670', 'faisal@example.com'    , NULL);
INSERT INTO `person` VALUES (2 , 'Abdul Rafey'    , '2222222222222', '03207047691', 'rafey@example.com'     , NULL);
INSERT INTO `person` VALUES (3 , 'Manager 1'      , '3333333333333', '03207047692', 'manager@example.com'   , NULL);
INSERT INTO `person` VALUES (10, 'Employee 1'     , '4444444444444', '03207047695', NULL                    , NULL);
INSERT INTO `person` VALUES (11, 'Employee 2'     , '5555555555555', '03207047623', NULL                    , NULL);
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
    (1 , 'completed', '10/03/2021 23:40:17', 20000, 30, 0.15, NULL, 8   , 1, 1 ),
    (2 , 'completed', '15/03/2021 23:40:17', 20000, 30, NULL, NULL, NULL, 1, 2 ),
    (3 , 'completed', '20/03/2021 23:40:17', 20000, 30, NULL, NULL, NULL, 1, 11),
    (4 , 'completed', '25/03/2021 23:40:17', 20000, 30, 0.4 , NULL, 8   , 2, 3 ),
    (5 , 'completed', '30/03/2021 23:40:17', 20000, 30, NULL, NULL, NULL, 2, 4 ),
    (6 , 'completed', '10/03/2021 23:40:17', 20000, 30, NULL, NULL, NULL, 2, 12),
    (7 , 'on going' , '15/03/2021 23:40:17', 20000, 30, 0.3 , NULL, 8   , 3, 5 ),
    (8 , 'on going' , '20/03/2021 23:40:17', 20000, 30, NULL, NULL, NULL, 3, 6 ),
    (9 , 'on going' , '25/03/2021 23:40:17', 20000, 30, 0.4 , NULL, 9   , 4, 15),
    (10, 'on going' , '30/03/2021 23:40:17', 20000, 30, NULL, NULL, NULL, 4, 13),
    (11, 'on going' , '10/03/2021 23:40:17', 20000, 30, 0.2 , NULL, 9   , 4, 14)
;


INSERT INTO `transaction` VALUES (1 , 9000 , CURRENT_DATE - INTERVAL 12 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in May 2020"       , NULL, 1);
INSERT INTO `transaction` VALUES (2 , 100  , CURRENT_DATE - INTERVAL 12 MONTH - INTERVAL 2 DAY, "Commission of Deal 1, Expense in May 2020"      , NULL, 2);
INSERT INTO `transaction` VALUES (3 , 2000 , CURRENT_DATE - INTERVAL 12 MONTH + INTERVAL 2 DAY, "Office Expense in May 2020"                     , NULL, 3);
INSERT INTO `transaction` VALUES (4 , 3000 , CURRENT_DATE - INTERVAL 12 MONTH + INTERVAL 4 DAY, "Miscellaneous Expense in May 2020"              , NULL, 4);
INSERT INTO `transaction` VALUES (5 , 9000 , CURRENT_DATE - INTERVAL 11 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in June 2020"      , NULL, 1);
INSERT INTO `transaction` VALUES (6 , 200  , CURRENT_DATE - INTERVAL 11 MONTH - INTERVAL 2 DAY, "Commission of Deal 1, Expense in June 2020"     , NULL, 2);
INSERT INTO `transaction` VALUES (7 , 5000 , CURRENT_DATE - INTERVAL 11 MONTH - INTERVAL 2 DAY, "Office Expense in June 2020"                    , NULL, 3);
INSERT INTO `transaction` VALUES (8 , 6000 , CURRENT_DATE - INTERVAL 11 MONTH + INTERVAL 5 DAY, "Miscellaneous Expense in June 2020"             , NULL, 4);
INSERT INTO `transaction` VALUES (9 , 9000 , CURRENT_DATE - INTERVAL 10 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in July 2020"      , NULL, 1);
INSERT INTO `transaction` VALUES (10, 100  , CURRENT_DATE - INTERVAL 10 MONTH - INTERVAL 2 DAY, "Commission of Deal 1, Expense in July 2020"     , NULL, 2);
INSERT INTO `transaction` VALUES (11, 2000 , CURRENT_DATE - INTERVAL 10 MONTH + INTERVAL 2 DAY, "Office Expense in July 2020"                    , NULL, 3);
INSERT INTO `transaction` VALUES (12, 1000 , CURRENT_DATE - INTERVAL 10 MONTH - INTERVAL 3 DAY, "Miscellaneous Expense in July 2020"             , NULL, 4);
INSERT INTO `transaction` VALUES (13, 9000 , CURRENT_DATE - INTERVAL 09 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in August 2020"    , NULL, 1);
INSERT INTO `transaction` VALUES (14, 200  , CURRENT_DATE - INTERVAL 09 MONTH - INTERVAL 6 DAY, "Commission of Deal 4, Expense in August 2020"   , NULL, 2);
INSERT INTO `transaction` VALUES (15, 6000 , CURRENT_DATE - INTERVAL 09 MONTH + INTERVAL 3 DAY, "Office Expense in August 2020"                  , NULL, 3);
INSERT INTO `transaction` VALUES (16, 9000 , CURRENT_DATE - INTERVAL 09 MONTH + INTERVAL 2 DAY, "Miscellaneous Expense in August 2020"           , NULL, 4);
INSERT INTO `transaction` VALUES (17, 9000 , CURRENT_DATE - INTERVAL 08 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in September 2020" , NULL, 1);
INSERT INTO `transaction` VALUES (18, 300  , CURRENT_DATE - INTERVAL 08 MONTH - INTERVAL 6 DAY, "Commission of Deal 4, Expense in September 2020", NULL, 2);
INSERT INTO `transaction` VALUES (19, 11000, CURRENT_DATE - INTERVAL 08 MONTH + INTERVAL 0 DAY, "Office Expense in September 2020"               , NULL, 3);
INSERT INTO `transaction` VALUES (20, 8000 , CURRENT_DATE - INTERVAL 08 MONTH + INTERVAL 2 DAY, "Miscellaneous Expense in September 2020"        , NULL, 4);
INSERT INTO `transaction` VALUES (21, 9000 , CURRENT_DATE - INTERVAL 07 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in October 2020"   , NULL, 1);
INSERT INTO `transaction` VALUES (22, 500  , CURRENT_DATE - INTERVAL 07 MONTH - INTERVAL 6 DAY, "Commission of Deal 4, Expense in October 2020"  , NULL, 2);
INSERT INTO `transaction` VALUES (23, 4000 , CURRENT_DATE - INTERVAL 07 MONTH + INTERVAL 3 DAY, "Office Expense in October 2020"                 , NULL, 3);
INSERT INTO `transaction` VALUES (24, 6500 , CURRENT_DATE - INTERVAL 07 MONTH + INTERVAL 2 DAY, "Miscellaneous Expense in October 2020"          , NULL, 4);
INSERT INTO `transaction` VALUES (25, 9000 , CURRENT_DATE - INTERVAL 06 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in November 2020"  , NULL, 1);
INSERT INTO `transaction` VALUES (26, 200  , CURRENT_DATE - INTERVAL 06 MONTH - INTERVAL 3 DAY, "Commission of Deal 7, Expense in November 2020" , NULL, 2);
INSERT INTO `transaction` VALUES (27, 9900 , CURRENT_DATE - INTERVAL 06 MONTH + INTERVAL 2 DAY, "Office Expense in November 2020"                , NULL, 3);
INSERT INTO `transaction` VALUES (28, 5600 , CURRENT_DATE - INTERVAL 06 MONTH + INTERVAL 2 DAY, "Miscellaneous Expense in November 2020"         , NULL, 4);
INSERT INTO `transaction` VALUES (29, 9000 , CURRENT_DATE - INTERVAL 05 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in December 2020"  , NULL, 1);
INSERT INTO `transaction` VALUES (30, 400  , CURRENT_DATE - INTERVAL 05 MONTH - INTERVAL 3 DAY, "Commission of Deal 7, Expense in December 2020" , NULL, 2);
INSERT INTO `transaction` VALUES (31, 2000 , CURRENT_DATE - INTERVAL 05 MONTH + INTERVAL 2 DAY, "Office Expense in December 2020"                , NULL, 3);
INSERT INTO `transaction` VALUES (32, 3000 , CURRENT_DATE - INTERVAL 05 MONTH + INTERVAL 6 DAY, "Miscellaneous Expense in December 2020"         , NULL, 4);
INSERT INTO `transaction` VALUES (33, 9000 , CURRENT_DATE - INTERVAL 04 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in January 2021"   , NULL, 1);
INSERT INTO `transaction` VALUES (34, 100  , CURRENT_DATE - INTERVAL 04 MONTH - INTERVAL 3 DAY, "Commission of Deal 7, Expense in January 2021"  , NULL, 2);
INSERT INTO `transaction` VALUES (35, 22000, CURRENT_DATE - INTERVAL 04 MONTH + INTERVAL 2 DAY, "Office Expense in January 2021"                 , NULL, 3);
INSERT INTO `transaction` VALUES (36, 3600 , CURRENT_DATE - INTERVAL 04 MONTH + INTERVAL 4 DAY, "Miscellaneous Expense in January 2021"          , NULL, 4);
INSERT INTO `transaction` VALUES (37, 9000 , CURRENT_DATE - INTERVAL 03 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in Febuary 2021"   , NULL, 1);
INSERT INTO `transaction` VALUES (38, 400  , CURRENT_DATE - INTERVAL 03 MONTH - INTERVAL 5 DAY, "Commission of Deal 9, Expense in Febuary 2021"  , NULL, 2);
INSERT INTO `transaction` VALUES (39, 8900 , CURRENT_DATE - INTERVAL 03 MONTH + INTERVAL 7 DAY, "Office Expense in Febuary 2021"                 , NULL, 3);
INSERT INTO `transaction` VALUES (40, 4400 , CURRENT_DATE - INTERVAL 03 MONTH + INTERVAL 2 DAY, "Miscellaneous Expense in Febuary 2021"          , NULL, 4);
INSERT INTO `transaction` VALUES (41, 9000 , CURRENT_DATE - INTERVAL 02 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in March 2021"     , NULL, 1);
INSERT INTO `transaction` VALUES (42, 100  , CURRENT_DATE - INTERVAL 02 MONTH - INTERVAL 5 DAY, "Commission of Deal 9, Expense in March 2021"    , NULL, 2);
INSERT INTO `transaction` VALUES (43, 5500 , CURRENT_DATE - INTERVAL 02 MONTH + INTERVAL 2 DAY, "Office Expense in March 2021"                   , NULL, 3);
INSERT INTO `transaction` VALUES (44, 9000 , CURRENT_DATE - INTERVAL 02 MONTH + INTERVAL 4 DAY, "Miscellaneous Expense in March 2021"            , NULL, 4);
INSERT INTO `transaction` VALUES (45, 9000 , CURRENT_DATE - INTERVAL 01 MONTH + INTERVAL 1 DAY, "Salary to Manager 1, Expense in April 2021"     , NULL, 1);
INSERT INTO `transaction` VALUES (46, 250  , CURRENT_DATE - INTERVAL 01 MONTH + INTERVAL 6 DAY, "Commission of Deal 11, Expense in April 2021"   , NULL, 2);
INSERT INTO `transaction` VALUES (47, 11000, CURRENT_DATE - INTERVAL 01 MONTH + INTERVAL 2 DAY, "Office Expense in April 2021"                   , NULL, 3);
INSERT INTO `transaction` VALUES (48, 4500 , CURRENT_DATE - INTERVAL 01 MONTH + INTERVAL 3 DAY, "Miscellaneous Expense in April 2021"            , NULL, 4);
INSERT INTO `transaction` VALUES (49, 9000 , CURRENT_DATE                                     , "Salary to Manager 1, Expense in May 2021"       , NULL, 1);
INSERT INTO `transaction` VALUES (50, 250  , CURRENT_DATE                                     , "Commission of Deal 11, Expense in May 2021"     , NULL, 2);
INSERT INTO `transaction` VALUES (51, 2000 , CURRENT_DATE                                     , "Office Expense in May 2021"                     , NULL, 3);
INSERT INTO `transaction` VALUES (52, 3600 , CURRENT_DATE                                     , "Miscellaneous Expense in May 2021"              , NULL, 4);

INSERT INTO `transaction` VALUES (53, 20000 , CURRENT_DATE - INTERVAL 12 MONTH + INTERVAL 13 DAY , "Installment 1 of Deal 1, made in May 2020"       , 1   , NULL);
INSERT INTO `transaction` VALUES (54, 20000 , CURRENT_DATE - INTERVAL 11 MONTH + INTERVAL 13 DAY , "Installment 2 of Deal 1, made in June 2020"      , 1   , NULL);
INSERT INTO `transaction` VALUES (55, 20000 , CURRENT_DATE - INTERVAL 10 MONTH + INTERVAL 13 DAY , "Installment 3 of Deal 1, made in July 2020"      , 1   , NULL);
INSERT INTO `transaction` VALUES (56, 20000 , CURRENT_DATE - INTERVAL 09 MONTH + INTERVAL 13 DAY , "Installment 4 of Deal 1, made in August 2020"    , 1   , NULL);
INSERT INTO `transaction` VALUES (57, 20000 , CURRENT_DATE - INTERVAL 08 MONTH + INTERVAL 13 DAY , "Installment 5 of Deal 1, made in September 2020" , 1   , NULL);

INSERT INTO `transaction` VALUES (58, 20000 , CURRENT_DATE - INTERVAL 11 MONTH + INTERVAL 10 DAY , "Installment 1 of Deal 2, made in June 2020"      , 2   , NULL);
INSERT INTO `transaction` VALUES (59, 20000 , CURRENT_DATE - INTERVAL 10 MONTH + INTERVAL 10 DAY , "Installment 2 of Deal 2, made in July 2020"      , 2   , NULL);
INSERT INTO `transaction` VALUES (60, 20000 , CURRENT_DATE - INTERVAL 09 MONTH + INTERVAL 10 DAY , "Installment 3 of Deal 2, made in August 2020"    , 2   , NULL);
INSERT INTO `transaction` VALUES (61, 20000 , CURRENT_DATE - INTERVAL 08 MONTH + INTERVAL 10 DAY , "Installment 4 of Deal 2, made in September 2020" , 2   , NULL);
INSERT INTO `transaction` VALUES (62, 20000 , CURRENT_DATE - INTERVAL 07 MONTH + INTERVAL 10 DAY , "Installment 5 of Deal 2, made in October 2020"   , 2   , NULL);

INSERT INTO `transaction` VALUES (63, 20000 , CURRENT_DATE - INTERVAL 10 MONTH - INTERVAL 10 DAY , "Installment 1 of Deal 3, made in July 2020"      , 3   , NULL);
INSERT INTO `transaction` VALUES (64, 20000 , CURRENT_DATE - INTERVAL 09 MONTH - INTERVAL 10 DAY , "Installment 2 of Deal 3, made in August 2020"    , 3   , NULL);
INSERT INTO `transaction` VALUES (65, 20000 , CURRENT_DATE - INTERVAL 08 MONTH - INTERVAL 10 DAY , "Installment 3 of Deal 3, made in September 2020" , 3   , NULL);
INSERT INTO `transaction` VALUES (66, 20000 , CURRENT_DATE - INTERVAL 07 MONTH - INTERVAL 10 DAY , "Installment 4 of Deal 3, made in October 2020"   , 3   , NULL);
INSERT INTO `transaction` VALUES (67, 20000 , CURRENT_DATE - INTERVAL 06 MONTH - INTERVAL 10 DAY , "Installment 5 of Deal 3, made in November 2020"  , 3   , NULL);

INSERT INTO `transaction` VALUES (68, 20000 , CURRENT_DATE - INTERVAL 09 MONTH - INTERVAL 13 DAY , "Installment 1 of Deal 4, made in August 2020"    , 4   , NULL);
INSERT INTO `transaction` VALUES (69, 20000 , CURRENT_DATE - INTERVAL 08 MONTH - INTERVAL 13 DAY , "Installment 2 of Deal 4, made in September 2020" , 4   , NULL);
INSERT INTO `transaction` VALUES (70, 20000 , CURRENT_DATE - INTERVAL 07 MONTH - INTERVAL 13 DAY , "Installment 3 of Deal 4, made in October 2020"   , 4   , NULL);
INSERT INTO `transaction` VALUES (71, 20000 , CURRENT_DATE - INTERVAL 06 MONTH - INTERVAL 13 DAY , "Installment 4 of Deal 4, made in November 2020"  , 4   , NULL);
INSERT INTO `transaction` VALUES (72, 20000 , CURRENT_DATE - INTERVAL 05 MONTH - INTERVAL 13 DAY , "Installment 5 of Deal 4, made in December 2020"  , 4   , NULL);

INSERT INTO `transaction` VALUES (73, 20000 , CURRENT_DATE - INTERVAL 08 MONTH - INTERVAL 07 DAY , "Installment 1 of Deal 5, made in September 2020" , 5   , NULL);
INSERT INTO `transaction` VALUES (74, 20000 , CURRENT_DATE - INTERVAL 07 MONTH - INTERVAL 07 DAY , "Installment 2 of Deal 5, made in October 2020"   , 5   , NULL);
INSERT INTO `transaction` VALUES (75, 20000 , CURRENT_DATE - INTERVAL 06 MONTH - INTERVAL 07 DAY , "Installment 3 of Deal 5, made in November 2020"  , 5   , NULL);
INSERT INTO `transaction` VALUES (76, 20000 , CURRENT_DATE - INTERVAL 05 MONTH - INTERVAL 07 DAY , "Installment 4 of Deal 5, made in December 2020"  , 5   , NULL);
INSERT INTO `transaction` VALUES (77, 20000 , CURRENT_DATE - INTERVAL 04 MONTH - INTERVAL 07 DAY , "Installment 5 of Deal 5, made in January 2021"   , 5   , NULL);

INSERT INTO `transaction` VALUES (78, 20000 , CURRENT_DATE - INTERVAL 07 MONTH - INTERVAL 17 DAY , "Installment 1 of Deal 6, made in October 2020"   , 6   , NULL);
INSERT INTO `transaction` VALUES (79, 20000 , CURRENT_DATE - INTERVAL 06 MONTH - INTERVAL 17 DAY , "Installment 2 of Deal 6, made in November 2020"  , 6   , NULL);
INSERT INTO `transaction` VALUES (80, 20000 , CURRENT_DATE - INTERVAL 05 MONTH - INTERVAL 17 DAY , "Installment 3 of Deal 6, made in December 2020"  , 6   , NULL);
INSERT INTO `transaction` VALUES (81, 20000 , CURRENT_DATE - INTERVAL 04 MONTH - INTERVAL 17 DAY , "Installment 4 of Deal 6, made in January 2021"   , 6   , NULL);
INSERT INTO `transaction` VALUES (82, 20000 , CURRENT_DATE - INTERVAL 03 MONTH - INTERVAL 17 DAY , "Installment 5 of Deal 6, made in Febuary 2021"   , 6   , NULL);

INSERT INTO `transaction` VALUES (83, 20000 , CURRENT_DATE - INTERVAL 05 MONTH + INTERVAL 02 DAY , "Installment 1 of Deal 7, made in December 2020"  , 7   , NULL);
INSERT INTO `transaction` VALUES (84, 20000 , CURRENT_DATE - INTERVAL 04 MONTH + INTERVAL 02 DAY , "Installment 2 of Deal 7, made in January 2021"   , 7   , NULL);
INSERT INTO `transaction` VALUES (85, 20000 , CURRENT_DATE - INTERVAL 03 MONTH + INTERVAL 02 DAY , "Installment 3 of Deal 7, made in Febuary 2021"   , 7   , NULL);

INSERT INTO `transaction` VALUES (86, 20000 , CURRENT_DATE - INTERVAL 04 MONTH - INTERVAL 05 DAY , "Installment 1 of Deal 8, made in January 2021"   , 8   , NULL);
INSERT INTO `transaction` VALUES (87, 20000 , CURRENT_DATE - INTERVAL 03 MONTH - INTERVAL 05 DAY , "Installment 2 of Deal 8, made in Febuary 2021"   , 8   , NULL);
INSERT INTO `transaction` VALUES (88, 20000 , CURRENT_DATE - INTERVAL 02 MONTH - INTERVAL 05 DAY , "Installment 3 of Deal 8, made in March 2021"     , 8   , NULL);

INSERT INTO `transaction` VALUES (89, 20000 , CURRENT_DATE - INTERVAL 03 MONTH - INTERVAL 17 DAY , "Installment 1 of Deal 9, made in Febuary 2020"  , 9   , NULL);
INSERT INTO `transaction` VALUES (90, 20000 , CURRENT_DATE - INTERVAL 02 MONTH - INTERVAL 17 DAY , "Installment 2 of Deal 9, made in March 2021"    , 9   , NULL);
INSERT INTO `transaction` VALUES (91, 20000 , CURRENT_DATE - INTERVAL 01 MONTH - INTERVAL 17 DAY , "Installment 3 of Deal 9, made in April 2021"    , 9   , NULL);

INSERT INTO `transaction` VALUES (92, 20000 , CURRENT_DATE - INTERVAL 02 MONTH - INTERVAL 10 DAY , "Installment 1 of Deal 10, made in March 2020"   , 10   , NULL);
INSERT INTO `transaction` VALUES (93, 20000 , CURRENT_DATE - INTERVAL 01 MONTH - INTERVAL 10 DAY , "Installment 2 of Deal 10, made in April 2021"   , 10   , NULL);
INSERT INTO `transaction` VALUES (94, 20000 , CURRENT_DATE - INTERVAL 10 DAY                     , "Installment 3 of Deal 10, made in May 2021"     , 10   , NULL);

INSERT INTO `transaction` VALUES (95, 20000 , CURRENT_DATE - INTERVAL 02 MONTH - INTERVAL 08 DAY , "Installment 1 of Deal 11, made in March 2020"   , 11   , NULL);
INSERT INTO `transaction` VALUES (96, 20000 , CURRENT_DATE - INTERVAL 01 MONTH - INTERVAL 08 DAY , "Installment 2 of Deal 11, made in April 2021"   , 11   , NULL);
INSERT INTO `transaction` VALUES (97, 20000 , CURRENT_DATE - INTERVAL 10 DAY                     , "Installment 3 of Deal 11, made in May 2021"     , 11   , NULL);

INSERT INTO `salary` VALUES (1 , 3, 1);
INSERT INTO `salary` VALUES (2 , 3, 5);
INSERT INTO `salary` VALUES (3 , 3, 9);
INSERT INTO `salary` VALUES (4 , 3, 13);
INSERT INTO `salary` VALUES (5 , 3, 17);
INSERT INTO `salary` VALUES (6 , 3, 21);
INSERT INTO `salary` VALUES (7 , 3, 25);
INSERT INTO `salary` VALUES (8 , 3, 29);
INSERT INTO `salary` VALUES (9 , 3, 33);
INSERT INTO `salary` VALUES (10, 3, 37);
INSERT INTO `salary` VALUES (11, 3, 41);
INSERT INTO `salary` VALUES (12, 3, 45);
INSERT INTO `salary` VALUES (13, 3, 49);



INSERT INTO `commission` 
VALUES
    (1 , 1 , 8, 2),
    (2 , 1 , 8, 6),
    (3 , 1 , 8, 10),
    (4 , 4 , 8, 14),
    (5 , 4 , 8, 18),
    (6 , 4 , 8, 22),
    (7 , 7 , 8, 26),
    (8 , 7 , 8, 30),
    (9 , 7 , 8, 34),
    (10, 9 , 9, 38),
    (11, 9 , 9, 42),
    (12, 11, 9, 46),
    (13, 11, 9, 50)
;