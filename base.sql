DROP TABLE IF EXISTS public.cineprocesado;
CREATE TABLE public.cineprocesado
(
    "Provincia" text,
    "Pantallas" text,
    "Butacas" text,
    "espacio_INCAA" text,
    fecha text
);


DROP TABLE IF EXISTS public.totalespor;
CREATE TABLE public.totalespor
(
    "Categoría" text,
    "Cantidad" text,
    fecha text
);


DROP TABLE IF EXISTS public.informacion;
CREATE TABLE public.informacion
(
    "Cod_Loc" text,
    "IdProvincia" text,
    "IdDepartamento" text,
    "Categoría" text,
    "Provincia" text,
    "Localidad" text,
    "Nombre" text,
    "Domicilio" text,
    "CP" text,
    "Teléfono" text,
    "Mail" text,
    "Web" text,
    fecha text
);

