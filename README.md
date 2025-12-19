# 🏭 Industrial Optimizer: Multi-Block System

Sistema inteligente de optimización industrial para gestión de inventarios complejos y cálculo de líneas de corte utilizando Inteligencia Artificial.

## 📋 Descripción

**Industrial Optimizer** es una aplicación web construida con Streamlit que utiliza agentes de IA (GPT-4o-mini) para resolver problemas de optimización tipo "Bin Packing 3D". El sistema analiza inventarios de bloques de material y calcula los puntos de corte óptimos para satisfacer pedidos de clientes, minimizando el desperdicio.

### Características principales

- 🤖 **Sistema Multi-Agente**: Dos agentes especializados colaboran para análisis técnico e informes ejecutivos
- 📐 **Análisis Geométrico**: Cálculo preciso usando algoritmos "Big Rocks First" para optimización de corte
- 📊 **Visualización Gráfica**: Representación visual de los planos de corte por bloque
- 💾 **Persistencia**: Historial de predicciones almacenado en SQLite
- 🎨 **Soporte Multi-Color**: Gestión de múltiples líneas de producción (Azul, Rojo, Verde, etc.)

## 🏗️ Arquitectura

```
industrial/
├── cuts/
│   ├── app.py          # Aplicación principal Streamlit
│   ├── agents.py       # Agentes de IA (Técnico + Gerente)
│   ├── database.py     # Módulo de persistencia SQLite
│   └── .env            # Variables de entorno (API Key)
├── requirements.txt    # Dependencias del proyecto
└── industrial_predictions.db  # Base de datos SQLite
```

### Agentes de IA

| Agente | Rol | Función |
|--------|-----|---------|
| **Agente 1 - Planificador Técnico** | Análisis Geométrico | Calcula rejillas XY, valida dimensiones, genera JSON estructurado con capas y scrap |
| **Agente 2 - Gerente de Optimización** | Informe Ejecutivo | Consolida resultados, genera instrucciones para operarios, gestiona incidencias |

## 🚀 Instalación

### Prerrequisitos

- Python 3.8+
- Una API Key de OpenAI

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd industrial
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear archivo `.env` en la carpeta `cuts/`:
   ```env
   OPENAI_API_KEY=tu_api_key_aqui
   ```

## ▶️ Uso

1. **Ejecutar la aplicación**
   ```bash
   cd cuts
   streamlit run app.py
   ```

2. **Acceder a la interfaz**
   
   Abrir en el navegador: `http://localhost:8501`

3. **Ingresar una descripción del problema industrial**
   
   Ejemplo de entrada:
   ```
   INVENTARIO:
   - Bloque Azul: 6000mm x 200mm x 200mm
   - Bloque Rojo: 4000mm x 150mm x 150mm
   
   PEDIDOS:
   - Cliente A: 50 piezas azules de 100mm x 50mm x 20mm
   - Cliente B: 30 piezas rojas de 80mm x 40mm x 15mm
   ```

4. **Ver resultados**
   - Análisis técnico detallado con razonamiento Chain-of-Thought
   - Informe ejecutivo para gestión
   - Visualización gráfica de los planos de corte

## 📦 Dependencias

| Paquete | Uso |
|---------|-----|
| `streamlit` | Framework de interfaz web |
| `openai` | Cliente API de OpenAI |
| `pandas` | Manejo de datos tabulares |
| `python-dotenv` | Gestión de variables de entorno |
| `matplotlib` | Generación de gráficos |

## 🗄️ Base de Datos

El sistema utiliza SQLite para persistir el historial de predicciones:

```sql
CREATE TABLE industrial_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    client_req TEXT,           -- Descripción del pedido
    first_review TEXT,         -- Análisis del Agente 1
    second_review TEXT         -- Informe del Agente 2
);
```

## 🔧 Configuración Avanzada

### Cambiar modelo de IA

En `agents.py`, modificar la línea:
```python
model="gpt-4o-mini"  # Cambiar a "gpt-4o" para mayor precisión
```

### Ajustar temperatura

```python
temperature=0.2  # 0.0 = más determinista, 1.0 = más creativo
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de enviar un PR.

---

**Desarrollado con ❤️ utilizando Streamlit + OpenAI**
