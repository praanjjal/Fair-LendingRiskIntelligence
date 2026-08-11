CREATE DATABASE fair_lending;
GO
USE fair_lending;
GO
CREATE SCHEMA raw;
GO
CREATE SCHEMA stg;
GO
CREATE SCHEMA core;
GO
CREATE SCHEMA mart;
GO
CREATE SCHEMA audit;
GO
CREATE SCHEMA ml;
GO
CREATE SCHEMA ai;
GO





USE fair_lending;
GO
SELECT name FROM sys.schemas
WHERE name IN ('raw','stg','core','mart','audit','ml','ai')
ORDER BY name;