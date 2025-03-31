--CREATE DATABASE [Test]

USE [Test]
GO

CREATE TABLE [Users](
	[ID] INT IDENTITY NOT NULL,
	[Login] VARCHAR(50) NOT NULL,
	[Password] VARCHAR(255) NOT NULL,
	[SecretKey] VARBINARY(16),
)

SELECT * FROM [Users]