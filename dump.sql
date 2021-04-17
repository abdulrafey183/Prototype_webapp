
INSERT INTO user 
VALUES 
    (1, "faisal@example.com", "Faisal Rasool", "pop", 0),
    (2, "rafey@example.com" , "Abdul Rafey"  , "pop", 0),
    (3, "munshi@example.com", "Manager 1"    , "pop", 1)
;

-- INSERT INTO buyer 
-- VALUES 
--     (1, "Hadi Ali"  , 12345,  null),
--     (2, "Haider Ali", 12346,  null)
-- ;


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

INSERT INTO plot 
    (`id`, `type`, `address`, `status`, `size`)
VALUES 
    (1 , "residential", "first"   , "not sold", "7"),
    (2 , "residential", "second"  , "not sold", "2"),
    (3 , "residential", "third"   , "not sold", "5"),
    (4 , "residential", "fouth"   , "not sold", "5"),
    (5 , "residential", "fifth"   , "not sold", "7"),
    (6 , "residential", "sixth"   , "not sold", "5"),
    (7 , "residential", "seventh" , "not sold", "7"),
    (11, "commercial" , "eleven"  , "not sold", "5"),
    (12, "commercial" , "twelve"  , "not sold", "5"),
    (13, "commercial" , "thirteen", "not sold", "5"),
    (14, "commercial" , "fourteen", "not sold", "5"),
    (15, "commercial" , "fifteen" , "not sold", "5"),
    (16, "commercial" , "sixteen" , "not sold", "5")
;



