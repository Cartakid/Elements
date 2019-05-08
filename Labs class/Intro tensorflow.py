# -*- coding: utf-8 -*-
"""Juan Jose ML con TF 1 - Intro a TensorFlow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wwTiYFClx_-v5rut0oirl-SczJehDXqM

# Introducción

Éste notebook busca introducir uno de los frameworks más populares de `Python`: `TensorFlow`. Si bien no es una explicación exhaustiva, se busca que sea concisa, por lo que cualquier consulta no dude en preguntarme.

## `TensorFlow`

Google lanzó de manera abierta su framework de machine learning, [**`TensorFlow`**](https://www.tensorflow.org/) en el 2015. La librería está implementada en `C++`, pero nos concentraremos en su API de `Python`. 

Los cálculos o computaciones son descritos como diagramas de flujo. Quizá su mayor ventaja es la *diferenciación automática*, lo cual nos permite implementar **backpropagation** sin ahondar mucho en los detalles de cada derivada.

Otra gran ventaja que incluye `TensorFlow` es la herramienta de visualización *TensorBoard* con el cual podemos visualizar las transformaciones de los datos, resúmenes de los datos, histogramas, imágenes generadas, entre otros.

Es de notarse que TensorFlow se puede usar para más que redes neuronales, gracias a sus propiedades algebraicas y matriciales.

---
### Instalación

Véase la documentación original de Google para la instalación de `TensorFlow`, pero con las últimas versiones estables, lo más probable es que sea del siguiente tipo:

```
pip install tensorflow
```

Si se tiene una tarjeta de video NVidia con CUDA instalado, podemos proseguir a utilizar la versión de `TensorFlow` con GPU:

```
pip install tensorflow-gpu
```

En cualquier caso, el siguiente bloque de código no debe de darnos error:
"""

import tensorflow as tf

print(tf.__version__)

"""Utilizaremos la versión `1.x`, ya que si bien ahora está disponible la versión alpha de `2.0`, no todos la estarán implementando, por lo que lo más probable es que encuentre programas o scripts con la versión que usaremos ahora.

El siguiente texto ha sido adaptado del libro [Machine Learning with TensorFlow]() de Nishant Shukla. Si bien trataré de ser lo más exhaustivo posible, no me será posible incluir todo el material, por lo que les recomiendo que consigan una copia del mismo, o bien que vean la documentación de [`TensorFlow`](https://www.tensorflow.org).

## Representando a tensores

En `TensorFlow`, utilizaremos *tensores*. Se puede imaginar a un tensor como una generalizacion de una matriz. En efecto, tendremos lo siguiente:

  - Un escalar será un tensor de rango 0.
  - Un vector de $n\times1$ será un tensor de rango 1.
  - Una matriz de $n\times m$ será un tensor de rango 2.
  - Una matriz de $n\times m \times c$ será un tensor de rango 3. Podemos imaginarlo como $n$ matrices de tamaño $m\times c$.
  - etc.
  
Por lo tanto, *el rango nos indica la cantidad de índices que se necesitan para representar un elemento del tensor*. Veamos un ejemplo:

El tensor `[[[1 ,2], [3, 4], [5, 6]], [[7, 8], [9, 10], [11, 12]]]` tiene dimensiones $3 \times 2 \times 2$, por lo que será un tensor de rango 3, ya que necesitamos 3 índices para indicar alguno de los elementos del mismo.

En general, utilizaremos matrices de `NumPy` en `TensorFlow`. Presentamos tres maneras de definir a una matriz de $2\times2$:
"""

import numpy as np

m1 = [[1.0, 2.0],
      [3.0, 4.0]]

m2 = np.array([[1.0, 2.0],
               [3.0, 4.0]], dtype=np.float32)

m3 = tf.constant([[1.0, 2.0],
                  [3.0, 4.0]])

print(type(m1))
print(type(m2))
print(type(m3))

"""Podemos crear tensores (objetos) a partir de estos tres distintos tipos mediante [`tf.convert_to_tensor`](https://www.tensorflow.org/api_docs/python/tf/convert_to_tensor):"""

t1 = tf.convert_to_tensor(m1, dtype=tf.float32)
t2 = tf.convert_to_tensor(m2, dtype=tf.float32)
t3 = tf.convert_to_tensor(m3, dtype=tf.float32)

"""Ahora, los tres serán del mismo tipo:"""

print(type(t1))
print(type(t2))
print(type(t3))

"""Usualmente no es necesario convertir explícitamente a cada objeto a un tensor, ya que `TensorFlow` lo hará por nosotros, pero es útil utilizar la función `tf.convert_to_tensor(...)` para saber que estamos operando con tensores.

Definamos otros tensores:
"""

m1 = tf.constant([[1., 2.]])

m2 = tf.constant([[1], [2]])

m3 = tf.constant([[[1, 2],
                   [3, 4],
                   [5, 6]],
                   [[7, 8],
                   [9, 10],
                   [11, 12]]])

"""¿Qué pasa ahora si queremos imprimir los valores de estos tensores?"""

print(m1)
print(m2)
print(m3)

"""Obtendremos algo del tipo `Tensor("Const:0", shape=(n, m), dtype=dtype)`, donde el primero nos indicará el label o nombre del tensor, el segundo las dimensiones del mismo, y por último el tipo de datos que contiene. Por lo tanto, podemos nombrar a cada uno de los tensores para así tener una mejor idea de cuál es el que estamos tratando, pero de no hacerlo, la librería los nombra automáticamente.

`TensorFlow` también tiene constructores simples como en `NumPy`: por ejemplo, podemos construir un tensor de $100\times300$ cuyos elementos son todos iguales a `0.2` mediante:

```python
>>> tf.ones([100, 300]) * 0.2
```

## Creando operadores

Uno de los operadores más simples es la negación o cambio de signo. Lo utilizamos de la siguiente manera:
"""

x = tf.constant([[1, 2]])
negMatrix = tf.negative(x)
print(negMatrix)

"""Vemos que el output no es `[[-1, -2]]`, ya que estamos imprimiendo la definición de la operación negación y no su evaluación. Más adelante veremos cómo imprimir dicha evaluación. Por lo tanto, igual que antes, vemos que el tensor `negMatrix` ha sido nombrado como `"Neg:0"` por `TensorFlow`, pero pudo haber sido nombrado explícitamente por nosotros desde un inicio:

```python
tf.negative(x, name="Nombre")
```

Nombramos ahora algunos de los operadores más útiles, pero hay más que se pueden encontrar en la documentación de [`tf.math`](https://www.tensorflow.org/api_docs/python/tf/math):

* `tf.add(x, y)`, donde sumamos dos tensores `x` y `y` de mismo tipo
* `tf.subtract(x, y)`, donde restamos dos tensores `x` y `y` de mismo tipo
* `tf.multiply(x, y)`, donde multiplicamos a los dos tensores `x` y `y`, elemento por elemento
* `tf.pow(x, y)`, donde elevamos `x` a la potencia de `y`, elemento por elemento
* `tf.exp(x)`, equivalente a `tf.pow(e, x)`
* `tf.sqrt(x)`, equivalente a `tf.pow(x, 0.5)`
* `tf.div(x, y)`, tomamos a la división de `x` dentro de `y`, elemento por elemento
* `tf.truediv(x, y)`, igual que `tf.div(...)`, solo que se toman a los argumentos como de tipo `float`
* `tf.floordiv(x, y)`, igual que `tf.truediv(...)`, solo que ahora se redondea para abajo a la respuesta final (de tipo `int`)
* `tf.mod(x, y)`, tomamos al residuo de la división de `x` dentro de `y`, elemento por elemento

***
**Ejercicio 1:** Use a los operadores que acabamos de listar para producir una distribución Normal ($x \sim \mathcal{N}(0, 1)$). Use a `pi` de `math` y defina a la media y varianza en como tipo `float`.

*Solución:* Los operadores clásicos, `*, +, -` se pueden usar de envés de a `tf.multiply(...)`, etc. Por lo tanto, ya que la distribución Gaussiana se define mediante:

$$ f(x; \mu, \sigma^2) = \frac{1}{\sqrt{2 \pi} \sigma} \exp{\left(-\frac{(x-\mu)^2}{2 \sigma^2}\right)}$$

podemos usar a los operadores clásicos y no tantos operadores de `TensorFlow` para así no confundirnos tanto. La distribución nos queda entonces de la siguiente manera:

```python
>>> from math import pi
>>> mean = 0.0
>>> sigma = 1.0

>>> tf.exp(tf.negative(tf.pow(x - mean, 2.0) / (2.0 * tf.pow(sigma, 2.0)))) * (1.0 / (sigma * tf.sqrt(2.0 * pi)))

```
***
"""

from math import pi
mean = 0.0
sigma = 1.0
tf.exp(tf.negative(tf.pow(x - mean, 2.0) / (2.0 * tf.pow(sigma, 2.0)))) * (1.0 / (sigma * tf.sqrt(2.0 * pi)))

"""## Ejecutando operadores con sesiones

Una *sesión* es un ambiente de un sistema de software que describe cómo se deben de ejecutar las líneas de un código. En `TensorFlow`, una sesión configura cómo hablan entre sí los dispositivos de hardware (ya sean CPUs o GPUs). Así, solamente diseñamos el algoritmo de aprendizaje automático sin preocuparnos de cómo manejar el hardware en el que se va a correr. Después podemos preocuparnos por configurar la sesión para cambiar su comportamiento sin tener que cambiar el código del algoritmo.

Entonces, para ejecutar una operación y recuperar el valor calculado, `TensorFlow` requiere de una sesión: solamente una sesión registrada puede rellenar los valores de un objeto de tipo `Tensor`. Entonces, debemos de crear una clase sesión mediante `tf.Session()` e indicarle que corra un operador.
"""

x = tf.constant([[1., 2.]])
neg_op = tf.negative(x)

with tf.Session() as sess:
    result = sess.run(negMatrix)

print(result)
print(type(result))

"""Entonces, una sesión configura *dónde* se va a computar el código y *cómo* se va a establecer la computación para paralelizar la misma. Ésto lo podemos notar más en el código que acabamos de correr: fue mucho más lento de lo que esperábamos, pero el código está optimizado para poder paralelizar códgio más largo y complicado que éste.

Otra forma equivalente es usando la función `eval()` que cada objeto de tipo `Tensor` tiene. Podemos usar esta función con la sesión interactiva de `TensorFlow`, la cual puede ser muy útil a la hora de presentar el código o bien para encontrar bugs en el mismo.
"""

sess = tf.InteractiveSession()

x = tf.constant([[1., 2.]])
negMatrix = tf.negative(x)

result = negMatrix.eval()

print(result)
print(type(result))

sess.close()

"""Ahora es importante que cerremos la sesión para así liberar recursos de nuestro dispositivo.

### Entendiendo al código como un grafo

Regresemos al Ejercicio 1: usamos muchas operaciones matemáticas, así como otros operadores de `TensorFlow`. Podemos, entonces, pensar que cada operador es un nodo en un grafo: cada suma, resta, multiplicación, división, potencia y negación será un nodo. Los bordes entre estos nodos representarán la composición de los operadores a utilizar. Entonces, un `Tensor` será transformado conforme viaje hacia adentro o afuera de los bordes entre los nodos. Es decir, un tensor fluirá a través del grafo, lo que le da el nombre a esta librería: `TensorFlow`.

![](https://dpzbhybb2pdcj.cloudfront.net/shukla/Figures/02fig03_alt.jpg)
*Fig. 1: La composición de muchos operadores simples nos da como resultado una función complicada: la distribución Gaussiana.*

### Ajustando las configuraciones de la sesión

Podemos pasarle opciones a `tf.Session`. La opción más usada es la de `feed_dict`, pero ahondaremos en esta más adelante. Podemos además, ver el listado de equipo a usar (CPUs y GPUs disponibles) mediante el siguiente comando:
"""

x = tf.constant([[1., 2.]])

negMatrix = tf.negative(x)

with tf.Session() as sess:
    result = sess.run(negMatrix)
    devices = sess.list_devices()
    for d in devices:
        print(d.name)
        print(d.device_type)
        
print(result)

"""Quizá falte la opción más útil que es `log_device_placements=True`, la cual nos permitirá ver cómo `TensorFlow` asigna cada operación a cada dispositivo (CPU o GPU). Lamentablemente, en `Jupyter` no se imprime esta información, por lo que solo podremos ver el siguiente resultado si corremos el código en una consola, por ejemplo.

```python
>>> x = tf.constant([[1., 2.]])

>>> negMatrix = tf.negative(x)

>>> with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
...    result = sess.run(negMatrix)
        
>>> print(result)

Device mapping:
/job:localhost/replica:0/task:0/device:XLA_CPU:0 -> device: XLA_CPU device
2019-04-24 01:13:01.898822: I tensorflow/core/common_runtime/direct_session.cc:307] Device mapping:
/job:localhost/replica:0/task:0/device:XLA_CPU:0 -> device: XLA_CPU device

Neg: (Neg): /job:localhost/replica:0/task:0/device:CPU:0
2019-04-24 01:13:01.901110: I tensorflow/core/common_runtime/placer.cc:927] Neg: (Neg)/job:localhost/replica:0/task:0/device:CPU:0
Const: (Const): /job:localhost/replica:0/task:0/device:CPU:0
2019-04-24 01:13:01.901230: I tensorflow/core/common_runtime/placer.cc:927] Const: (Const)/job:localhost/replica:0/task:0/device:CPU:0

```

Una sesión no corre únicamente el grafo de una operación, también puede tomar como inputs a [`tf.placeholder`](https://www.tensorflow.org/api_docs/python/tf/placeholder), [`tf.consant`](https://www.tensorflow.org/api_docs/python/tf/constant) y [`tf.Variable`](https://www.tensorflow.org/api_docs/python/tf/Variable). Resumimos un poco de cómo vamos a utilizar a los mismos:

* **`tf.placeholder`:** Es un valor que no ha sido asignado pero que va a ser inicalizado por la sesión donde sea corrido. Típicamente lo utilizamos para el *input* y *output* del modelo.
* **`tf.constant`:** Es un valor que no cambia, como hiperparámetros del modelo (número de neuronas, learning rate, etc.) o bien configuraciones del mismo.
* **`tf.Variable`:** Es un valor que puede cambiar, tales como los parámetros del modelo (interceptos, coeficientes, etc.). Debemos de inicializarlos mediante la sesión antes de que los podamos usar.

![sesion](https://dpzbhybb2pdcj.cloudfront.net/shukla/Figures/02fig04.jpg)
*Fig. 2: La sesión dicta cómo se va a utilizar el hardware para procesar al grafo de la manera más eficiente posible. Al iniciar la sesión, se les asigna al CPU o GPU cada uno de los nodos y al finalizar se obtienen los datos en un formato útil como un array de `NumPy`.*

## Usando variables

Claramente, no queremos limitar a nuestros modelos a siempre utilizar constantes. Por lo tanto, podemos utilizar a la clase `tf.Variable` para representar, válgase la redundancia, una variable cuyo valor varía con el tiempo (o bien que reacciona conforme otras variables cambian). En efecto, en una regresión lineal simple, debemos de inicializar al intercepto y pendiente con unos valores cualesquieras, pero después debemos de irlos actualizando, cada vez obteniendo mejores y mejores resultados. Por lo tanto, a éstos se les llaman los *parámetros* del modelo, ya que cualquier modelo de aprendizaje automático tendrá los suyos, la clase `tf.Variable` es perfecta para el trabajo.

Veamos un ejemplo simple de detectar cuándo el cambio en el valor de una acción en la bolsa de valores tiene una subida o bajada pronunciada (*spikes*). Lo correremos todo como una sesión interactiva:
"""

sess = tf.InteractiveSession()

raw_data = [0.1, 0.25, 0.8, -0.1, 0., 0.55, 0.65, 1.2]
spike = tf.Variable(False)  # Inicializamos la variable booleana con un valor 
spike.initializer.run()     # Debemos de inicializar a todas las variables al llamar a .run() con su inicializador

for i in range(1, len(raw_data)):
    if abs(raw_data[i] - raw_data[i-1]) > 0.5:  # Si el cambio entre el actual y el anterior es mayor a 0.5%
        updater = tf.assign(spike, True)        # Le asignamos el valor True a spike mediante tf.assign(...)
        updater.eval()                          # Evaluamos para actualizar el valor
    else:
        updater = tf.assign(spike, False)       # Le asignamos False, por si tenía asignado True anteriormente
        updater.eval()                          # Actualizamos el valor
    print("Spike: {}".format(spike.eval()))
    
sess.close()                                    # Recordar de cerrar la sesión

"""### Guardando y cargando variables

Claramente no queremos estar corriendo todo el código cada vez que queramos depurar nuestro programa. `TensorFlow` nos ofrece una manera de guardar variables para solo así tener que cargarlas desde un instante en específico. Para esto, utilizaremos otras maneras (más comunes) de inicializar variables: [`tf.get_variable(...)`](https://www.tensorflow.org/api_docs/python/tf/get_variable) y [`tf.global_variables_initializer()`](https://www.tensorflow.org/api_docs/python/tf/initializers/global_variables):
"""

# create graph
weights = tf.get_variable(name="W", shape=[2,3], initializer=tf.truncated_normal_initializer(stddev=0.01))
biases = tf.get_variable(name="b", shape=[3], initializer=tf.zeros_initializer())

# Inicializamos las variables mediante la siguiente operacion:
init_op = tf.global_variables_initializer()

# La operacion tf.train.Saver() nos va a permitir guardar y cargar variables
saver = tf.train.Saver()       

with tf.Session() as sess:
    # Corremos al inicializador de variables
    sess.run(init_op)
    # Corremos ahora las operaciones
    W, b = sess.run([weights, biases])
    print('weights = {}'.format(W))
    print('biases = {}'.format(b))

    # Guardamos a las variables en la memoria en el folder actual
    save_path = saver.save(sess, './wandb.ckpt')
    
print('Datos de las variables fueron guardados en el archivo: %s' % save_path)

"""Podemos imprimir las variables que hemos guardado, así como el `dtype`, `shape` y si es `tf.Variable`, etc.:"""

for i, var in enumerate(saver._var_list):
    print('Var {}: {}'.format(i, var))

"""Entonces, si corremos `!ls`, veremos que hemos generado cuatro archivos nuevos:"""

!ls

"""Los archivos `.ckpt` son archivos binarios que usaremos mediante la función `.restore()`:"""

# Borramos al grafo actual
tf.reset_default_graph()

# Creamos uno nuevo con las variables que teníamos
weights = tf.get_variable(name="W", shape=[2,3], initializer=tf.truncated_normal_initializer(stddev=0.01))
biases = tf.get_variable(name="b", shape=[3], initializer=tf.zeros_initializer())

# Inicializamos las variables
tf.global_variables_initializer()

# Creamos un objeto saver
saver = tf.train.Saver()

# Por si el grafo tiene un error
try:
    # Corremos la sesión
    with tf.Session() as sess:
        # Restoramos a las variables guardadas
        saver.restore(sess, './wandb.ckpt')
        # Imprimimos a las variables para confirmar que lo hemos hecho bien
        w_out, b_out = sess.run([weights, biases])
        print('w = ', w_out)
        print('b = ', b_out)
    
except Exception as e:
    print(str(e))

"""Nótese que los valores de las variables son aquellos que guardamos arriba.

## `TensorBoard`

Cuando estamos entrenando a nuestros algoritmos en Aprendizaje Automático, lo que más tiempo nos toma (aparte de la limpieza de datos) es esperar que los algoritmos convergan (i.e., que lleguen al nivel de error establecido o requerido). No hay nada peor que dejar que un algoritmo corra durante horas solo para que los resultados no tengan sentido. Imagine ahora que su algoritmo debe de correr durante días, inclusive semanas. ¿Esperaría hasta el final para saber si va por el camino correcto, o quisiera saber si sucede algo malo durante el entrenamiento?

Para ese fin crearon [`TensorBoard`](https://www.tensorflow.org/guide/summaries_and_tensorboard) que nos permite visualizar cómo cambian los distintos valores de los nodos de nuestro grafo, el error de entrenamiento, la pérdida, inclusive visualizar el grafo en sí. No es necesario instalarlo por aparte, ya que usualmente se instala al instalar `TensorFlow`.

![Pong-v0](https://user-images.githubusercontent.com/24496178/56482649-64223400-6482-11e9-9280-3b5e52f85717.PNG)
*Fig. 3: `Tensorboard` de un agente que aprende a jugar [`Pong-v0`](https://gym.openai.com/envs/Pong-v0/) usado en mi tésis de maestría.*

Debemos de crear un directorio que llamaremos `logs`:
"""

!mkdir logs

"""En una consola debemos de correr:

```
$ tensorboard --logdir=./logs
```

El cual nos dirá que debemos de abrir (si no es que se abre automáticamente) a `TensorBoard` en una pestaña mediante la dirección local `http://localhost:6006` (6006 = GOOGLE). Ahora, debemos de poblarlo con datos/logs.

### Implementando un suavizamiento exponencial

Vamos a usar a `TensorBoard` para visualizar un [suavizamiento exponencial](https://en.wikipedia.org/wiki/Exponential_smoothing). Éste es útil cuando se desea ver el precio promedio de una acción con sus valores en el tiempo dados por $x_1, \dots, x_n$, por ejemplo. Debido a que no se tienen todos los valores (ya que cada cierto tiempo se consigue un nuevo dato), no podemos calcular el promedio usual. Entonces, el algoritmo es el siguiente:

$$ \text{Avg}_{t} = f(\text{Avg}_{t-1}, x_t) = (1-\alpha) \text{Avg}_{t-1} + \alpha x_t, \alpha \in [0, 1] $$

Lo pondremos así en el código:

```python
>>> update_avg = alpha * curr_value + (1 - alpha) * prev_avg
```

Tendremos datos aleatorios que querremos conseguir el promedio:

```python
>>> raw_data = np.random.normal(10, 1, 100)
>>> with tf.Session() as sess:
...     for i in range(len(raw_data)):
...         currr_avg = sess.run(update_avg, feed_dict={curr_value: raw_data[i]})
...         sess.run(tf.assign(prev_avg, curr_avg))
```

Ahora solo nos queda definir a las variables con su respectivo código. Veamos qué vamos a producir:
"""

import numpy as np

# Borramos al grafo actual
tf.reset_default_graph()

# alpha nos indica qué tanto nos importan los valores nuevos agregados, o qué tanto no nos interesan los pasados
# Por supuesto, es una constante
alpha = tf.constant(0.05)

# El valor actual lo iremos creando conforme corramos la sesión
curr_val = tf.placeholder(dtype=tf.float32, shape=None)

# Inicializamos al promedio pasado como cero
prev_avg = tf.Variable(0.)
# Otra opcion seria: prev_avg = tf.get_variable("prev_avg", [1], tf.float32, initializer=tf.zeros_initializer)

# Nuestro algoritmo es:
update_avg = alpha * curr_val + (1 - alpha) * prev_avg

# Para reproducir los resultados
np.random.seed(42)
# Creamos un  vector aleatorio de 100 números con un promedio de 10 y desviación estándar 1
raw_data = np.random.normal(10, 1, 100)

# Inicializamos a nuestras variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    
    for i in range(len(raw_data)):
        curr_avg = sess.run(update_avg, feed_dict={curr_val: raw_data[i]})
        sess.run(tf.assign(prev_avg, curr_avg))
        print(raw_data[i], curr_avg)

"""Queremos ahora visualizar a estos datos, específicamente en `TensorBoard`. Entonces, debemos de realizar algunas modificaciones:"""

# Borramos al grafo actual
tf.reset_default_graph()

alpha = tf.constant(0.05)
curr_val = tf.placeholder(dtype=tf.float32, shape=None)
prev_avg = tf.Variable(0.)
update_avg = alpha * curr_val + (1 - alpha) * prev_avg

# Para reproducir los resultados
np.random.seed(42)
raw_data = np.random.normal(10, 1, 100)

# Cramos un nodo de resumen (summary) para los promedios
avg_hist = tf.summary.scalar("suav_exp", update_avg)

# Creamos un nodo de resumen para los valores actuales
value_hist = tf.summary.scalar("valor_entrante", curr_val)

# Fusionamos a los nodos de resumen para poder manejarlos mas facilmente
merged = tf.summary.merge_all()

# Le pasamos al escritor (writer) la direccion de los logs
writer = tf.summary.FileWriter("./logs")

# Inicializamos a nuestras variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    # Podemos visualizar el grafo computacional en TensorBoard agregando este comando:
    writer.add_graph(sess.graph)
    
    for i in range(len(raw_data)):
        
        summary_str, curr_avg = sess.run([merged, update_avg], feed_dict={curr_val: raw_data[i]})
        
        sess.run(tf.assign(prev_avg, curr_avg))
        # Podríamos obviar imprimor los valores aquí, pero lo hacemos solo para recordar los resultados
        print(raw_data[i], curr_avg)
        
        # Agregamos el resumen al escritor
        writer.add_summary(summary_str, i)

"""Regresando a `TensorBoard`, debería de obtener lo siguiente en el tab de `SCALARS`:

![TB exp average](https://user-images.githubusercontent.com/24496178/56703870-1f87da00-66c8-11e9-9455-8a4f46409640.png)
*Fig. 4: Podemos ver que el suavizamiento exponencial se acerca a `10.`.*

Observamos que, gracias a la [Ley de los grandes números](https://en.wikipedia.org/wiki/Law_of_large_numbers), `suav_exp` tiende a `10.`, ya que ese fue el valor de la media que le dimos a los números aleatorios generados (`raw_data`). 

En el tab de `GRAPHS` tendremos a nuestro grafo computacional:

![Grafo](https://user-images.githubusercontent.com/24496178/56703596-da16dd00-66c6-11e9-942a-bcf516dba1fd.png)
*Fig. 5: Grafo de nuestra operación. Trate de entender todo lo que sucede aquí.*

Para correr `Tensorboard` en `Colab`, las instrucciones son un poco más complejas; debemos de utilizar [`Ngrok`](https://ngrok.com/), por lo que es aconsejable que se sigan [estas instrucciones](https://www.dlology.com/blog/quick-guide-to-run-tensorboard-in-google-colab/).

En conclusión, `TensorBoard` es una herramienta muy útil, tanto para visualizar nuestro grafo computacional, como para visualizar si en efecto nuestro algoritmo está convergiendo. Recuerde que ahora las operaciones matemáticas son nodos y los datos fluyen a través de éstos. Éste punto clave nos servirá a la hora de definir nuestras redes neuronales.

***

**Ejercicio 2:** Consiga el grafo en `TensorBoard` de una operación sencilla: la suma de dos tensores constantes. Acostumbre su ojo a éste tipo de grafos computacionales.
"""

!wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
!unzip ngrok-stable-linux-amd64.zip

LOG_DIR = './log'
get_ipython().system_raw(
    'tensorboard --logdir {} --host 0.0.0.0 --port 6006 &'
    .format(LOG_DIR)
)

get_ipython().system_raw('./ngrok http 6006 &')

! curl -s http://localhost:4040/api/tunnels | python3 -c \
    "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"

a = 2
b = 3
c = tf.add(a, b, name='Add')
print(c)

sess = tf.Session()
print(sess.run(c))
sess.close()

with tf.Session() as sess:
    print(sess.run(c))

"""***

**Ejercicio 3:** Ahora, consiga el grafo en `TensorBoard`  de la operación de la distribución Normal que obtuvimos en el Ejercicio 1. ¿Cómo se compara con el que teníamos en la Figura 1?
"""

k = tf.placeholder(tf.float32)

mean_moving_normal = tf.random_normal(shape=[1000], mean=(5*k), stddev=1)
tf.summary.histogram("normal/moving_mean", mean_moving_normal)

sess = tf.Session()
writer = tf.summary.FileWriter("/tmp/histogram_example")

summaries = tf.summary.merge_all()

N = 400
for step in range(N):
  k_val = step/float(N)
  summ = sess.run(summaries, feed_dict={k: k_val})
  writer.add_summary(summ, global_step=step)
  
tensorboard --logdir=/tmp/histogram_example