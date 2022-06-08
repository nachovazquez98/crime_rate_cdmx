import streamlit as st
st.set_page_config(page_title="Reportes de incidencia delictiva", layout="wide")
import sqlite3
from PIL import Image
import pandas as pd
import itertools 
from crime_plot import crime_plot
from crime_rate_plot import crime_rate_plot
from indv_crime_rate_plot import indv_crime_rate_plot

# pendientes
# 1. agregar graficas poblacion
# 2. agregar seleccion de rango de tiempo y diagarama de los edlitos mas altos en ese rango
# 3. agregar en suma total la seleccion de delito y subtipo de delito y sumarlo, donde esta la opcion de decomposiicon estacional
# 4. en la tabla de cambio porcentual agregar el tipo de sampleo de tiempo para no mostrar solamente meses
def main():
    menu = [
        "Inicio", 
        "Créditos", 
        "Suma total de delitos en ZMG",
        "Tasa de criminalidad en ZMG",
        "Tasa de crimen por municipio"
        ]
    choice_menu = st.sidebar.selectbox("Menu",menu)

    if choice_menu == "Inicio":
        st.title("Inicio")
        st.text('''
                Este proyecto tiene la finalidad de proporcionar 
                información actualizada y automatizada de la criminalidad en el área
                metropolitana de Guadalajara (ZMG), al utilizar los datos abiertos de
                la incidencia delictiva del Secretariado Ejecutivo del Sistema Nacional
                de Seguridad Pública y el censo poblacional del INEGI. Se dispone de
                la información en una interfaz web interactiva donde se puede
                consultar las estadísticas como la tasa de criminalidad, gráficas y filtrar
                los delitos con un aumento respecto a una serie de tiempo
                predeterminada por las estrategias establecidas (1 mes, 6 meses, 1 año,
                etc.) para graficar los delitos con más aumento de los 10 municipios.
                Se agregaron los atributos del delito como: Bien jurídico afectado,
                Tipo de delito, Subtipo de delito y Modalidad.
                
                El objetivo del proyecto es dar a conocer a la sociedad en general la
                información obtenida sobre el fenómeno de la delincuencia, y
                proporcionar elementos para la toma de decisiones de política pública.
                
                Con un análisis estadístico de las determinantes del crimen, poder
                expresar qué características sociodemográficas, cuáles factores
                económicos específicos o qué combinación de ambos motivan a las
                personas a cometer delitos, y que sirva para prevenir y disuadir la
                incidencia de delitos en la ZMG a partir del combate de raíz de la
                problemática.''')
        st.header("Me interesa mucho tu opinión. Actualmente está en desarrollo y mejora continua la aplicación web. Cualquier duda, comentario, ó sugerencia porfavor de contactarse a ignacio.vperez@alumnos.udg.mx")
            
    elif choice_menu == "Créditos":
        st.title("Créditos")
        st.text('''
        El 31 de diciembre de 1994, se llevó a cabo una reforma constitucional en la que se creó un concepto 
        nuevo y ampliado de seguridad pública. Esta dejó de ser atributo y responsabilidad exclusiva de las instituciones 
        gubernamentales centrales para convertirse en responsabilidad de los tres órdenes federal, estatal y municipal. 
        
        El 11 de diciembre de 1995 se publicó la Ley General que establecía las Bases de Coordinación del Sistema Nacional
        de Seguridad Pública y a partir de estas reformas diversos estados de la República comenzaron a generar ordenamientos 
        jurídicos especiales en materia de seguridad pública, así como consejos consultivos estatales y academias de policía 
        o de cuerpos de seguridad pública.
        
        La Seguridad Pública es la principal función del Estado que consiste en la protección de las personas y sus propiedades; 
        de las instituciones políticas de las amenazas de violencia física tanto interna como transnacional, de la intimidación, 
        la corrupción o actos de gobierno predatorios. De acuerdo con la Ley General del Sistema Nacional de Seguridad Pública, 
        en México, esta es una función a cargo de los tres órdenes de gobierno que tiene como fin el salvaguardar la integridad 
        y los derechos de las personas, así como preservar las libertades, el orden y la paz públicos.
        
        La forma de medir la criminalidad es dividiendo el número de delitos conocidos entre un determinado número de habitantes 
        (usualmente 100 mil personas). El resultado de esta operación representa el índice de criminalidad de una ciudad o un país determinado. 
        La metodología para cuantificar la criminalidad es limitada, porque sólo se contabilizan los delitos registrados por las autoridades, 
        quedando fuera aquellos que no son denunciados. Otro problema es la inconsistencia de los registros: no todos los delitos denunciados 
        se registran en las estadísticas finales, ya sea por errores de procedimiento, discrecionalidad o corrupción dentro de los sistemas 
        de procuración y administración de justicia. En un segundo plano, la información obtenida por este medio proporciona una interpretación 
        errónea del problema delictivo al utilizar cifras parciales, lo que imposibilita un diseño adecuado de políticas de atención en la materia. 
        Una consecuencia negativa adicional, es la erosión de la confianza entre autoridades y ciudadanos. 
        
        Está comprobado que los ciudadanos viven constantemente con el temor de ser víctimas de un delito. El miedo al delito, definido como el 
        sentimiento de inseguridad general que tiene la población, es un factor que opera de forma negativa en contra de la información oficial 
        en cuanto a índices delictivos se refiere. La ausencia de denuncias ciudadanas genera lo que se conoce como 
        ‘‘cifra negra’’ u ‘‘oculta’’ de la criminalidad. 
        Este desconocimiento de la criminalidad real dificulta la planeación de las estrategias para combatir la delincuencia.''')
            
    elif choice_menu == "Suma total de delitos en ZMG":
        crime_plot()
    
    elif choice_menu == "Tasa de criminalidad en ZMG":
        crime_rate_plot() 
    elif choice_menu == "Tasa de crimen por municipio":
        indv_crime_rate_plot()


if __name__ == '__main__':
    st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
    padding = 12
    st.markdown(f""" <style>
    * {{
        text-align: justify;
    }}

    .reportview-container .main .block-container{{
        padding-top: {0}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)
    main()


