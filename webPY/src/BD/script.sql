create table Estadistica(
IdEStadistica int primary key identity,
Descripcion varchar(50),
Temperatura_Inicial decimal(3,2),
Temperatura_Inicial_Fecha datetime default(GetDate()),
Temperatura_Final decimal(3,2),
Temperatura_Final_Fecha datetime default(GetDate()),
Humedad_Inicial decimal(3,2),
Humedad_Inicial_Fecha datetime default(GetDate()),
Humedad_Final decimal(3,2),
Humedad_Final_Fecha datetime default(GetDate())
)

ALTER TABLE Estadistica
ALTER COLUMN Humedad_Final decimal(5,2);

insert into Estadistica (Descripcion, Temperatura_Inicial, Temperatura_Final,
Humedad_Inicial, Humedad_Final)
values('Planta 1', 50.00,55.00, 25.00, 75.00);

select CONCAT(CONVERT(varchar(50),Temperatura_Inicial_Fecha,103),' ',CONVERT(varchar(50),Temperatura_Inicial_Fecha,24)) as [Fecha Temperatura Inicial],
	CONVERT(varchar(6),Temperatura_Inicial) as [Temperatura Inicial] from Estadistica
	where IdEStadistica=12
	select * from Estadistica