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

INSERT INTO cabinet (idCabinet, numOfSlot, idPOP) VALUES
('A-NA', 20, 1),
('A-RM', 20, 2),
('A-MI', 20, 3),
('A-TO', 20, 4),
('A-FI', 20, 5),
('B-NA', 10, 1),
('C-NA', 15, 1);

-- Insert data into employee table
INSERT INTO employee (idEmployee, name, surname, birthDate, email) VALUES
(1, 'Mario', 'Rossi', '1985-07-20', 'mario.rossi@example.com'),
(2, 'Luigi', 'Verdi', '1990-08-15', 'luigi.verdi@example.com'),
(3, 'Giulia', 'Bianchi', '1982-06-30', 'giulia.bianchi@example.com');

-- Insert data into action table
INSERT INTO action (idAction, actionType) VALUES
(1, 'Install'),
(2, 'Remove'),
(3, 'Update'),
(4, 'ErrorMes');
