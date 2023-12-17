USE [master]
GO
CREATE DATABASE [ChessDB]
USE [ChessDB]
GO
/****** Object:  Table [dbo].[PlayerData]    Script Date: 9/6/2023 23:02:07 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PlayerData](
	[Id] [int] NOT NULL,
	[Account] [nvarchar](15) NOT NULL,
	[Password] [char](20) NOT NULL,
	[Online] [char](5) NOT NULL,
	[Point] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[PlayerData] ADD  CONSTRAINT [DF_PlayerData_Point]  DEFAULT ((0)) FOR [Point]
GO
