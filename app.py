import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat
import datetime

# Configuración de página
st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyectar CSS personalizado
st.markdown("""
<style>
    /* Estilos generales */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4CAF50;
        margin-bottom: 1rem;
    }
    
    .menu-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .menu-card:hover {
        transform: translateY(-5px);
    }
    
    .habit-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Navegación mejorada */
    .stRadio > div {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    .stRadio > div[role="radiogroup"] > label {
        flex: 1;
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stRadio > div[role="radiogroup"] > label:hover {
        border-color: #667eea;
        background: #fff;
    }
    
    .stRadio > div[role="radiogroup"] > label[data-testid="stRadio"] > div:first-child {
        padding: 0;
    }
    
    /* Badges para hábitos */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-success {
        background: #d4edda;
        color: #155724;
    }
    
    .badge-warning {
        background: #fff3cd;
        color: #856404;
    }
    
    .badge-info {
        background: #d1ecf1;
        color: #0c5460;
    }
    
    /* Estilos para tablas */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 1rem;
    }
    
    .dataframe td {
        padding: 0.8rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    /* Tarjeta de usuario */
    .user-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .user-card i {
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 2.5rem;">🥗 NutriGen AI</h1>
    <p style="margin:0; opacity: 0.9; font-size: 1.1rem;">Tu asistente nutricional inteligente • Personaliza tu salud</p>
</div>
""", unsafe_allow_html=True)

# Estado de sesión
if "logged" not in st.session_state:
    st.session_state.logged = False

# ---------- PÁGINA DE LOGIN ----------
if not st.session_state.logged:
    # Usar columnas con proporción diferente
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 👋 Bienvenido/a")
        st.markdown("""
        <div class="menu-card">
            <h4 style="margin-top:0;">✨ Beneficios de NutriGen AI:</h4>
            <ul style="padding-left: 1.2rem;">
                <li>📋 Planes nutricionales personalizados</li>
                <li>🤖 Asistente con IA avanzada</li>
                <li>📈 Seguimiento de hábitos</li>
                <li>🍎 Base de datos nutricional</li>
                <li>🔔 Recordatorios inteligentes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        login_form()
    
    with col2:
        st.markdown("### 🚀 Comienza tu viaje saludable")
        st.markdown("""
        <div class="menu-card">
            <h4 style="margin-top:0;">📊 Lo que lograrás:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 1rem 0;">
                <span class="badge badge-success">+ Energía</span>
                <span class="badge badge-warning">- Peso</span>
                <span class="badge badge-info">+ Bienestar</span>
                <span class="badge badge-success">+ Concentración</span>
                <span class="badge badge-info">+ Salud</span>
            </div>
            <p>Regístrate gratis y obtén acceso completo a todas las funcionalidades.</p>
        </div>
        """, unsafe_allow_html=True)
        
        register_form()
    
    # Footer de login
    st.markdown("---")
    st.caption("🔒 Tus datos están seguros y protegidos • 💡 Basado en ciencia nutricional")
    st.stop()

# ---------- USUARIO LOGUEADO ----------
# Header con información de usuario
user_col1, user_col2 = st.columns([3, 1])
with user_col1:
    st.markdown(f"""
    <div class="user-card">
        <div style="font-size: 2rem;">👤</div>
        <div>
            <h3 style="margin:0;">¡Hola, {st.session_state.user.email.split('@')[0]}!</h3>
            <p style="margin:0; opacity: 0.9;">Listo para tu día saludable</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
with user_col2:
    if st.button("🚪 **Cerrar sesión**", use_container_width=True):
        logout()

st.divider()

# ---------- NAVEGACIÓN MEJORADA ----------
st.markdown("### 📍 Navegación")
page = st.radio(
    "Selecciona una sección:",
    ["🥗 Menús saludables", "🤖 Asistente IA", "💡 Hábitos saludables", "📊 Mi progreso"],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# ================= MENÚS SALUDABLES =================
if page == "🥗 Menús saludables":
    st.header("🍽️ Planificador de Menús")
    
    # Selector de objetivos
    objetivo = st.selectbox(
        "🎯 Selecciona tu objetivo:",
        ["🏃‍♂️ Ganar energía y vitalidad", "🔥 Pérdida de peso saludable", 
         "💪 Ganar masa muscular", "🧘‍♀️ Mantenimiento y bienestar", "🌱 Dieta vegetariana"]
    )
    
    # Información nutricional
    with st.expander("📊 Información nutricional del menú", expanded=True):
        col_cal, col_pro, col_car, col_gras = st.columns(4)
        with col_cal:
            st.metric("🔥 Calorías", "2,100 kcal", "±100")
        with col_pro:
            st.metric("💪 Proteínas", "85g", "15%")
        with col_car:
            st.metric("⚡ Carbohidratos", "280g", "55%")
        with col_gras:
            st.metric("🥑 Grasas", "65g", "30%")
    
    # Menús detallados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        st.subheader("🌅 Desayuno")
        
        if "energía" in objetivo:
            st.markdown("""
            **Energía matutina:**
            - 🥣 **Avena integral** con plátano y miel (50g avena, 1 plátano, 1 cda miel)
            - 🥛 **Batido verde** (espinacas, piña, jengibre)
            - ☕ Té verde o café sin azúcar
            
            ⏰ **Hora ideal:** 7:00 - 8:00 AM
            """)
        elif "peso" in objetivo:
            st.markdown("""
            **Desayuno ligero:**
            - 🥚 **Tortilla** (2 claras + 1 huevo entero)
            - 🥑 **Aguacate** (¼ unidad)
            - 🍞 **Pan integral** (1 rebanada)
            - 🍵 Té de canela
            
            ⏰ **Hora ideal:** 7:00 - 8:00 AM
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        st.subheader("🌞 Almuerzo")
        
        if "energía" in objetivo:
            st.markdown("""
            **Comida energética:**
            - 🍗 **Pechuga de pollo** a la plancha (150g)
            - 🍚 **Quinoa** con vegetales (1 taza)
            - 🥗 **Ensalada mixta** (lechuga, tomate, pepino)
            - 🍎 1 manzana de postre
            
            ⏰ **Hora ideal:** 13:00 - 14:00 PM
            """)
        elif "peso" in objetivo:
            st.markdown("""
            **Comida equilibrada:**
            - 🐟 **Salmón** al horno (120g)
            - 🥦 **Brócoli** y coliflor al vapor
            - 🥔 **Batata** asada (100g)
            - 🍓 Fresas naturales
            
            ⏰ **Hora ideal:** 13:00 - 14:00 PM
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        st.subheader("🌙 Cena")
        
        if "energía" in objetivo:
            st.markdown("""
            **Cena ligera:**
            - 🍤 **Camarones** salteados (100g)
            - 🥬 **Espárragos** a la plancha
            - 🍠 **Puré de calabaza**
            - 🥛 Vaso de leche de almendras
            
            ⏰ **Hora ideal:** 20:00 - 21:00 PM
            """)
        elif "peso" in objetivo:
            st.markdown("""
            **Cena super ligera:**
            - 🍲 **Sopa de verduras** (calabacín, zanahoria, apio)
            - 🐟 **Filete de merluza** al vapor (100g)
            - 🥒 **Pepino** y rábanos
            - 🍵 Infusión digestiva
            
            ⏰ **Hora ideal:** 19:30 - 20:30 PM
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Meriendas
    st.subheader("🍎 Meriendas recomendadas")
    snack_col1, snack_col2, snack_col3 = st.columns(3)
    
    with snack_col1:
        st.markdown('<div class="habit-card">', unsafe_allow_html=True)
        st.markdown("**🥜 Media mañana:**")
        st.markdown("- 1 puñado de almendras (10-12 unidades)")
        st.markdown("- 1 yogur natural sin azúcar")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with snack_col2:
        st.markdown('<div class="habit-card">', unsafe_allow_html=True)
        st.markdown("**🍌 Media tarde:**")
        st.markdown("- Batido de proteínas")
        st.markdown("- 1 plátano pequeño")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with snack_col3:
        st.markdown('<div class="habit-card">', unsafe_allow_html=True)
        st.markdown("**🌰 Antes de dormir:**")
        st.markdown("- 1 vaso de leche caliente")
        st.markdown("- 3-4 nueces")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Lista de compras
    with st.expander("🛒 Lista de compras semanal"):
        st.markdown("""
        **Frutas y Verduras:**
        - 🍌 Plátanos (6 unidades)
        - 🍎 Manzanas (4 unidades)
        - 🥑 Aguacates (3 unidades)
        - 🥦 Brócoli (2 unidades)
        - 🥬 Espinacas (200g)
        - 🍅 Tomates (4 unidades)
        
        **Proteínas:**
        - 🍗 Pechuga de pollo (500g)
        - 🐟 Salmón (300g)
        - 🥚 Huevos (12 unidades)
        - 🥛 Yogur natural (4 unidades)
        
        **Carbohidratos:**
        - 🥣 Avena integral (500g)
        - 🍚 Quinoa (250g)
        - 🍠 Batatas (3 unidades)
        
        **Otros:**
        - 🥜 Almendras (200g)
        - 🌰 Nueces (150g)
        - 🍯 Miel natural
        """)
    
    # Botón para guardar menú
    if st.button("💾 Guardar este menú en mi perfil", use_container_width=True):
        st.success("✅ Menú guardado correctamente en tu perfil")

# ================= ASISTENTE IA =================
elif page == "🤖 Asistente IA":
    st.header("🤖 NutriGen Assistant")
    
    # Introducción
    st.markdown("""
    <div class="menu-card">
        <h4 style="margin-top:0;">✨ Genera planes personalizados con IA</h4>
        <p>Describe tus objetivos, restricciones alimentarias, preferencias y nivel de actividad. 
        Nuestra IA creará un plan nutricional adaptado exclusivamente para ti.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario estructurado
    with st.form("assistant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            objetivos = st.multiselect(
                "🎯 Objetivos principales:",
                ["Pérdida de peso", "Ganar masa muscular", "Más energía", 
                 "Mejorar digestión", "Controlar colesterol", "Deporte"]
            )
            
            alergias = st.multiselect(
                "⚠️ Alergias o intolerancias:",
                ["Lácteos", "Gluten", "Frutos secos", "Mariscos", "Huevos", "Soja", "Ninguna"]
            )
            
            actividad = st.select_slider(
                "🏃 Nivel de actividad física:",
                options=["Sedentario", "Ligero", "Moderado", "Activo", "Muy activo"]
            )
        
        with col2:
            preferencias = st.multiselect(
                "❤️ Preferencias alimentarias:",
                ["Vegetariano", "Pescetariano", "Vegano", "Sin azúcar", 
                 "Bajo en carbohidratos", "Alta proteína", "Comida rápida saludable"]
            )
            
            comidas_dia = st.slider("🍽️ Número de comidas al día:", 3, 6, 4)
            
            presupuesto = st.select_slider(
                "💰 Presupuesto semanal:",
                options=["Económico", "Moderado", "Flexible", "Premium"]
            )
        
        # Campo de texto libre
        prompt = st.text_area(
            "📝 Describe tu situación en detalle:",
            height=150,
            placeholder="Ejemplo: Soy una persona de 30 años que trabaja en oficina, quiero perder 5kg en 2 meses. Me gusta cocinar pero tengo poco tiempo entre semana. Necesito ideas de comidas rápidas y saludables. No como carne roja..."
        )
        
        submitted = st.form_submit_button("🚀 Generar plan nutricional personalizado")
    
    if submitted:
        if not prompt.strip():
            st.warning("⚠️ Por favor, describe tu situación para generar un plan personalizado.")
        else:
            # Construir prompt estructurado
            structured_prompt = f"""
            Crea un plan nutricional detallado con esta información:
            
            OBJETIVOS: {', '.join(objetivos) if objetivos else 'No especificado'}
            ALERGIAS: {', '.join(alergias) if alergias else 'Ninguna'}
            ACTIVIDAD: {actividad}
            PREFERENCIAS: {', '.join(preferencias) if preferencias else 'Sin preferencias específicas'}
            COMIDAS/DÍA: {comidas_dia}
            PRESUPUESTO: {presupuesto}
            
            CONTEXTO DEL USUARIO:
            {prompt}
            
            Por favor, genera un plan que incluya:
            1. Distribución calórica diaria
            2. Menú semanal detallado
            3. Lista de compras organizada
            4. Consejos específicos para los objetivos
            5. Recetas rápidas y fáciles
            6. Estrategias para mantener la motivación
            
            Formatea la respuesta con encabezados claros y emojis relevantes.
            """
            
            with st.spinner("🧠 Analizando tu perfil y generando plan personalizado..."):
                respuesta = gemini_chat(structured_prompt)
            
            # Mostrar resultado
            st.success("✅ ¡Plan generado con éxito!")
            
            # Dividir respuesta en secciones
            st.markdown("---")
            st.markdown("### 📋 Tu Plan Nutricional Personalizado")
            
            # Contenedor con estilo
            st.markdown('<div class="menu-card">', unsafe_allow_html=True)
            st.markdown(respuesta)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Opciones adicionales
            col_save, col_share, col_download = st.columns(3)
            with col_save:
                if st.button("💾 Guardar plan", use_container_width=True):
                    st.success("Plan guardado en tu historial")
            with col_share:
                if st.button("📤 Exportar PDF", use_container_width=True):
                    st.info("Funcionalidad de exportación en desarrollo")
            with col_download:
                if st.button("🛒 Generar lista de compras", use_container_width=True):
                    st.info("Lista generada en la sección de menús")

# ================= HÁBITOS SALUDABLES =================
elif page == "💡 Hábitos saludables":
    st.header("🌱 Tu Camino hacia una Vida Más Saludable")
    
    # Introducción
    st.markdown("""
    <div class="menu-card">
        <h4 style="margin-top:0;">✨ La ciencia de los hábitos</h4>
        <p>Los pequeños cambios consistentes son más poderosos que las grandes transformaciones ocasionales. 
        Aquí te guiamos para construir hábitos que perduren.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    st.subheader("📊 Tu Panel de Salud")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        pasos = st.slider("🚶 Pasos hoy:", 0, 20000, 8500, 100)
        st.progress(min(pasos/10000, 1.0))
        st.caption(f"Meta: 10,000 pasos ({pasos}/10,000)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        agua = st.slider("💧 Agua consumida (L):", 0.0, 5.0, 1.8, 0.1)
        st.progress(min(agua/2.5, 1.0))
        st.caption(f"Meta: 2.5L ({agua:.1f}/2.5L)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        sueño = st.slider("😴 Horas de sueño:", 0, 12, 7)
        st.progress(min(sueño/8, 1.0))
        st.caption(f"Ideal: 7-8 horas ({sueño}/8)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        calorias = st.number_input("🔥 Calorías hoy:", 0, 5000, 2100)
        st.progress(min(calorias/2500, 1.0))
        st.caption(f"Meta: 2,100-2,300 kcal")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sección de hábitos semanales
    st.subheader("📅 Hábitos para esta semana")
    
    habit_col1, habit_col2 = st.columns(2)
    
    with habit_col1:
        st.markdown("### 🍎 Nutrición")
        habitos_nutricion = {
            "Desayunar en 1 hora después de levantarse": st.checkbox("🌅 Desayuno temprano", True),
            "5 porciones de frutas/verduras al día": st.checkbox("🥦 5 frutas/verduras", False),
            "Consumir proteína en cada comida": st.checkbox("🍗 Proteína balanceada", True),
            "Limitar azúcares añadidos": st.checkbox("🚫 Sin azúcar añadido", False),
            "Comer cada 3-4 horas": st.checkbox("⏰ Comidas regulares", True)
        }
        
        # Mostrar progreso nutrición
        progreso_nut = sum(habitos_nutricion.values()) / len(habitos_nutricion) * 100
        st.metric("Progreso nutrición", f"{progreso_nut:.0f}%")
    
    with habit_col2:
        st.markdown("### 🏃 Actividad")
        habitos_actividad = {
            "30 minutos de ejercicio al día": st.checkbox("⏱️ 30 min ejercicio", False),
            "Estiramientos matutinos": st.checkbox("🧘 Estiramientos", True),
            "10,000 pasos diarios": st.checkbox("👣 10K pasos", False),
            "Pausas activas cada 2 horas": st.checkbox("⚡ Pausas activas", True),
            "Ejercicio de fuerza 3x/semana": st.checkbox("💪 Fuerza 3x", False)
        }
        
        # Mostrar progreso actividad
        progreso_act = sum(habitos_actividad.values()) / len(habitos_actividad) * 100
        st.metric("Progreso actividad", f"{progreso_act:.0f}%")
    
    # Desafío semanal
    st.subheader("🎯 Desafío de la semana")
    
    with st.expander("🔥 Desafío: Hidratación consciente", expanded=True):
        st.markdown("""
        **Objetivo:** Beber 2.5L de agua al día durante 7 días seguidos.
        
        **Reglas:**
        1. 💧 1 vaso al despertar (250ml)
        2. 🥤 1 vaso antes de cada comida (750ml)
        3. 🏢 1 vaso cada 2 horas de trabajo (500ml)
        4. 🏋️ 1 vaso durante ejercicio (500ml)
        5. 🌙 1 vaso antes de dormir (250ml)
        
        **Beneficios esperados:**
        - ✅ Más energía durante el día
        - ✅ Piel más hidratada
        - ✅ Mejor digestión
        - ✅ Control del apetito
        - ✅ Desintoxicación natural
        
        **Premio al completar:** 🏆 Insignia "Hidratación Máxima"
        """)
        
        dias = st.multiselect(
            "📅 Días completados:",
            ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
            ["Lunes", "Martes"]
        )
        
        if len(dias) == 7:
            st.success("🎉 ¡Felicidades! Has completado el desafío semanal.")
    
    # Consejos científicos
    st.subheader("🧠 Consejos basados en ciencia")
    
    consejos_col1, consejos_col2, consejos_col3 = st.columns(3)
    
    with consejos_col1:
        st.markdown('<div class="habit-card">', unsafe_allow_html=True)
        st.markdown("**🍽️ Técnica del plato saludable**")
        st.markdown("""
        1. ½ plato de verduras
        2. ¼ plato de proteínas
        3. ¼ plato de carbohidratos
        4. Grasas saludables
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with consejos_col2:
        st.markdown('<div class="habit-card">', unsafe_allow_html=True)
        st.markdown("**😴 Ritmo circadiano**")
        st.markdown("""
        • Comer en ventana de 10h
        • Dormir a la misma hora
        • Exposición solar matutina
        • Cenar 3h antes de dormir
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with consejos_col3:
        st.markdown('<div class="habit-card">', unsafe_allow_html=True)
        st.markdown("**🧘 Mindfulness alimenticio**")
        st.markdown("""
        • Comer sin distracciones
        • Masticar 20-30 veces
        • Saborear cada bocado
        • Reconocer señales de saciedad
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recursos adicionales
    with st.expander("📚 Recursos adicionales"):
        st.markdown("""
        **Libros recomendados:**
        - 📖 "Hábitos Atómicos" de James Clear
        - 📖 "El poder de los hábitos" de Charles Duhigg
        - 📖 "La mente consciente" de Daniel Siegel
        
        **Apps útiles:**
        - 📱 MyFitnessPal (seguimiento nutricional)
        - 📱 Strava (actividad física)
        - 📱 Headspace (meditación)
        - 📱 Water Reminder (hidratación)
        
        **Canales de YouTube:**
        - ▶️ NutritionFacts.org
        - ▶️ Doctor Mike
        - ▶️ Athlean-X
        - ▶️ Yoga With Adriene
        """)
    
    # Botón de registro diario
    if st.button("📝 Registrar mi día hoy", use_container_width=True):
        st.success("✅ Registro guardado. ¡Buen trabajo!")

# ================= MI PROGRESO =================
elif page == "📊 Mi progreso":
    st.header("📈 Mi Progreso y Estadísticas")
    
    # Resumen mensual
    st.subheader("📅 Resumen del mes actual")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📋 Días saludables", "22/30", "+5 vs mes pasado")
    
    with col2:
        st.metric("🎯 Objetivos cumplidos", "15", "83% efectividad")
    
    with col3:
        st.metric("🔥 Calorías promedio", "2,150 kcal", "-150 vs meta")
    
    # Gráficos (placeholders por ahora)
    st.subheader("📊 Evolución de hábitos")
    
    tab1, tab2, tab3 = st.tabs(["🏃 Actividad", "🍎 Nutrición", "😴 Descanso"])
    
    with tab1:
        st.markdown("**Pasos diarios (últimas 2 semanas)**")
        # Placeholder para gráfico
        st.info("📈 Integración con gráficos disponible en versión PRO")
        st.write("Tendencia: ↗️ Aumentando 12% semanal")
    
    with tab2:
        st.markdown("**Consumo de agua (últimos 7 días)**")
        # Placeholder para gráfico
        st.info("📈 Integración con gráficos disponible en versión PRO")
        st.write("Promedio: 2.1L/día (84% de meta)")
    
    with tab3:
        st.markdown("**Horas de sueño (último mes)**")
        # Placeholder para gráfico
        st.info("📈 Integración con gráficos disponible en versión PRO")
        st.write("Promedio: 7.2h/noche")
    
    # Logros
    st.subheader("🏆 Mis Logros")
    
    logro_col1, logro_col2, logro_col3 = st.columns(3)
    
    with logro_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🥇")
        st.markdown("**7 días consecutivos**")
        st.markdown("Hidratación perfecta")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with logro_col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🥈")
        st.markdown("**Meta superada**")
        st.markdown("10K pasos x 15 días")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with logro_col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🥉")
        st.markdown("**Consistencia**")
        st.markdown("21 días sin azúcar")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Reflexión semanal
    with st.expander("💭 Reflexión semanal"):
        reflexion = st.text_area(
            "¿Cómo te sentiste esta semana? ¿Qué logros celebramos?",
            height=100,
            placeholder="Esta semana logré... Me sentí orgulloso de... La próxima semana mejoraré..."
        )
        
        if st.button("Guardar reflexión"):
            st.success("Reflexión guardada en tu diario personal")

# Footer de la aplicación
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🥗 <strong>NutriGen AI</strong> • Tu compañero en el viaje hacia una vida más saludable</p>
    <p>💡 <em>Recuerda: La consistencia es más importante que la perfección</em></p>
    <p style="font-size: 0.8rem;">v2.0 • Basado en ciencia nutricional • Actualizado hoy</p>
</div>
""", unsafe_allow_html=True)
