import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import re
import database as db
import agents as ag

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Industrial Optimizer",
    layout="wide",
    page_icon="🏭",
    initial_sidebar_state="expanded"
)

# --- INICIALIZACIÓN ---
try:
    db.init_db()
except Exception as e:
    st.error(f"⚠️ Error DB: {e}")

# Variables de Sesión
if "technical_result" not in st.session_state:
    st.session_state.technical_result = None
if "json_data" not in st.session_state: 
    st.session_state.json_data = None
if "final_report" not in st.session_state:
    st.session_state.final_report = None

# --- FUNCIONES AUXILIARES (PARSING Y DIBUJO DINÁMICO) ---

def extract_json_from_text(text):
    """Extrae el JSON estructurado del texto del agente."""
    try:
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        match_raw = re.search(r"\{.*\}", text, re.DOTALL)
        if match_raw:
            return json.loads(match_raw.group(0))
        return None
    except:
        return None

def draw_single_block(block_data, index):
    """Dibuja un solo bloque basado en datos JSON."""
    try:
        master = block_data.get("master_block", {})
        layers = block_data.get("layers", [])
        scrap = block_data.get("scrap", {})

        L_total = master.get("L", 200)
        H_total = master.get("H", 100)
        color_name = master.get("color", "Bloque")

        fig, ax = plt.subplots(figsize=(10, 5))
        
        # 1. Contorno Maestro
        ax.add_patch(patches.Rectangle((0, 0), L_total, H_total, linewidth=3, edgecolor='black', facecolor='none', label=f'{color_name} ({L_total}x{H_total})'))

        # 2. Capas
        colors = ['#AED6F1', '#5DADE2', '#3498DB', '#2E86C1'] # Azules por defecto
        # Si es rojo, cambiamos paleta (simple logic)
        if "Rojo" in color_name: colors = ['#F5B7B1', '#E74C3C', '#C0392B']
        if "Verde" in color_name: colors = ['#A9DFBF', '#27AE60', '#196F3D']

        for i, layer in enumerate(layers):
            z_start = layer.get("z_start", 0)
            h_layer = layer.get("height", 0)
            client = layer.get("client", "?")
            count = layer.get("items_count", 0)
            
            c = colors[i % len(colors)]
            ax.add_patch(patches.Rectangle((0, z_start), L_total, h_layer, linewidth=1, edgecolor='white', facecolor=c, alpha=0.9))
            ax.text(L_total/2, z_start + h_layer/2, f"Cliente {client} ({count} items)", ha='center', va='center', fontsize=9, fontweight='bold')

        # 3. Scrap
        if scrap:
            z_s = scrap.get("z_start", 0)
            h_s = scrap.get("height", 0)
            if h_s > 0:
                ax.add_patch(patches.Rectangle((0, z_s), L_total, h_s, linewidth=1, edgecolor='red', facecolor='#FADBD8', hatch='xx', label='Scrap'))
                ax.text(L_total/2, z_s + h_s/2, f'LIBRE ({h_s} cm)', ha='center', va='center', color='#922B21', fontsize=8)

        ax.set_xlim(- (L_total*0.05), L_total*1.05)
        ax.set_ylim(- (H_total*0.05), H_total*1.1)
        ax.set_title(f"Bloque #{index+1}: {color_name}")
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.close(fig)
        return fig
    except:
        return None

# --- UI PRINCIPAL ---
st.title("🏭 Industrial Optimizer: Multi-Block System")
st.markdown("Sistema inteligente para gestión de inventarios complejos y múltiples líneas de corte.")

with st.sidebar:
    st.header("📝 Entrada")
    
    user_input = st.text_area("Descripción:", height=300)
    
    if st.button("✂️ Calcular puntos de corte", type="primary"):
        if user_input.strip():
            # Reset
            st.session_state.technical_result = None
            st.session_state.json_data = None
            st.session_state.final_report = None
            
            try:
                with st.status("⚙️ Procesando Planta...", expanded=True) as status:
                    # 1. Agente Técnico
                    st.write("Analizando inventario y pedidos...")
                    resp_1 = ag.agent_1_geometric_analysis(user_input)
                    st.session_state.technical_result = resp_1
                    
                    # Extraer datos JSON para gráficas
                    st.write("Generando planos de corte...")
                    json_data = extract_json_from_text(resp_1)
                    st.session_state.json_data = json_data # Guardamos el objeto completo
                    
                    # 2. Agente Gerente
                    st.write("Redactando informe consolidado...")
                    resp_2 = ag.agent_2_final_report(user_input, resp_1)
                    st.session_state.final_report = resp_2
                    
                    # Guardar DB
                    db.save_prediction(user_input, resp_1, resp_2)
                    status.update(label="¡Completado!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"Error: {e}")

# --- RESULTADOS ---
if st.session_state.technical_result and st.session_state.final_report:
    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📐 Análisis Técnico")
        with st.expander("Ver razonamiento detallado"):
            st.markdown(st.session_state.technical_result)
            
    with c2:
        st.subheader("📑 Informe Ejecutivo")
        st.info(st.session_state.final_report)
    
    # --- SECCIÓN GRÁFICA MULTI-BLOQUE ---
    st.divider()
    st.subheader("📊 Planos de Corte por Bloque")
    
    if st.session_state.json_data and "blocks_processed" in st.session_state.json_data:
        blocks = st.session_state.json_data["blocks_processed"]
        
        # Iteramos y dibujamos CADA bloque devuelto por el agente
        for idx, block in enumerate(blocks):
            fig = draw_single_block(block, idx)
            if fig:
                st.pyplot(fig)
    else:
        st.warning("No se pudieron generar gráficos. El agente no devolvió datos estructurados válidos.")

# --- HISTORIAL ---
st.divider()
try:
    h = db.get_history()
    if not h.empty: st.dataframe(h, use_container_width=True)
except: pass