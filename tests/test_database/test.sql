CREATE TABLE User
(
	Tag VARCHAR(20) PRIMARY KEY CHECK (length(Tag) <= 20),
	Name VARCHAR(64) NOT NULL CHECK (length(Name) <= 64),
	Email VARCHAR(254) NOT NULL CHECK (length(Email) <= 254),
	Password VARCHAR(128) NOT NULL CHECK (length(Password) <= 128)
);
CREATE TABLE Model
(
	Id INTEGER PRIMARY KEY,
	Name VARCHAR(64) NOT NULL CHECK (length(Name) <= 64),
	Description VARCHAR(256) NOT NULL CHECK (length(Description) <= 256),
	Definition TEXT
);
CREATE TABLE Session
(
	Id INTEGER PRIMARY KEY,
	Creator VARCHAR(20),
	ModelId INTEGER,
	CreationDate TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	StartDate TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	ExpirationDate TEXT NOT NULL DEFAULT (datetime('now', '+1 day')),
	Participants TEXT,
	FOREIGN KEY (Creator) REFERENCES User (Tag) ON DELETE CASCADE,
	FOREIGN KEY (ModelId) REFERENCES Model (Id) ON DELETE CASCADE
);

PRAGMA foreign_key = ON;

INSERT INTO User VALUES ('cyber_bob', 'bob', 'rbcmlproject@gmail.com', 'Hello_World');
INSERT INTO User VALUES ('cyber_alice', 'alice', 'rbcmlproject@gmail.com', 'Hello_World');
INSERT INTO Model (Name, Description, Definition) VALUES ('School news', 
							  'This model can be used by schools to announce news',
							  '{"roles":["Student", "Professor", "Principal"],"connections":{"Principal-Professor-Student":[[true, true, true, true, true, true, true, false],[false, true, true, true, true, true, true, false],[false, true, false, true, true, true, false, true]],"Principal-Professor":[[true, true, true, true, true, true, true, false],[true, true, true, true, true, true, false, true]],"Professor-Student":[[true, true, true, true, true, true, true, false],[false, true, true, true, true, true, false, true]]}}');
INSERT INTO Session (Creator, ModelId, Participants) VALUES ("cyber_bob", 1, '{"cyber_bob":["Student"],"cyber_alice":["Principal","Professor"]}');
