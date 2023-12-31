CREATE DATABASE [Invernadero]
go
USE [Invernadero]
GO
/****** Object:  Table [dbo].[mediciones]    Script Date: 5/11/2023 23:32:02 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[mediciones](
	[idmediciones] [int] IDENTITY(22,1) NOT NULL,
	[humedad_inicial] [decimal](5, 2) NULL,
	[humedad_final] [decimal](5, 2) NULL,
	[temperatura_inicial] [decimal](5, 2) NULL,
	[temperatura_final] [decimal](5, 2) NULL,
	[fecha_registro] [datetime2](0) NULL,
	[sector_id] [int] NOT NULL,
 CONSTRAINT [PK_mediciones_idmediciones] PRIMARY KEY CLUSTERED 
(
	[idmediciones] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Sector]    Script Date: 5/11/2023 23:32:02 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Sector](
	[idSector] [int] IDENTITY(3,1) NOT NULL,
	[Sector_Nombre] [nvarchar](45) NULL,
	[Sector_Estado] [bit] NULL,
 CONSTRAINT [PK_Sector_idSector] PRIMARY KEY CLUSTERED 
(
	[idSector] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[usuarios]    Script Date: 5/11/2023 23:32:02 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[usuarios](
	[id] [int] IDENTITY(4,1) NOT NULL,
	[name_surname] [nvarchar](100) NOT NULL,
	[email_user] [nvarchar](50) NOT NULL,
	[pass_user] [nvarchar](max) NOT NULL,
	[created_user] [datetime] NOT NULL,
 CONSTRAINT [PK_users_id] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[mediciones] ON 

INSERT [dbo].[mediciones] ([idmediciones], [humedad_inicial], [humedad_final], [temperatura_inicial], [temperatura_final], [fecha_registro], [sector_id]) VALUES (22, CAST(10.50 AS Decimal(5, 2)), CAST(42.00 AS Decimal(5, 2)), CAST(30.00 AS Decimal(5, 2)), CAST(40.00 AS Decimal(5, 2)), CAST(N'2023-11-01T04:28:44.0000000' AS DateTime2), 3)
INSERT [dbo].[mediciones] ([idmediciones], [humedad_inicial], [humedad_final], [temperatura_inicial], [temperatura_final], [fecha_registro], [sector_id]) VALUES (23, CAST(20.00 AS Decimal(5, 2)), CAST(60.00 AS Decimal(5, 2)), CAST(10.00 AS Decimal(5, 2)), CAST(50.00 AS Decimal(5, 2)), CAST(N'2023-10-31T00:00:00.0000000' AS DateTime2), 4)
INSERT [dbo].[mediciones] ([idmediciones], [humedad_inicial], [humedad_final], [temperatura_inicial], [temperatura_final], [fecha_registro], [sector_id]) VALUES (24, CAST(80.00 AS Decimal(5, 2)), CAST(10.00 AS Decimal(5, 2)), CAST(70.00 AS Decimal(5, 2)), CAST(30.00 AS Decimal(5, 2)), CAST(N'2023-11-02T00:31:37.0000000' AS DateTime2), 4)
INSERT [dbo].[mediciones] ([idmediciones], [humedad_inicial], [humedad_final], [temperatura_inicial], [temperatura_final], [fecha_registro], [sector_id]) VALUES (25, CAST(80.00 AS Decimal(5, 2)), CAST(10.00 AS Decimal(5, 2)), CAST(30.00 AS Decimal(5, 2)), CAST(70.00 AS Decimal(5, 2)), CAST(N'2023-11-02T01:15:33.0000000' AS DateTime2), 4)
INSERT [dbo].[mediciones] ([idmediciones], [humedad_inicial], [humedad_final], [temperatura_inicial], [temperatura_final], [fecha_registro], [sector_id]) VALUES (26, CAST(20.00 AS Decimal(5, 2)), CAST(30.00 AS Decimal(5, 2)), CAST(15.00 AS Decimal(5, 2)), CAST(25.00 AS Decimal(5, 2)), CAST(N'2023-11-02T23:44:03.0000000' AS DateTime2), 3)
INSERT [dbo].[mediciones] ([idmediciones], [humedad_inicial], [humedad_final], [temperatura_inicial], [temperatura_final], [fecha_registro], [sector_id]) VALUES (29, CAST(10.00 AS Decimal(5, 2)), CAST(40.00 AS Decimal(5, 2)), CAST(40.00 AS Decimal(5, 2)), CAST(10.00 AS Decimal(5, 2)), CAST(N'2023-11-05T19:56:51.0000000' AS DateTime2), 3)
SET IDENTITY_INSERT [dbo].[mediciones] OFF
GO
SET IDENTITY_INSERT [dbo].[Sector] ON 

INSERT [dbo].[Sector] ([idSector], [Sector_Nombre], [Sector_Estado]) VALUES (3, N'Planta 1', 1)
INSERT [dbo].[Sector] ([idSector], [Sector_Nombre], [Sector_Estado]) VALUES (4, N'Planta 2', 1)
SET IDENTITY_INSERT [dbo].[Sector] OFF
GO
SET IDENTITY_INSERT [dbo].[usuarios] ON 

INSERT [dbo].[usuarios] ([id], [name_surname], [email_user], [pass_user], [created_user]) VALUES (4, N'chemoYBL', N'chemo@chemo.com', N'scrypt:32768:8:1$yUBsXYlFrkrVqpZJ$9eb21b4d39bd480de56daa450a93ecd2f51a14a60b476272dbb1a860ebc3a9944df6ac78af00b9f2b136fab23fc81fee0afae0fcb323748963ea6c61bff0122f', CAST(N'2023-10-31T00:55:31.000' AS DateTime))
INSERT [dbo].[usuarios] ([id], [name_surname], [email_user], [pass_user], [created_user]) VALUES (5, N'GuillermiBaltodano', N'gb@gb.com', N'scrypt:32768:8:1$5fBmdi9afv41WA4W$bca6bc1c92a9c6cfe8b1c3b91e6495d87f71b6b737042dfc3e395a373900f906827d2831f1c3892b519f4cea04f7827ae541346d705d04d360d618d0b5ba05ec', CAST(N'2023-11-06T04:27:50.210' AS DateTime))
SET IDENTITY_INSERT [dbo].[usuarios] OFF
GO
ALTER TABLE [dbo].[mediciones] ADD  DEFAULT (NULL) FOR [humedad_inicial]
GO
ALTER TABLE [dbo].[mediciones] ADD  DEFAULT (NULL) FOR [humedad_final]
GO
ALTER TABLE [dbo].[mediciones] ADD  DEFAULT (NULL) FOR [temperatura_inicial]
GO
ALTER TABLE [dbo].[mediciones] ADD  DEFAULT (NULL) FOR [temperatura_final]
GO
ALTER TABLE [dbo].[mediciones] ADD  DEFAULT (NULL) FOR [fecha_registro]
GO
ALTER TABLE [dbo].[Sector] ADD  DEFAULT (NULL) FOR [Sector_Nombre]
GO
ALTER TABLE [dbo].[Sector] ADD  DEFAULT (NULL) FOR [Sector_Estado]
GO
ALTER TABLE [dbo].[usuarios] ADD  DEFAULT (getdate()) FOR [created_user]
GO
ALTER TABLE [dbo].[mediciones]  WITH CHECK ADD  CONSTRAINT [mediciones$medicion_sector_id] FOREIGN KEY([sector_id])
REFERENCES [dbo].[Sector] ([idSector])
GO
ALTER TABLE [dbo].[mediciones] CHECK CONSTRAINT [mediciones$medicion_sector_id]
GO
