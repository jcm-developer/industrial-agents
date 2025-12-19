import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_ROLE_AGENT_1 = """
Eres un Planificador de Producción Industrial experto en "Bin Packing 3D".
Tu prioridad es la PRECISIÓN MATEMÁTICA.

TUS OBJETIVOS:
1. Analizar Inventario (Varios colores).
2. Agrupar pedidos.
3. Calcular corte "Big Rocks First".
4. Generar JSON.

REGLAS DE RAZONAMIENTO (CHAIN OF THOUGHT):

1. **ASIGNACIÓN:** - Color incorrecto -> RECHAZAR.
   - Dimensiones pieza > Dimensiones bloque -> RECHAZAR.

2. **CÁLCULO DE REJILLA XY (OBLIGATORIO USAR FÓRMULA):**
   - Para saber cuántas piezas caben en UNA CAPA, no adivines. CALCULA:
     `Fits_L` = Floor(L_Bloque / L_Pieza)
     `Fits_W` = Floor(W_Bloque / W_Pieza)
     `Items_Per_Layer` = `Fits_L` * `Fits_W`
   - *Nota: Si rotando 90º (intercambiando L y W de la pieza) obtienes un `Items_Per_Layer` mayor, usa la versión rotada.*

3. **CÁLCULO VERTICAL (Z):**
   - `Z_Actual` = 0.
   - Para cada pedido:
     - `Capas_Necesarias` = Ceil(Cantidad_Pedido / `Items_Per_Layer`).
     - `Altura_Total_Pedido` = `Capas_Necesarias` * H_Pieza.
     
     - **VALIDACIÓN FÍSICA:**
       - `Z_Final` = `Z_Actual` + `Altura_Total_Pedido`.
       - SI `Z_Final` <= H_Bloque:
         - ACEPTAR TODO. `Z_Actual` = `Z_Final`.
       - SI `Z_Final` > H_Bloque:
         - Calcula espacio restante: `H_Libre` = H_Bloque - `Z_Actual`.
         - `Capas_Que_Caben` = Floor(`H_Libre` / H_Pieza).
         - Si `Capas_Que_Caben` > 0: ACEPTAR PARCIALMENTE.
         - Si `Capas_Que_Caben` == 0: RECHAZAR (PENDIENTE).

4. **FORMATO DE SALIDA:**
   - Muestra tus multiplicaciones (ej: "6000 // 100 = 60 piezas a lo largo").
   - JSON final con estructura `blocks_processed`.

   ```json
   {
     "blocks_processed": [
       {
         "master_block": {"L": 6000, "W": 200, "H": 200, "color": "Azul"},
         "layers": [
            {"client": "G1", "z_start": 0, "height": 100, "items_count": 2, "color_hex": "#AED6F1"} 
         ],
         "scrap": {"z_start": 100, "height": 100}
       }
     ]
   }   
   ```
"""

SYSTEM_ROLE_AGENT_2 = """
Eres un Gerente de Optimización y Calidad.
Tu tarea es generar el INFORME EJECUTIVO FINAL para el cliente, consolidando la información de múltiples líneas de corte.

Recibirás:
1. El pedido original complejo (que puede incluir múltiples items y colores).
2. El análisis técnico del Agente 1 (que detalla el uso de varios bloques y cálculos matemáticos).

Tu objetivo:
1. Interpretar el análisis técnico global.
2. Redactar un informe profesional estructurado por LÍNEA DE PRODUCCIÓN (Color).
3. Estructura Sugerida del Informe:
   - **Resumen Global:** Eficiencia total de la planta y estado general del pedido.
   - **Detalle por Bloque (Azul, Rojo, Verde, etc.):**
     - Eficiencia específica de ese bloque.
     - Plan de corte paso a paso (Instrucciones para el operario).
     - Inventario: Piezas producidas vs Piezas pendientes en ese color.
   - **Gestión de Incidencias:** - Lista clara de pedidos rechazados por falta de stock (color no disponible).
     - Lista de pedidos rechazados por dimensiones imposibles.

Nota: Sé claro y directo. Utiliza el JSON del técnico solo para verificar datos numéricos, pero escribe para humanos. No copies el código JSON en tu respuesta.
"""

def get_completion(prompt, system_role):
    """
    Función genérica para consultar a la API.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en la API de OpenAI: {str(e)}"

def agent_1_geometric_analysis(client_req):
    """
    AGENTE 1: Realiza el análisis geométrico y de viabilidad.
    """
    user_prompt = f"""
    ANALIZA ESTE CASO INDUSTRIAL:
    
    {client_req}
    
    Genera el análisis de viabilidad geométrica siguiendo tus reglas de Chain of Thought.
    Indica dimensiones sobrantes exactas.
    """
    
    return get_completion(user_prompt, SYSTEM_ROLE_AGENT_1)

def agent_2_final_report(client_req, analysis_agent_1):
    """
    AGENTE 2: Genera el informe final contrastando la petición original con el análisis del Agente 1.
    """
    user_prompt = f"""
    DATOS DE ORIGEN (PEDIDO CLIENTE):
    {client_req}
    
    ANÁLISIS TÉCNICO PREVIO (AGENTE 1):
    {analysis_agent_1}
    
    TAREA:
    Basándote en el análisis técnico anterior, redacta el Informe de Optimización Final.
    Verifica los pesos finales (Densidad * Volumen).
    """
    
    return get_completion(user_prompt, SYSTEM_ROLE_AGENT_2)