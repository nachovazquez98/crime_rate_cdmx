# crime_rate_zmg

## Resumen
Este proyecto tiene la finalidad de proporcionar información actualizada y automatizada de la criminalidad en el área metropolitana de Guadalajara (ZMG), al utilizar los datos abiertos de la incidencia delictiva del Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública y el censo poblacional del INEGI. 

Se dispone de la información en una interfaz web interactiva donde se puede consultar las estadísticas como la tasa de criminalidad, gráficas y filtrar los delitos con un aumento respecto a una serie de tiempo predeterminada por las estrategias establecidas (1 mes, 6 meses, 1 año, etc.) para graficar los delitos con más aumento de los 10 municipios. Se recalca que se agregaron los atributos del delito como: Bien jurídico afectado, Tipo de delito, Subtipo de delito y Modalidad.

## Introducción 
El 31 de diciembre de 1994, se llevó a cabo una reforma constitucional en la que se creó un concepto nuevo y ampliado de seguridad pública. Esta dejó de ser atributo y responsabilidad exclusiva de las instituciones gubernamentales centrales para convertirse en responsabilidad de los tres órdenes federal, estatal y municipal. El 11 de diciembre de 1995 se publicó la Ley General que establecía las Bases de Coordinación del Sistema Nacional de Seguridad Pública y a partir de estas reformas diversos estados de la República comenzaron a generar ordenamientos jurídicos especiales en materia de seguridad pública, así como consejos consultivos estatales y academias de policía o de cuerpos de seguridad pública.

La Seguridad Pública es la principal función del Estado que consiste en la protección de las personas y sus propiedades; de las instituciones políticas de las amenazas de violencia física tanto interna como transnacional, de la intimidación, la corrupción o actos de gobierno predatorios. De acuerdo con la Ley General del Sistema Nacional de Seguridad Pública, en México, esta es una función a cargo de los tres órdenes de gobierno que **tiene como fin el salvaguardar la integridad y los derechos de las personas, así como preservar las libertades, el orden y la paz públicos.**
## Sesgo 
La forma de medir la criminalidad es dividiendo el número de delitos conocidos entre un determinado número de habitantes (usualmente 100 mil personas). El resultado de esta operación representa el índice de criminalidad de una ciudad o un país determinado. **La metodología para cuantificar la criminalidad es limitada, porque sólo se contabilizan los delitos registrados por las autoridades, quedando fuera aquellos que no son denunciados.**

Otro problema es la inconsistencia de los registros: no todos los delitos denunciados se registran en las estadísticas finales, ya sea por errores de procedimiento, discrecionalidad o corrupción dentro de los sistemas de procuración y administración de justicia. En un segundo plano, la información obtenida por este medio proporciona una interpretación errónea del problema delictivo al utilizar cifras parciales, lo que imposibilita un diseño adecuado de políticas de atención en la materia. 

Una consecuencia negativa adicional, es la erosión de la confianza entre autoridades y ciudadanos. Está  comprobado que los ciudadanos viven constantemente con el temor de ser víctimas de un delito. El miedo al delito, definido como el sentimiento de inseguridad general que tiene la población, es un factor que opera de forma negativa en contra de la información oficial en cuanto a índices delictivos se refiere. La ausencia de denuncias ciudadanas genera lo que se conoce como ‘‘cifra negra’’ u ‘‘oculta’’ de la criminalidad. **Este desconocimiento de la criminalidad real dificulta la planeación de las estrategias para combatir la delincuencia.**

## Funcionamiento

1. Ambientación:
    - **Referencia**: https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv
    - pip install --user pipenv
    - pipenv shell
    - pipenv sync

2. Se descargan desde la página de Datos Abiertos de Incidencia Delictiva las Cifras de Incidencia Delictiva Municipal más nuevas, se guardan en el directorio /data del proyecto, y se escribe el nombre del archivo csv en el archivo **data_extraction** en la línea 22.

3. Se ejecuta el archivo **data_extraction.py** y se genera el archivo **file_global_vars.txt**

4. streamlit run gui_app.py

## Referencia
- Instituto Nacional de Estadística y Geografía. (n.d.). INEGI. Encuesta Nacional de Victimización de Empresas 2020. Retrieved May 16, 2022, from https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825197889.pdf
- Alejandro Espinosa, Jonatan Hernández, Rubén Leal, & Gilberto Ramos. (n.d.). Las determinantes del crimen en México. Retrieved May 16, 2022, from http://www.ree.economiatec.com/A1N1/206278.pdf
- René A. JIMÉNEZ ORNELAS. (n.d.). LA CIFRA NEGRA DE LA DELINCUENCIA EN MÉXICO: SISTEMA DE ENCUESTAS SOBRE VICTIMIZACIÓN. Retrieved May 16, 2022, from https://archivos.juridicas.unam.mx/www/bjv/libros/1/479/17.pdf
- 
