CREATE TABLE IF NOT EXISTS pop(
   idPOP INT PRIMARY KEY,
   popPosition VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS cabinet(
	idCabinet VARCHAR(5) PRIMARY KEY,
	numOfSlot INT NOT NULL,
	idPOP INT,
	FOREIGN KEY (idPOP) REFERENCES pop (idPOP)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS employee(
	idEmployee INT PRIMARY KEY,
	name VARCHAR(20) NOT NULL,
	surname VARCHAR(20) NOT NULL,
	birthDate DATE NOT NULL,
	email VARCHAR(20) NOT NULL UNIQUE
);



CREATE TABLE IF NOT EXISTS deviceType(
	idDeviceType SERIAL PRIMARY KEY,
	deviceType VARCHAR(15) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS action(
	idAction SERIAL PRIMARY KEY,
	actionType VARCHAR(10) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS device(

	idDevice SERIAL PRIMARY KEY,
	serialNumber VARCHAR(30) NOT NULL,
	sizeDevice INT NOT NULL,
	producerDevice VARCHAR(20) NOT NULL,
	yearProduction DATE NOT NULL,
	statusDevice VARCHAR(10) NOT NULL,
	usedSlot VARCHAR(15),
	idDeviceType INT,
	idEmployee INT, 
	idCabinet VARCHAR(5),
	FOREIGN KEY(idDeviceType) REFERENCES deviceType(idDeviceType)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY(idEmployee) REFERENCES employee(idEmployee)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY(idCabinet) REFERENCES cabinet(idCabinet)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);



CREATE TABLE IF NOT EXISTS log(
	idLog SERIAL PRIMARY KEY,
    dateLog DATE NOT NULL,
    timeLog TIMESTAMP NOT NULL,
    slotOccupati INT NOT NULL,
    idDevice INT,
    idEmployee INT,
    idCabinet VARCHAR(5),
    idAction INT,
	idDeviceReplaced INT,
    FOREIGN KEY(idDevice) REFERENCES device(idDevice)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
    FOREIGN KEY(idEmployee) REFERENCES employee(idEmployee)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
    FOREIGN KEY(idCabinet) REFERENCES cabinet(idCabinet)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
    FOREIGN KEY(idAction) REFERENCES action(idAction)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE
);







INSERT INTO deviceType (idDeviceType, deviceType) VALUES
(1, 'Router'),
(2, 'Switch'),
(3, 'Firewall'),
(4, 'PowerSupply');


-- Insert data into pop table
INSERT INTO pop (idPOP, popPosition) VALUES
(1, 'Napoli'),
(2, 'Roma'),
(3, 'Milano'),
(4, 'Torino'),
(5, 'Firenze');

-- Insert data into cabinet table
INSERT INTO cabinet (idCabinet, numOfSlot, idPOP) VALUES
--('A-NA', 20, 1),
--('A-RM', 20, 2),
--('A-MI', 20, 3),
--('A-TO', 20, 4),
--('A-FI', 20, 5)
('C-NA', 20, 1)




-- Insert data into employee table
INSERT INTO employee (idEmployee, name, surname, birthDate, email) VALUES
(1, 'Mario', 'Rossi', '1985-07-20', 'mario.rossi@example.com'),
(2, 'Luigi', 'Verdi', '1990-08-15', 'luigi.verdi@example.com'),
(3, 'Giulia', 'Bianchi', '1982-06-30', 'giulia.bianchi@example.com');

-- Insert data into action table
INSERT INTO action (idAction, actionType) VALUES
(1, 'Install'),
(2, 'Remove'),
(3, 'Update');




-- Insert data into device table
INSERT INTO device (idDevice, serialNumber, sizeDevice, producerDevice, yearProduction, statusDevice, usedSlot, idDeviceType, idEmployee, idCabinet) VALUES
--(1, 'SN123456', 1, 'Cisco', '2020-01-01', 'Active', 'A-NA - 1', 1, 1, 'A-NA'),
--(2, 'SN789012', 2, 'HP', '2019-02-02', 'Removed', NULL, 2, 2, 'A-RM'),
--(3, 'SN345678', 3, 'Juniper', '2021-03-03', 'Inactive', 'A-MI - 1 / 3 ', 3, 3, 'A-MI');
	




-- Insert data into log table
INSERT INTO log (idLog, dateLog, timeLog, slotOccupati, idDevice, idEmployee, idCabinet, idAction) VALUES
--(1, '2024-07-01', '2024-07-01 12:00:00', 1, 1, 1, 'A-NA', 1),
--(2, '2024-07-02', '2024-07-02 13:00:00', 2, 2, 2, 'A-RM', 2),
(1, '2024-07-03', '2024-07-03 14:00:00', 3, 3, 3, 'A-MI', 3);
(4, '2024-07-04', '2024-07-04 12:00:00', 4, 1, 1, 'A-NA', 1),
(5, '2024-07-04', '2024-07-04 12:00:01', 6, 1, 1, 'A-MI', 1);



UPDATE Device SET usedSlot = 'A-NA - 1 / 4'  WHERE idDevice='1'
UPDATE Device SET usedSlot = NULL WHERE idDevice='2'
	

SELECT numOfSlot, idCabinet FROM Cabinet WHERE idCabinet= (SELECT idCabinet FROM Device WHERE idDevice=1)




SELECT DT.DeviceType, D.serialnumber, D.producerdevice, D.iddevice 
	FROM Device AS D LEFT JOIN DeviceType AS DT ON D.idDeviceType=DT.idDeviceType 
	WHERE (D.statusDevice = 'Active' OR D.statusDevice = 'Inactive') AND D.idCabinet= 'A-MI'


SELECT L.slotOccupati, D.idCabinet, D.sizeDevice FROM Log AS L JOIN Device AS D ON  D.idCabinet = L.idCabinet WHERE D.idCabinet = (SELECT idCabinet FROM Device WHERE idDevice=1) AND L.timeLog = (SELECT MAX(timeLog) FROM Log where idCabinet=D.idCabinet)

SELECT * FROM Device

SELECT * FROM Cabinet
SELECT * FROM Log

DROP TABLE Log

DELETE FROM Log Where idLog=8


-- Aggiornamento della sequenza
SELECT setval('log_idlog_seq', (SELECT MAX(idLog) FROM log)); --aggiorniamo sequenza
SELECT setval('device_iddevice_seq', (SELECT MAX(idDevice) FROM Device));

SELECT idEmployee, email FROM Employee WHERE idEmployee = '1' AND email = 'mario.rossi@example.com'




--QUERY CHE RESTIUISCE i cabinet con slot occupati tali da fare spazio a una certa dimensione, raccogliendo i dati dai log. 

SELECT c.idCabinet, COALESCE(l.slotOccupati, 0) AS slotOccupati, c.numOfSlot - COALESCE(l.slotOccupati, 0) AS slotLiberiFROM cabinet c LEFT JOIN (SELECT idCabinet, slotOccupati,ROW_NUMBER() OVER(PARTITION BY idCabinet ORDER BY timeLog DESC) AS rnFROM log WHERE timeLog = (SELECT MAX(timeLog) FROM log l2 WHERE l2.idCabinet = log.idCabinet)) l ON c.idCabinet = l.idCabinet AND l.rn = 1 INNER JOIN PoP p ON c.idPOP = p.idPOP WHERE p.popPosition = 'Napoli' GROUP BY c.idCabinet, c.numOfSlot, l.slotOccupati HAVING (c.numOfSlot - COALESCE(l.slotOccupati, 0)) > 5;


--Massimo spazio residuo nei cabinet, alla posizione attuale--
SELECT MAX(c.numOfSlot - COALESCE(l.slotOccupati, 0)) AS MaxOccupied FROM cabinet c LEFT JOIN log l ON l.idCabinet = c.idCabinet AND l.timeLog = (SELECT MAX(l2.timeLog) FROM log l2 WHERE l2.idCabinet = c.idCabinet) INNER JOIN  PoP p ON c.idPOP = p.idPOP WHERE p.popPosition = 'Napoli';


--Query per inserimento corretto
SELECT C.idCabinet, COALESCE(D.usedSlot, '0') FROM Cabinet AS C JOIN Device AS D ON D.idCabinet= C.idCabinet JOIN POP AS P ON p.idPOP = C.idPOP WHERE  P.popPosition = 'Napoli' AND D.usedSlot != '-' GROUP BY C.idCabinet, D.usedSlot ORDER BY usedSlot 

SELECT idCabinet, numOfSlot from Cabinet AS C join Pop As P on C.idPOP = P.idPOP WHERE P.popPosition = 'Napoli'

SELECT slotOccupati FROM Log WHERE timeLog = (SELECT MAX(timeLog) FROM Log WHERE idCabinet = 'A-NA')


SELECT max(idDevice) from Device

UPDATE LOG SET slotOccupati = NULL where idLog = 8


SELECT L.slotOccupati, D.idCabinet, D.sizeDevice FROM Log AS L JOIN Device AS D ON  D.idCabinet = L.idCabinet WHERE D.idCabinet = (SELECT idCabinet FROM Device WHERE idDevice=15) AND L.timeLog = (SELECT MAX(timeLog) FROM Log where idCabinet=D.idCabinet) 

