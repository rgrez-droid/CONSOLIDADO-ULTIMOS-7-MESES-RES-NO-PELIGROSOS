import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
st.set_page_config(
    page_title="Análisis Residuos No Peligrosos Últimos 7 Meses",
    layout="wide"
)

# =====================================================
# ARCHIVOS
# =====================================================
archivo_excel = "ANALISIS RESIDUOS NO PELIGROSOS ULTIMOS 7 MESES.xlsx"
logo_superior = "logo1.png"
logo_sello = "logoredondo.png"

# =====================================================
# CONVERTIR IMAGEN A BASE64 PARA SELLO DE AGUA
# =====================================================
def imagen_base64(ruta):
    if os.path.exists(ruta):
        with open(ruta, "rb") as imagen:
            return base64.b64encode(imagen.read()).decode()
    return None


sello_base64 = imagen_base64(logo_sello)
css_sello = ""

if sello_base64:
    css_sello = f"""
    .stApp::before {{
        content: "";
        position: fixed;
        top: 55%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 620px;
        height: 620px;
        background-image: url("data:image/png;base64,{sello_base64}");
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.035;
        z-index: 0;
        pointer-events: none;
    }}

    .block-container {{
        position: relative;
        z-index: 1;
    }}
    """

# =====================================================
# ESTILO VISUAL
# =====================================================
st.markdown(
    f"""
    <style>
        /* =================================================
           FONDO GENERAL
        ================================================= */
        .stApp {{
            background-color: #0f172a;
            color: #ffffff;
        }}

        {css_sello}

        html, body {{
            color: #ffffff;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: #ffffff !important;
            font-weight: 800 !important;
        }}

        /* =================================================
           ENCABEZADO
        ================================================= */
        .titulo-principal {{
            font-size: 46px;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 12px;
            line-height: 1.15;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.45);
        }}

        .subtitulo {{
            font-size: 21px;
            color: #e2e8f0;
            margin-bottom: 35px;
            line-height: 1.45;
            max-width: 1450px;
            font-weight: 500;
        }}

        /* =================================================
           TÍTULO DE FILTROS
        ================================================= */
        .seccion-filtros {{
            border-left: 8px solid #f59e0b;
            padding-left: 20px;
            font-size: 34px;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 25px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.45);
        }}

        label {{
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 17px !important;
        }}

        /* =================================================
           CAJAS DE SELECCIÓN
        ================================================= */
        div[data-baseweb="select"] > div {{
            background-color: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
        }}

        /* Texto interno visible en selectbox y multiselect */
        div[data-baseweb="select"] > div > div {{
            color: #0f172a !important;
        }}

        div[data-baseweb="select"] > div > div * {{
            color: #0f172a !important;
        }}

        div[data-baseweb="select"] span {{
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        div[data-baseweb="select"] input {{
            color: #0f172a !important;
            background-color: #f8fafc !important;
            font-weight: 600 !important;
        }}

        div[data-baseweb="select"] input::placeholder {{
            color: #64748b !important;
            opacity: 1 !important;
        }}

        /* Flecha de los filtros */
        div[data-baseweb="select"] svg {{
            fill: #0f172a !important;
            color: #0f172a !important;
        }}

        /* =================================================
           ELEMENTOS SELECCIONADOS EN MULTISELECT
        ================================================= */
        span[data-baseweb="tag"] {{
            background-color: #ef4444 !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border-radius: 8px !important;
        }}

        span[data-baseweb="tag"] span {{
            color: #ffffff !important;
        }}

        span[data-baseweb="tag"] svg {{
            fill: #ffffff !important;
            color: #ffffff !important;
        }}

        /* =================================================
           OPCIONES DESPLEGABLES
        ================================================= */
        div[data-baseweb="popover"] {{
            background-color: #f8fafc !important;
        }}

        div[data-baseweb="menu"] {{
            background-color: #f8fafc !important;
        }}

        div[role="listbox"] {{
            background-color: #f8fafc !important;
        }}

        ul[role="listbox"] {{
            background-color: #f8fafc !important;
        }}

        div[role="option"] {{
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        div[role="option"] * {{
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        div[role="option"]:hover {{
            background-color: #e2e8f0 !important;
        }}

        li[role="option"] {{
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        li[role="option"] * {{
            color: #0f172a !important;
        }}

        li[role="option"]:hover {{
            background-color: #e2e8f0 !important;
        }}

        /* =================================================
           CAMPO NUMÉRICO
        ================================================= */
        input {{
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 600 !important;
        }}

        /* =================================================
           INDICADORES
        ================================================= */
        div[data-testid="stMetric"] {{
            background-color: rgba(30, 41, 59, 0.96);
            padding: 24px;
            border-radius: 14px;
            border: 1px solid #475569;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
        }}

        div[data-testid="stMetricLabel"] {{
            color: #e2e8f0 !important;
            font-size: 18px !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stMetricValue"] {{
            color: #ffffff !important;
            font-size: 32px !important;
            font-weight: 900 !important;
        }}

        /* =================================================
           TABLAS Y SEPARADORES
        ================================================= */
        .stDataFrame {{
            background-color: #ffffff;
            border-radius: 10px;
        }}

        hr {{
            border-color: #334155 !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# CARGAR Y TRANSFORMAR DATOS
# =====================================================
@st.cache_data
def cargar_datos(ruta_excel):
    df = pd.read_excel(
        ruta_excel,
        sheet_name="Hoja1",
        header=None
    )

    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    registros = []
    columna_fecha = None

    for col in range(len(df.columns)):
        posibles_fechas = pd.to_datetime(
            df.iloc[2:, col],
            errors="coerce"
        )

        if posibles_fechas.notna().sum() >= 2:
            columna_fecha = col
            break

    if columna_fecha is None:
        raise ValueError(
            "No se encontró la columna de fechas en la planilla."
        )

    meses_espanol = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    for fila in range(2, len(df)):
        fecha = pd.to_datetime(
            df.iloc[fila, columna_fecha],
            errors="coerce"
        )

        if pd.isna(fecha):
            continue

        anio = fecha.year
        mes_numero = fecha.month
        mes_nombre = meses_espanol[mes_numero]
        periodo = f"{mes_nombre} {anio}"

        residuo_actual = None

        for col in range(columna_fecha + 1, len(df.columns)):
            nombre_residuo = df.iloc[0, col]
            concepto = df.iloc[1, col]

            if pd.notna(nombre_residuo):
                residuo_actual = str(nombre_residuo).strip()

            if pd.isna(concepto) or residuo_actual is None:
                continue

            concepto = str(concepto).strip()

            if concepto == "Traslados":
                traslados = pd.to_numeric(
                    df.iloc[fila, col],
                    errors="coerce"
                )

                camion_carro = pd.to_numeric(
                    df.iloc[fila, col + 1],
                    errors="coerce"
                )

                peso_promedio = pd.to_numeric(
                    df.iloc[fila, col + 2],
                    errors="coerce"
                )

                traslados = (
                    0 if pd.isna(traslados)
                    else traslados
                )

                camion_carro = (
                    0 if pd.isna(camion_carro)
                    else camion_carro
                )

                peso_promedio = (
                    0 if pd.isna(peso_promedio)
                    else peso_promedio
                )

                toneladas = (
                    traslados * peso_promedio
                ) / 1000

                registros.append({
                    "Fecha": fecha,
                    "Año": anio,
                    "Mes número": mes_numero,
                    "Mes": mes_nombre,
                    "Periodo": periodo,
                    "Residuo": residuo_actual,
                    "Traslados": traslados,
                    "Salidas camión y carro": camion_carro,
                    "Peso promedio por traslado kg": peso_promedio,
                    "Toneladas estimadas": toneladas
                })

    return pd.DataFrame(registros)

# =====================================================
# ENCABEZADO
# =====================================================
col_titulo, col_logo = st.columns([5, 1])

with col_titulo:
    st.markdown(
        """
        <div class="titulo-principal">
            ♻️ Análisis Residuos No Peligrosos Últimos 7 Meses
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitulo">
            El objetivo de este análisis es entregar una visión más clara
            del comportamiento operacional de los principales residuos
            gestionados, identificando la cantidad de traslados realizados,
            el uso de camión y carro, y las toneladas estimadas movilizadas
            por cada tipo de residuo.
        </div>
        """,
        unsafe_allow_html=True
    )

with col_logo:
    if os.path.exists(logo_superior):
        st.image(
            logo_superior,
            width=190
        )

# =====================================================
# DASHBOARD PRINCIPAL
# =====================================================
try:
    df = cargar_datos(archivo_excel)

    # =================================================
    # FILTROS
    # =================================================
    st.markdown(
        """
        <div class="seccion-filtros">
            🔎 Filtros de análisis
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        filtro_anio = st.multiselect(
            "Año",
            sorted(df["Año"].unique()),
            default=sorted(df["Año"].unique())
        )

    with col2:
        meses_ordenados = (
            df[["Mes número", "Mes"]]
            .drop_duplicates()
            .sort_values("Mes número")["Mes"]
            .tolist()
        )

        filtro_mes = st.multiselect(
            "Mes",
            meses_ordenados,
            default=meses_ordenados
        )

    with col3:
        filtro_residuo = st.multiselect(
            "Residuo / disposición",
            sorted(df["Residuo"].unique()),
            default=sorted(df["Residuo"].unique())
        )

    col4, col5 = st.columns(2)

    with col4:
        filtro_tipo_salida = st.selectbox(
            "Tipo de análisis",
            [
                "Todos los traslados",
                "Solo salidas con camión y carro",
                "Solo salidas sin camión y carro"
            ]
        )

    with col5:
        filtro_minimo_traslados = st.number_input(
            "Mínimo de traslados",
            min_value=0,
            value=0,
            step=1
        )

    # =================================================
    # APLICAR FILTROS
    # =================================================
    df_filtrado = df[
        (df["Año"].isin(filtro_anio)) &
        (df["Mes"].isin(filtro_mes)) &
        (df["Residuo"].isin(filtro_residuo)) &
        (df["Traslados"] >= filtro_minimo_traslados)
    ]

    if filtro_tipo_salida == "Solo salidas con camión y carro":
        df_filtrado = df_filtrado[
            df_filtrado["Salidas camión y carro"] > 0
        ]

    elif filtro_tipo_salida == "Solo salidas sin camión y carro":
        df_filtrado = df_filtrado[
            df_filtrado["Salidas camión y carro"] == 0
        ]

    # =================================================
    # MÉTRICAS PRINCIPALES
    # =================================================
    st.markdown("---")
    st.subheader("📌 Indicadores principales")

    total_traslados = (
        df_filtrado["Traslados"].sum()
    )

    total_camion_carro = (
        df_filtrado["Salidas camión y carro"].sum()
    )

    total_toneladas = (
        df_filtrado["Toneladas estimadas"].sum()
    )

    promedio_mensual_traslados = (
        df_filtrado
        .groupby("Periodo")["Traslados"]
        .sum()
        .mean()
        if not df_filtrado.empty
        else 0
    )

    promedio_mensual_camion_carro = (
        df_filtrado
        .groupby("Periodo")["Salidas camión y carro"]
        .sum()
        .mean()
        if not df_filtrado.empty
        else 0
    )

    promedio_mensual_toneladas = (
        df_filtrado
        .groupby("Periodo")["Toneladas estimadas"]
        .sum()
        .mean()
        if not df_filtrado.empty
        else 0
    )

    promedio_toneladas_traslado = (
        total_toneladas / total_traslados
        if total_traslados > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total traslados",
        f"{total_traslados:,.0f}"
    )

    col2.metric(
        "Promedio mensual traslados",
        f"{promedio_mensual_traslados:,.2f}"
    )

    col3.metric(
        "Salidas camión y carro",
        f"{total_camion_carro:,.0f}"
    )

    col4.metric(
        "Toneladas por traslado",
        f"{promedio_toneladas_traslado:,.2f}"
    )

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "Toneladas estimadas",
        f"{total_toneladas:,.2f}"
    )

    col6.metric(
        "Promedio mensual camión y carro",
        f"{promedio_mensual_camion_carro:,.2f}"
    )

    col7.metric(
        "Promedio mensual toneladas",
        f"{promedio_mensual_toneladas:,.2f}"
    )

    # =================================================
    # RESUMEN POR RESIDUO
    # =================================================
    st.subheader(
        "📊 Resumen consolidado por residuo / disposición"
    )

    resumen = df_filtrado.groupby("Residuo").agg(
        Total_traslados=(
            "Traslados",
            "sum"
        ),
        Total_salidas_camion_y_carro=(
            "Salidas camión y carro",
            "sum"
        ),
        Total_toneladas_estimadas=(
            "Toneladas estimadas",
            "sum"
        ),
        Promedio_mensual_traslados=(
            "Traslados",
            "mean"
        ),
        Promedio_mensual_camion_y_carro=(
            "Salidas camión y carro",
            "mean"
        ),
        Promedio_peso_por_traslado_kg=(
            "Peso promedio por traslado kg",
            "mean"
        )
    ).reset_index()

    resumen["Promedio toneladas por traslado"] = (
        resumen["Total_toneladas_estimadas"] /
        resumen["Total_traslados"]
    ).fillna(0)

    resumen = resumen.rename(columns={
        "Residuo": "Residuo / disposición",
        "Total_traslados": "Total traslados",
        "Total_salidas_camion_y_carro":
            "Total salidas camión y carro",
        "Total_toneladas_estimadas":
            "Total toneladas estimadas",
        "Promedio_mensual_traslados":
            "Promedio mensual traslados",
        "Promedio_mensual_camion_y_carro":
            "Promedio mensual camión y carro",
        "Promedio_peso_por_traslado_kg":
            "Promedio peso por traslado kg"
    })

    resumen = resumen.round(2)

    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # PROMEDIOS MENSUALES POR DISPOSICIÓN
    # =================================================
    st.subheader(
        "📈 Promedio mensual por residuo / disposición"
    )

    promedio_disposicion = (
        df_filtrado
        .groupby("Residuo")
        .agg(
            Promedio_mensual_traslados=(
                "Traslados",
                "mean"
            ),
            Promedio_mensual_camion_y_carro=(
                "Salidas camión y carro",
                "mean"
            ),
            Promedio_mensual_toneladas=(
                "Toneladas estimadas",
                "mean"
            )
        )
        .reset_index()
    )

    promedio_disposicion = (
        promedio_disposicion.round(2)
    )

    promedio_disposicion = (
        promedio_disposicion.rename(columns={
            "Residuo": "Residuo / disposición",
            "Promedio_mensual_traslados":
                "Promedio mensual traslados",
            "Promedio_mensual_camion_y_carro":
                "Promedio mensual camión y carro",
            "Promedio_mensual_toneladas":
                "Promedio mensual toneladas"
        })
    )

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        fig_torta = px.pie(
            promedio_disposicion,
            names="Residuo / disposición",
            values="Promedio mensual traslados",
            hole=0.45,
            title=(
                "Distribución del promedio mensual "
                "de traslados"
            )
        )

        fig_torta.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont=dict(
                color="#ffffff",
                size=14
            )
        )

        fig_torta.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#ffffff",
                size=15
            ),
            title_font=dict(
                size=22,
                color="#ffffff"
            ),
            legend=dict(
                font=dict(
                    color="#ffffff",
                    size=13
                ),
                orientation="h",
                yanchor="bottom",
                y=-0.30,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(
            fig_torta,
            use_container_width=True
        )

    with col_g2:
        fig_barras_promedio = px.bar(
            promedio_disposicion.sort_values(
                "Promedio mensual traslados",
                ascending=False
            ),
            x="Residuo / disposición",
            y="Promedio mensual traslados",
            text="Promedio mensual traslados",
            title=(
                "Promedio mensual de traslados "
                "por disposición"
            )
        )

        fig_barras_promedio.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            textfont=dict(
                color="#ffffff",
                size=14
            )
        )

        fig_barras_promedio.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#ffffff",
                size=15
            ),
            title_font=dict(
                size=22,
                color="#ffffff"
            ),
            xaxis_title="Residuo / disposición",
            yaxis_title="Promedio mensual de traslados",
            xaxis=dict(
                tickfont=dict(
                    color="#ffffff",
                    size=13
                )
            ),
            yaxis=dict(
                tickfont=dict(
                    color="#ffffff",
                    size=13
                )
            )
        )

        st.plotly_chart(
            fig_barras_promedio,
            use_container_width=True
        )

    col_g3, col_g4 = st.columns(2)

    with col_g3:
        fig_camion = px.bar(
            promedio_disposicion.sort_values(
                "Promedio mensual camión y carro",
                ascending=False
            ),
            x="Residuo / disposición",
            y="Promedio mensual camión y carro",
            text="Promedio mensual camión y carro",
            title=(
                "Promedio mensual de salidas "
                "con camión y carro"
            )
        )

        fig_camion.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            textfont=dict(
                color="#ffffff",
                size=14
            )
        )

        fig_camion.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#ffffff",
                size=15
            ),
            title_font=dict(
                size=22,
                color="#ffffff"
            ),
            xaxis_title="Residuo / disposición",
            yaxis_title="Promedio mensual camión y carro",
            xaxis=dict(
                tickfont=dict(
                    color="#ffffff",
                    size=13
                )
            ),
            yaxis=dict(
                tickfont=dict(
                    color="#ffffff",
                    size=13
                )
            )
        )

        st.plotly_chart(
            fig_camion,
            use_container_width=True
        )

    with col_g4:
        fig_toneladas = px.bar(
            promedio_disposicion.sort_values(
                "Promedio mensual toneladas",
                ascending=False
            ),
            x="Residuo / disposición",
            y="Promedio mensual toneladas",
            text="Promedio mensual toneladas",
            title=(
                "Promedio mensual de toneladas "
                "estimadas"
            )
        )

        fig_toneladas.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            textfont=dict(
                color="#ffffff",
                size=14
            )
        )

        fig_toneladas.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#ffffff",
                size=15
            ),
            title_font=dict(
                size=22,
                color="#ffffff"
            ),
            xaxis_title="Residuo / disposición",
            yaxis_title="Promedio mensual toneladas",
            xaxis=dict(
                tickfont=dict(
                    color="#ffffff",
                    size=13
                )
            ),
            yaxis=dict(
                tickfont=dict(
                    color="#ffffff",
                    size=13
                )
            )
        )

        st.plotly_chart(
            fig_toneladas,
            use_container_width=True
        )

    # =================================================
    # RESUMEN MENSUAL
    # =================================================
    st.subheader("📅 Resumen mensual")

    resumen_mensual = (
        df_filtrado
        .groupby(["Fecha", "Periodo"])
        .agg(
            Total_traslados=(
                "Traslados",
                "sum"
            ),
            Total_salidas_camion_y_carro=(
                "Salidas camión y carro",
                "sum"
            ),
            Total_toneladas_estimadas=(
                "Toneladas estimadas",
                "sum"
            )
        )
        .reset_index()
    )

    resumen_mensual = (
        resumen_mensual.sort_values("Fecha")
    )

    resumen_mensual_tabla = (
        resumen_mensual
        .drop(columns=["Fecha"])
        .rename(columns={
            "Total_traslados":
                "Total traslados",
            "Total_salidas_camion_y_carro":
                "Total salidas camión y carro",
            "Total_toneladas_estimadas":
                "Total toneladas estimadas"
        })
        .round(2)
    )

    st.dataframe(
        resumen_mensual_tabla,
        use_container_width=True,
        hide_index=True
    )

    fig_linea = px.line(
        resumen_mensual,
        x="Periodo",
        y="Total_traslados",
        markers=True,
        title="Evolución mensual de traslados"
    )

    fig_linea.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#ffffff",
            size=15
        ),
        title_font=dict(
            size=22,
            color="#ffffff"
        ),
        xaxis_title="Periodo",
        yaxis_title="Total traslados",
        xaxis=dict(
            tickfont=dict(
                color="#ffffff",
                size=13
            )
        ),
        yaxis=dict(
            tickfont=dict(
                color="#ffffff",
                size=13
            )
        )
    )

    st.plotly_chart(
        fig_linea,
        use_container_width=True
    )

    # =================================================
    # PIE DE PÁGINA
    # =================================================
    st.markdown(
        """
        <div style="
            text-align: center;
            margin-top: 55px;
            padding: 24px 12px 10px 12px;
            color: #cbd5e1;
            font-size: 15px;
            line-height: 1.65;
            border-top: 1px solid rgba(148, 163, 184, 0.25);
        ">
            <strong>
                Panel desarrollado por Ricardo Grez
            </strong>
            <br>
            Administrador de Contrato | SAIVAM
            <br>
            Version 1.0 | Ultima actualizacion: Mayo 2026
        </div>
        """,
        unsafe_allow_html=True
    )

except FileNotFoundError:
    st.error("No se encontró la planilla Excel.")

    st.write(
        "El archivo debe estar en la misma carpeta que app.py "
        "y llamarse exactamente:"
    )

    st.code(
        "ANALISIS RESIDUOS NO PELIGROSOS ULTIMOS 7 MESES.xlsx"
    )

except Exception as e:
    st.error("Ocurrió un error al cargar el dashboard.")
    st.write(e)