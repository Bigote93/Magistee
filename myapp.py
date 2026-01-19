# app_agromarket.py
# ---------- IMPORTACIONES ----------
import streamlit as st
import pandas as pd
import altair as alt
from scipy.stats import pearsonr
# -----------------------------------

# ---------- COnstantes de datos ----------
data = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril"],
    "Ventas (MM$)": [520, 480, 450, 420],
    "N° de clientes activos": [1200,1100,1050,950],
    "Reclamos registrados": [15,22,28,35]
}

# ------- CONFIGURACIÓN DE LA PÁGINA URI----------
st.set_page_config(
    page_title="Caso AgroMarket S.A.",
    page_icon="📊",
    layout="wide"
)
# -----------------------------------------------

# ------- BANNER IZQUIERDO Y PANEL DE INFORMACIÓN DEL CURSO -------
st.sidebar.image("/home/dnalli/Escritorio/Magistee/imgs/Universidad-autonoma-de-chile.png")
st.sidebar.markdown("""
        # Universidad Autonoma de Chile
        **Curso:** Toma de decisiones basada en datos         
        **Profesor:** César González Zúñiga 
        **Grupo:** 2
        """)
st.sidebar.markdown("---")
st.sidebar.markdown("## Integrantes del grupo:")
st.sidebar.markdown("""
        - Osvaldo Felipe Cerda González
        - Kevin Felipe Gomez Aranda
        - Gonzalo Patricio Luna Ahumada
        - Diego Alfredo Nalli García
        """)
st.sidebar.markdown("---")
# ---------------------------------------------------------------

# ------- TÍTULO Y DESCRIPCIÓN DE LA APLICACIÓN -------
st.title("📊 AgroMarket S.A.")
st.write("Aplicación en Streamlit para analizar el caso de AgroMarket S.A.")
# ---------------------------------------------------


# Barra lateral de navegación (la iremos completando)
seccion = st.sidebar.radio(
    "Panel",
    [
        "Instrucciones",
        "Datos",
        "Análisis",
        "Modelos de decisión"
    ]
)



# ------ ESTRUCTURA DE SECCIONES DE LA APLICACIÓN -------
if seccion == "Instrucciones":
    st.header("📘 Instrucciones del trabajo")

    st.subheader("¿Que debemos hacer?")
    st.markdown("""
    - **Clasificar datos:** Identificar cuáles de los datos presentados son estructurados y no estructurados.
    - **Evaluación de calidad de datos:** Analizar si la información presentada cumple con criterios de integridad, confiabilidad y utilidad para la toma de decisiones.
    """)

    st.subheader("Análisis estadistico descriptivo")
    st.markdown("""
    - Tasa de variación mensual de ventas.
    - Promedio de reclamos
    - Relación entre clientes activos y reclamos
    """)

    st.subheader("Análisis inferencial")
    st.markdown("Formular una hipótesis sobre la relación entre el aumento de reclamos y la disminución de clientes, y plantear cómo se validaría (sin necesidad de cálculos avanzados, solo diseño del análisis).")

    st.subheader("Modelos de apoyo a la decisión")
    st.markdown("""
    - Proponer un modelo analítico
    - Proponer un modelo predictivo
    - Proponer un modelo prescriptivo
    """)


elif seccion == "Datos":
    st.header("Datos internos")
    st.write("Ventas registradas en el Sistema de Gestión de AgroMarket S.A.")



    df = pd.DataFrame(data)
    st.write(df)

    # ------ Detalles de datos internos -------
    st.subheader("Observación:")
    st.text("Para la obtención de datos de comentarios en redes sociales se evidencian como:")
    st.markdown("""
    - Los productos ya no llegan tan frescos como antes.
    - La entrega demora más de lo prometido
    - La atención telefónica no responde rápido
    """)

    st.header("Datos externos")
    st.write("Un informe del Ministerio de Agricultura indica que el consumo de frutas ha caído un 5% anual por cambios en los hábitos alimenticios.")

    st.subheader("Solicitud de gerencia:")
    st.markdown("La gerencia quiere que el equipo de analistas identifique las causas del problema, "
               "evalúe la calidad e integridad de los datos disponibles y elabore un modelo de "
               "apoyo a la decisión para revertir la tendencia de las ventas."
               "")

elif seccion == "Análisis":
    st.header("Análisis")

    st.subheader("Clasificación de datos")
    st.image("/home/dnalli/Escritorio/Magistee/imgs/claisifcacion de datos.png", caption="Clasificación de datos")

    st.subheader("Análisis estadístico descriptivo")





    # ---- Calculo de contraccion de ventas ----
    df = pd.DataFrame(data)

    st.markdown("### Tasa de variación mensual de ventas")
    ventas = df["Ventas (MM$)"]
    tasa_variacion = ventas.pct_change().fillna(0) * 100
    df["Tasa de variación mensual (%)"] = tasa_variacion.round(2)
    st.write(df[["Mes", "Ventas (MM$)", "Tasa de variación mensual (%)"]])  
    st.markdown("Se observa una disminución constante en las ventas mensuales.")

    # Agregando columna de diferencia de contraccion respecto al mes anterior
    df["Diferencia de contracción (%)"] = df["Tasa de variación mensual (%)"].diff().fillna(0).round(2)
    st.write(df[["Mes", "Tasa de variación mensual (%)", "Diferencia de contracción (%)"]])

    # ----- Calculo de contraccion total de ventas ----
    st.markdown("### Contracción total de ventas")
    contraccion_total = ((ventas.iloc[-1] - ventas.iloc[0]) / ventas.iloc[0]) * 100
    st.write(f"La contracción total de ventas de Enero a Abril es de {contraccion_total:.2f}%.")

    # ------------------------------------------------

    # ---- Promedio de reclamos ----
    st.markdown("### Promedio de reclamos")
    promedio_reclamos = df["Reclamos registrados"].mean()
    st.write(f"El promedio de reclamos registrados es de {promedio_reclamos:.0f} reclamos por mes.")
    # ------------------------------------------------

        # ---- Relación Clientes Activos vs. Reclamos ----
    st.markdown("### Relación (Ratio) Clientes Activos vs. Reclamos")
    
    # Calcular indicador de conflictividad
    df["Reclamos por 100 clientes (%)"] = (df["Reclamos registrados"] / df["N° de clientes activos"] * 100).round(2)
    
    st.write(df[["Mes", "N° de clientes activos", "Reclamos registrados", "Reclamos por 100 clientes (%)"]])
    
    st.markdown("""
    **Indicador de conflictividad de la cartera:**
    - **Enero**: 1.25% (1.2 reclamos por cada 100 clientes).
    - **Abril**: 3.68% (Casi 4 de cada 100 clientes reclaman formalmente).
    
    El indicador de conflictividad se ha **triplicado** en este período.
    """)
    
    st.info("""
    **Conclusion inicial:**
    La calidad del servicio se deteriora a un ritmo más rápido que la fuga de clientes.
    El indicador de conflictividad permite evaluar la magnitud del deterioro en la experiencia del cliente. 
    De acuerdo a la evidencia, este aumento evidencia que la degradación del servicio se concentra en 
    la experiencia del cliente y no exclusivamente en la pérdida de demanda.
    """)
    # ------------------------------------------------

    # ---- Análisis de Correlación de Pearson ----
    st.markdown("### Análisis de Correlación de Pearson")
    
    st.markdown("""
    **Definicion**: El coeficiente de correlación de Pearson mide la relación lineal entre dos variables.
    Valores cercanos a -1 indican correlación negativa fuerte, 0 indica sin correlación, 
    y valores cercanos a 1 indican correlación positiva fuerte.
    """)
    
    # ---------------- Cálculo de correlación ----------------
    
    clientes = df["N° de clientes activos"]
    reclamos = df["Reclamos registrados"]
    
    # Calcular coeficiente de correlación y p-value
    coef_pearson, p_value = pearsonr(clientes, reclamos)
    
    # Mostrar resultados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Coeficiente de Correlación (r)", f"{coef_pearson:.4f}")
    
    with col2:
        st.metric("P-value", f"{p_value:.6f}")
    
    with col3:
        if p_value < 0.05:
            significancia = "✅ Significativa"
        else:
            significancia = "❌ No significativa"
        st.metric("Significancia (α=0.05)", significancia)
    
    # Interpretación
    st.markdown("""
    **Observacion de lo resultante:**
    """)
    
    if coef_pearson < -0.7:
        interpretacion = "**Correlación negativa fuerte**: A medida que los clientes activos disminuyen, los reclamos aumentan significativamente."
    elif coef_pearson < -0.4:
        interpretacion = "**Correlación negativa moderada**: Existe una relación inversa notable entre clientes activos y reclamos."
    elif coef_pearson < 0:
        interpretacion = "**Correlación negativa débil**: Existe una leve relación inversa."
    else:
        interpretacion = "**No hay correlación negativa significativa**."
    
    st.markdown(interpretacion)
    
    if p_value < 0.05:
        st.success(f"""
        ✅ Con un p-value de {p_value:.6f} < 0.05, **rechazamos la hipótesis nula**.
        La relación entre clientes activos y reclamos es **estadísticamente significativa**.
        """)
    else:
        st.warning(f"""
        ⚠️ Con un p-value de {p_value:.6f} > 0.05, **no rechazamos la hipótesis nula**.
        La relación entre clientes activos y reclamos **no es estadísticamente significativa**.
        """)
    
    # Gráfico de dispersión con línea de tendencia
    st.markdown("#### Gráfico de dispersión")
    
    scatter = alt.Chart(df).mark_circle(size=100, color='steelblue').encode(
        x=alt.X("N° de clientes activos", title="Clientes Activos"),
        y=alt.Y("Reclamos registrados", title="Reclamos"),
        tooltip=["Mes", "N° de clientes activos", "Reclamos registrados"]
    ).properties(height=400)
    
    st.altair_chart(scatter, use_container_width=True)

    # Observaciones y alcances dado los datos limitados
    st.markdown("""

    **Observaciones y alcances:**
    - Tamaño muestral extremadamente reducido (n=4): Con solo cuatro puntos mensuales, la estimación de Pearson (y cualquier otro modelo) es sensible a cualquier variación.
    - Supuesto de linealidad: Pearson solo detecta relaciones lineales. 
    - Sensibilidad a valores atípicos
    """)
    # ------------------------------------------------


elif seccion == "Modelos de decisión":
    st.header("Modelos de apoyo a la decisión")
    
    df = pd.DataFrame(data)
    
    st.markdown("""
    Basados en el análisis de correlación de Pearson y el indicador de conflictividad, 
    proponemos tres modelos para apoyar la toma de decisiones estratégicas.
    """)
    
    # ---- MODELO ANALÍTICO ----
    st.subheader("1. Modelo Analítico: Descomposición de la caída en ventas")
    
    st.markdown("""
    Este modelo descompone la caída de ventas en dos efectos principales:
    
    **Fórmula:** Ventas = Clientes Activos × Venta Promedio por Cliente
    """)
    
    # Calcular venta promedio por cliente
    df["Venta promedio por cliente (MM$)"] = (df["Ventas (MM$)"] / df["N° de clientes activos"]).round(3)
    
    st.write(df[["Mes", "Ventas (MM$)", "N° de clientes activos", "Venta promedio por cliente (MM$)"]])
    
    st.markdown("""
    **Análisis:**
    - **Efecto volumen**: La pérdida de clientes activos (de 1200 a 950) explica parte de la caída.
    - **Efecto precio/calidad**: La venta promedio por cliente también ha disminuido, lo que sugiere 
      que los clientes restantes están comprando menos (posiblemente por la reducción en calidad del servicio).
    """)
    
    # Calcular contribución de cada efecto
    variacion_clientes = ((df["N° de clientes activos"].iloc[-1] - df["N° de clientes activos"].iloc[0]) / df["N° de clientes activos"].iloc[0]) * 100
    variacion_venta_promedio = ((df["Venta promedio por cliente (MM$)"].iloc[-1] - df["Venta promedio por cliente (MM$)"].iloc[0]) / df["Venta promedio por cliente (MM$)"].iloc[0]) * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Variación en Clientes Activos", f"{variacion_clientes:.2f}%")
    with col2:
        st.metric("Variación en Venta Promedio", f"{variacion_venta_promedio:.2f}%")
    
    st.info("""
    ✅ **Conclusión**: Ambos efectos contribuyen a la caída de ventas. La degradación de la calidad 
    del servicio (reflejada en el aumento de reclamos) está impactando tanto en la retención como 
    en el volumen de compra de los clientes existentes.
    """)
    
    # ---- MODELO PREDICTIVO ----
    st.subheader("2. Modelo Predictivo: Proyección de tendencias")
    
    st.markdown("""
    Si la tendencia actual continúa sin intervención, ¿cuál sería el escenario en los próximos 3 meses?
    """)
    
    # Calcular tasas de cambio promedio
    tasa_perdida_clientes = (df["N° de clientes activos"].pct_change().mean())
    tasa_aumento_reclamos = (df["Reclamos registrados"].pct_change().mean())
    
    # Proyectar 3 meses adicionales
    proyeccion_meses = ["Mayo", "Junio", "Julio"]
    proyeccion_datos = {
        "Mes": proyeccion_meses,
        "Clientes Activos (proyectado)": [],
        "Reclamos (proyectado)": [],
        "Venta promedio (proyectado)": []
    }
    
    ultimo_cliente = df["N° de clientes activos"].iloc[-1]
    ultimo_reclamo = df["Reclamos registrados"].iloc[-1]
    ultima_venta_promedio = df["Venta promedio por cliente (MM$)"].iloc[-1]
    
    for i in range(1, 4):
        clientes_proj = int(ultimo_cliente * ((1 + tasa_perdida_clientes) ** i))
        reclamos_proj = int(ultimo_reclamo * ((1 + tasa_aumento_reclamos) ** i))
        venta_prom_proj = ultima_venta_promedio * ((1 + tasa_aumento_reclamos) ** i)
        
        proyeccion_datos["Clientes Activos (proyectado)"].append(clientes_proj)
        proyeccion_datos["Reclamos (proyectado)"].append(reclamos_proj)
        proyeccion_datos["Venta promedio (proyectado)"].append(round(venta_prom_proj, 3))
    
    df_proyeccion = pd.DataFrame(proyeccion_datos)
    st.write(df_proyeccion)
    
    # Gráfico de proyección
    df_historico = df[["Mes", "N° de clientes activos"]].copy()
    df_historico.columns = ["Mes", "Clientes"]
    df_historico["Tipo"] = "Histórico"
    
    df_proj_grafico = df_proyeccion[["Mes", "Clientes Activos (proyectado)"]].copy()
    df_proj_grafico.columns = ["Mes", "Clientes"]
    df_proj_grafico["Tipo"] = "Proyectado"
    
    df_combinado = pd.concat([df_historico, df_proj_grafico], ignore_index=True)
    
    chart_proyeccion = alt.Chart(df_combinado).mark_line(point=True).encode(
        x=alt.X("Mes:N", sort=list(df_historico["Mes"]) + proyeccion_meses),
        y=alt.Y("Clientes:Q", title="Clientes Activos"),
        color=alt.Color("Tipo:N", scale=alt.Scale(domain=["Histórico", "Proyectado"], range=["steelblue", "orange"])),
        tooltip=["Mes", "Clientes", "Tipo"]
    ).properties(height=400)
    
    st.altair_chart(chart_proyeccion, use_container_width=True)
    
    st.warning(f"""
    ⚠️ **Escenario sin intervención**: 
    - Pérdida promedio mensual de clientes: {abs(tasa_perdida_clientes)*100:.1f}%
    - Aumento promedio mensual de reclamos: {tasa_aumento_reclamos*100:.1f}%
    - Para julio se proyectan solo {proyeccion_datos['Clientes Activos (proyectado)'][-1]} clientes activos.
    """)
    
    # ---- MODELO PRESCRIPTIVO ----
    st.subheader("3. Modelo Prescriptivo: Recomendaciones de decisión")
    
    st.markdown("""
    Con base en los análisis previos, se proponen las siguientes acciones estratégicas:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 Acciones Inmediatas (0-30 días)
        
        1. **Auditoría operacional urgente**
           - Revisar procesos de logística y almacenamiento
           - Evaluar protocolos de manejo de productos perecederos
        
        2. **Implementar sistema de feedback**
           - Encuestas post-compra
           - Monitoreo de redes sociales en tiempo real
        
        3. **Centro de atención al cliente mejorado**
           - Aumentar cobertura telefónica
           - Reducir tiempo de respuesta
        """)
    
    with col2:
        st.markdown("""
        #### 📊 Acciones Mediano Plazo (1-3 meses)
        
        1. **Programa de retención de clientes**
           - Ofrecer incentivos a clientes de alto valor
           - Programa de lealtad
        
        2. **Mejora de calidad**
           - Inversión en cadena de frío
           - Reducir tiempos de entrega
        
        3. **Análisis de costos**
           - Evaluar impacto de mejoras en rentabilidad
        """)
    
 