-- # Datuluna Ali G. Dilangalen 2015-04685
-- # MySQL 5.7.28

INSERT INTO card_option (card_association, card_type) VALUES
	('VISA', 'Diamond'),
	('VISA', 'Platinum'),
	('VISA', 'Gold'),
	('VISA', 'Silver'),
	('Mastercard', 'Diamond'),
	('Mastercard', 'Platinum'),
	('Mastercard', 'Gold'),
	('Mastercard', 'Silver'),
	('JCB', 'Diamond'),
	('JCB', 'Platinum'),
	('JCB', 'Gold'),
	('JCB', 'Silver'),
	('American Express', 'Diamond'),
	('American Express', 'Platinum'),
	('American Express', 'Gold'),
	('American Express', 'Silver');

INSERT INTO application (card_option_id, person_id, card_number) VALUES
	(1, 1, 11112222333344445555),
	(1, 2, 99990000777788881111),
	(1, 3, 12345678901234567890);

INSERT INTO person VALUES
	(1, 'Mary Jane', 'Undergraduate', '1999-04-20', 'United States', 'Female', '09662391022', 'maryj@example.com', '9th floor #038; 10th floor Pearl Bank Center 146 Valero St, Salcedo', 'Full-time', 'Business Analyst', 2, 2000000.00),
	(2, 'Bogart Dominic', 'Undergraduate', '1999-04-17', 'Metro Manila', 'Male', '09692391029', 'bogartd@example.com', 'Pacific Building, 1325 Filmore Avenue', 'Full-time', 'Civil Engineer', 2, 5000000.00),
	(3, 'Rena Yuuki', 'Undergraduate', '1999-04-20', 'Japan', 'Female', '09762392022', 'renayuuki@example.com', '1584 A Mabini Street Corner Old Wack-Wack Road 1000', 'Full-time', 'Software Engineer', 2, 2000000.00);

INSERT INTO owned_card VALUES
	(11112222333344445555, '2017-08-01', 100000.00),
	(99990000777788881111, '2018-07-01', 200000.00),
	(12345678901234567890, '2018-09-01', 100000.00);
