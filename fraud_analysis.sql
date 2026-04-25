CREATE DATABASE fraud_detection;
USE fraud_detection;

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trans_date_trans_time DATETIME,
    cc_num BIGINT,
    merchant VARCHAR(200),
    category VARCHAR(100),
    amt DECIMAL(10,2),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender CHAR(1),
    city VARCHAR(100),
    state VARCHAR(10),
    zip INT,
    lat DECIMAL(9,6),
    `long` DECIMAL(9,6),
    city_pop INT,
    job VARCHAR(200),
    dob DATE,
    trans_num VARCHAR(100),
    unix_time BIGINT,
    merch_lat DECIMAL(9,6),
    merch_long DECIMAL(9,6),
    is_fraud TINYINT,
    hour INT,
    day_of_week VARCHAR(20),
    month VARCHAR(20),
    age INT,
    age_group VARCHAR(10)
);

USE fraud_detection;
SELECT COUNT(*) FROM transactions;

SELECT COUNT(*) AS total_columns
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'fraud_detection'
AND TABLE_NAME = 'transactions';

DROP TABLE creditcard_cleaned;

-- 1. Overall Audit
SELECT
  COUNT(*) AS total_transactions,
  SUM(is_fraud) AS fraud_cases,
  ROUND(SUM(is_fraud)/COUNT(*)*100, 4) AS fraud_rate_pct,
  ROUND(SUM(CASE WHEN is_fraud=1 THEN amt ELSE 0 END), 2) AS total_stolen,
  ROUND(AVG(CASE WHEN is_fraud=1 THEN amt END), 2) AS avg_fraud_amt
FROM transactions;

-- 2. Fraud by Category
SELECT category,
  COUNT(*) AS fraud_count,
  ROUND(SUM(amt),2) AS amount_stolen
FROM transactions WHERE is_fraud=1
GROUP BY category ORDER BY fraud_count DESC;

-- 3. Fraud by Hour
SELECT hour,
  SUM(is_fraud) AS fraud_cases,
  ROUND(SUM(is_fraud)/COUNT(*)*100,4) AS fraud_rate
FROM transactions
GROUP BY hour ORDER BY hour;

-- 4. Fraud by State
SELECT state,
  SUM(is_fraud) AS fraud_cases,
  ROUND(SUM(CASE WHEN is_fraud=1 THEN amt ELSE 0 END),2) AS stolen
FROM transactions
GROUP BY state ORDER BY fraud_cases DESC LIMIT 10;

-- 5. Fraud by Age Group
SELECT age_group,
  COUNT(*) AS fraud_cases,
  ROUND(AVG(amt),2) AS avg_stolen
FROM transactions WHERE is_fraud=1
GROUP BY age_group ORDER BY age_group;

-- 6. Fraud by Gender
SELECT gender,
  COUNT(*) AS fraud_cases,
  ROUND(SUM(amt),2) AS total_stolen,
  ROUND(SUM(is_fraud)/COUNT(*)*100,4) AS fraud_rate
FROM transactions GROUP BY gender;

-- 7. Top 10 Merchants by Fraud
SELECT merchant,
  COUNT(*) AS fraud_count,
  ROUND(SUM(amt),2) AS stolen
FROM transactions WHERE is_fraud=1
GROUP BY merchant ORDER BY fraud_count DESC LIMIT 10;