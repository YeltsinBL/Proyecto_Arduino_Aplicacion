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
