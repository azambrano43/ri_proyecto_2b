# **Sistema RAG (Retrieval-Augmented Generation)**

# **Integrantes:**
- Andrade Dilan
- Calahorrano David
- Zambrano Andrés

## **Descripción**
Este proyecto implementa un sistema RAG que combina técnicas de **Recuperación de Información (RI)** con **Modelos de Generación de Texto** para responder consultas basadas en documentos relevantes.

El sistema permite:
- Recuperar documentos relevantes desde una base de datos vectorial utilizando **ChromaDB**.
- Generar respuestas utilizando el modelo **T5 (Flan-T5-Large)**.
- Consultar información a través de una **API en Flask** o desde una **interfaz web**.
- Evaluar la calidad de la recuperación y generación de respuestas con métricas como **Precision@k, Recall, F1-Score, BLEU y ROUGE-L**.

---

## **Requisitos Previos**
Antes de ejecutar el sistema, asegúrate de cumplir con los siguientes requisitos:

- **Python 3.8 o superior**.
- Tener instaladas las siguientes librerías de Python:
  - `transformers`
  - `torch`
  - `chromadb`
  - `nltk`
  - `flask`
  - `flask-cors`
  - `rouge`

Para instalar las dependencias, ejecuta:

```bash
pip install transformers torch chromadb nltk flask flask-cors rouge
```

---

## **Instrucciones para Ejecutar el Sistema**

### **1. Preparar la Base de Datos**
Ejecuta el preprocesamiento del corpus y la creación de la base de datos vectorial:

```bash
python preprocessing.py
python database.py
```

Estos scripts procesarán los documentos, generarán embeddings y los almacenarán en **ChromaDB**.

---

### **2. Iniciar la API del Sistema**
Para ejecutar la API en Flask y permitir que el sistema procese consultas, ejecuta:

```bash
python app.py
```

Si la API se inicia correctamente, verás un mensaje como:

```
 * Running on http://127.0.0.1:5000/
```

---

### **3. Realizar Consultas al Sistema**
Puedes interactuar con el sistema mediante herramientas desde la **interfaz web**.


#### **Consulta desde el Navegador**
Si tienes una interfaz web implementada, accede a:

```
http://127.0.0.1:5000/
```

Ingresa una consulta y el sistema responderá con información generada.

---

### **4. Evaluar el Rendimiento del Sistema**
Para calcular las métricas de evaluación (Precision, Recall, BLEU Score, ROUGE-L), ejecuta:

```bash
python calcular_metricas.py
```

Este script generará un informe con los valores obtenidos en la evaluación del sistema.

---

### **5. Detener el Sistema**
Para detener la API, presiona **Ctrl + C** en la terminal donde se ejecuta `app.py`.

---

## **Estructura del Proyecto**

```
📂 ri_proyecto_2b
 ├── data/                 # Archivos de datos y corpus
 ├── db/                   # Archivos de base de datos
 ├── db_muestra/           # Datos de muestra para pruebas
 ├── documentation/        # Documentación del proyecto
 ├── notebooks/            # Notebooks para pruebas y análisis
 ├── src/                  # Código fuente del proyecto
 │   ├── static/           # Archivos estáticos (CSS, JS)
 │   ├── templates/        # Plantillas HTML para la interfaz web
 │   │   ├── index.html    # Página principal
 │   ├── app.py            # API en Flask
 │   ├── calcular.py       # Cálculo de métricas
 │   ├── database.py       # Manejo de base de datos en ChromaDB
 │   ├── datos_prueba.py   # Datos de prueba para evaluación
 │   ├── main.py           # Script principal
 │   ├── model.py          # Modelo de generación con T5 (Flan-T5-Large)
 │   ├── preprocessing.py  # Preprocesamiento del corpus
 │   ├── resultModeloG.py  # Evaluación de generación
 ├── .gitignore            # Archivos ignorados en Git
 ├── README.md             # Documentación principal del proyecto
 ├── requirements.txt      # Dependencias del proyecto
```