CREATE TABLE IF NOT EXISTS Admins (
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50),
    Password VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Address VARCHAR(255),
    Password VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS InsurancePolicies (
    PolicyID INT AUTO_INCREMENT PRIMARY KEY,
    PolicyNumber VARCHAR(20),
    PolicyType VARCHAR(50),
    PolicyStartDate DATE,
    PolicyEndDate DATE,
    PremiumAmount DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS PolicyOwnership (
    PolicyOwnerID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    PolicyID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (PolicyID) REFERENCES InsurancePolicies(PolicyID)
);

CREATE TABLE IF NOT EXISTS Claims (
    ClaimID INT AUTO_INCREMENT PRIMARY KEY,
    ClaimNumber VARCHAR(20),
    ClaimDate DATE,
    ClaimAmount DECIMAL(10, 2),
    PolicyID INT,
    Approved INT,
    FOREIGN KEY (PolicyID) REFERENCES InsurancePolicies(PolicyID)
);

CREATE TABLE IF NOT EXISTS InsuranceAgents (
    AgentID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Password VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS PolicyAssignments (
    AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
    PolicyID INT,
    AgentID INT,
    AssignmentDate DATE,
    FOREIGN KEY (PolicyID) REFERENCES InsurancePolicies(PolicyID),
    FOREIGN KEY (AgentID) REFERENCES InsuranceAgents(AgentID)
);
