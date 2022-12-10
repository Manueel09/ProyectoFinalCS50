# ProyectoFinalCS50
# ¡Bienvenido al repositorio de HERA!
#### Video Demo: https://www.youtube.com/watch?v=rbNjJYddoeU 
#### Description: HERA, es una app WEB, que permite visualizar y regugistra los datos obtenidos de las mediciones del sensor MAX30105 de pulso cardiaco que se ha tomado un determinado usuario.

- ### COLABORADORES.
- ##### DYLAN STEVEN  RIZO POVEDA
- ##### MANUEL FERNANDO CONRADO FERNANDEZ.
- ##### CARLOS JAVIER GARCÍA PEREZ

#### Pasos requeridos para utilizar la app web HERA:
1.  Realice las conexiones necesarias para poner en funcionamiento el sensor de pulso cardiaco MAX30105, para ayudarle con este paso le proporcionaremos el siguiente esquematico, dé click [aqui](https://www.bing.com/images/search?view=detailV2&insightstoken=bcid_TnXLfe655.0Ei3N6ef9fdzQe.uhr......0*ccid_dct97rnn&form=SBIIRP&iss=SBIUPLOADGET&sbisrc=ImgDropper&idpbck=1&sbifsz=565+x+510+%c2%b7+30.92+kB+%c2%b7+jpeg&sbifnm=Imagen+de+WhatsApp+2022-12-10+a+las+03.38.57.jpg&thw=565&thh=510&ptime=247&dlen=42216&expw=565&exph=510&selectedindex=0&id=1643799539&ccid=dct97rnn&vt=2&sim=11 "aqui") para ver el esquematico.

2. Como segundo requerimiento dé click [aquí](https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library "aquí") para dirigirse al repositorio donde podrá descargar la librería que estaremos utilizando para el sensor, que deberá instalar en su IDE de Arduino de la version de su preferencia.

3. Una vez que haya hecho los ejemplos anteriores, ubiquese en los ejemplos de la librería, justamente al que dice "Example5_HeartRate.ino" y abralo. Eate programa es el que estaremos utilizando.

### Introducción. 
HERA, es el nombre que hemos elegido para nuestro proyecto, por las siglas "Heart Electric Rate with Arduino". Esta aplicación web es capaz de comunicarse con el puerto serial de arduino donde el sensor arroja los datos leidos de las mediciones y los extrae, para ser alamacenados en una base de datos junto a otros datos que seran de relevancia para obtener del usuario.

Este proyecto va dirigido principalmente a los centros médicos, donde se propone esta alternativa para llevar un mejor control  sobre los pacientes que posean alguna enfermedad cardiovascular. Esta aplicacion, trata de ser intuitiva para el usuario así como para el médico, que ingresando como "administrador" podrá acceder tanto a todas las mediciones hechas por los distintos usuarios registrados, como a todos los registros que se han realizado con su respectiva fecha y hora para tener un mayor orden. 

### Explicación del código de HERA.
Para la creación de era, nos hemos apoyado en distintos lenguajes de programación, como lo fueron: C, Python, JavaScript. Así, como también nos apoyamos con lenguaje de marcado de hipertexto (HTML), CSS, SQLite. esn su conjunto, cada uno de estos lenguajes fueron utilizados para hacer una tarea en especifico dentro de nuestro proyecto Hera, buscando siempre la accesibilida, sencillez y versatilidad para que el usuario tenga una navegación placentera.

Para el desarrollo de nuestra aplicacion web nos apoyamos en el **Framework** FLASK, que está escrtito en python y que posee distintas librerias con funciones que nos serían muy utilies, como es el caso de la lfuncion "serial" que nos permitió extraer y exportar los datos desde el monitor serie del IDE de Ardunio hasta nuestra funcion de Flask, permintiendo así almacernar el valor de las mediciones en una variable que utilizamos como el dato de relevancia que queriamos mostrar.

En el archivo "app.py" de nuestro proyecto. podemos emcontar distintas funciones que van para el registro del usuario, que es un paso muy imortante a la hora de obtener datos como la edad, el nombre completo del usuario, que haciendo uso de una base de datos como lo es SQLite, con distintas consultas fuimos capaces de almacenar todas esta informacion para ser ocupada posteriormente como lo es cuando un usuario desea ingresar y ya está registrado, al poner sus datos (Usuario y Contraseña), era capaz de ingresar al inicio de la aplicacion web.

También, en las funciones de login y registros, evaluamos distintas situaciones  que realizará la aplicación cuando el usuario no ingrese algun campo de registro o de ingresar, así como el evaluar si la contraseña y el usuario ingresados son correctos.

Una vez que se haya ingresado de manera correcta, el usurio tendrá acceso a distintos apartados, como lo es de "Medicion", que ya dentro de este al presionar el botón de "realizar medicion" de inmediato se empezará a realizar la funcion "medicionbase" que esta parte del codigo su funcion es almacenar los valores dentro de un rango de tiempo en una lista, para luego sacar el promedio de las mediciones alamcenadas en dicha lista y este resultado será la medida a presentar al usuario y el que será almacenado en la tabla de datos. En la fución "medicionbase", también realizamos un filtrado de datos, ya que no todos los datos capturados por el sensor son reales, ya que el sensor no es 100 % eficiente, por lo cual nos desasemos de valores basuaras con una condicional.

Dentro de los archivos de nuestra aplicacion web, encontramos las carpeta llamada "templates", donde están ubicados todos los archivos html correspondientes a las disntintas ubicaciones donde podrá acceder ya sea el usuario o el administrador. Acceder como administrador, tiene una seríe de apartados específicos de interés, que en este caso sería el medico. para acceder como administrador, solo debe se ingresar una contraseña especifica y tendrá acceso, esta parte se evalua también en la parte de login de nuestro archivo "app.py"

Otra carpeta que podemos encontrar es la llamada "statics", donde ubicamos nuestros archivos de extención .css y .js, que son los encargados de darle a la aplicación un entorno más llamativo y bonito en donde el usuario pueda navedar y acceder a los distintos apartados de su interés.
