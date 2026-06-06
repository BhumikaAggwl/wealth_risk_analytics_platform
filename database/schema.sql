CREATE TABLE clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(100),
    age INT,
    risk_profile VARCHAR(20),
    investment_amount DECIMAL(15,2),
    investment_horizon INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO clients (
	client_name,
	age,
	risk_profile,
	investment_amount , 
	investment_horizon 

)
VALUES(
	'Bhumika',
	21,
	'Moderate',
	5000000,
	10
);


SELECT * FROM clients


-- PORTFOLIO TABLE 
CREATE TABLE portfolios( 
	portfolio_id INT AUTO_INCREMENT PRIMARY KEY,
	client_id INT ,
	portfolio_name VARCHAR(100),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
	FOREIGN KEY(client_id)
	REFERENCES clients(client_id)
);


-- HOLDINGS 
CREATE TABLE holdings( 
	holding_id INT AUTO_INCREMENT PRIMARY KEY,
	portfolio_id INT , 
	ticker VARCHAR(20 ),
	asset_type VARCHAR(50),
	allocation_percent DECIMAL(5,2),
	
	FOREIGN KEY(portfolio_id)
	REFERENCES portfolios(portfolio_id)
);



-- RISK METRICS 
CREATE TABLE risk_metrics( 
	metric_id INT AUTO_INCREMENT PRIMARY KEY , 
	
	portfolio_id INT, 
	
	expected_return DECIMAL(10,4),
	
	volatility DECIMAL(10,4),
	
	sharpe_ratio DECIMAL(10,4),
	
	var_95 DECIMAL(10,4),
	
	max_drawdown DECIMAL(10,4),
	
	calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	
	FOREIGN KEY (portfolio_id)
    REFERENCES portfolios(portfolio_id)
);

SELECT * FROM holdings;


SELECT * FROM risk_metrics;



CREATE TABLE market_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(20),
    trade_date DATE,
    close_price DECIMAL(15,4)
);



SELECT COUNT(*) FROM market_data;

SELECT *
FROM market_data
LIMIT 69;

CREATE TABLE client_recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_score INT,
    risk_profile VARCHAR(20),
    expected_return DECIMAL(10,4),
    volatility DECIMAL(10,4),
    sharpe_ratio DECIMAL(10,4),
    var_95 DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


SELECT COUNT(*) FROM clients;
SELECT COUNT(*) FROM portfolios;
SELECT COUNT(*) FROM holdings;
SELECT COUNT(*) FROM market_data;
SELECT COUNT(*) FROM risk_metrics;
