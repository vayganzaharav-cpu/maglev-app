import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# 1. Настройка внешнего вида страницы
st.set_page_config(page_title="Maglev Research Lab", layout="wide")

# Кастомный заголовок с иконкой
st.title("🔬 Исследование магнитной левитации (Maglev)")
st.markdown("""
---
**Цель проекта:** Изучение зависимости подъемной силы магнитного поля от расстояния и мощности источника. 
Данное приложение является математическим двойником физической установки.
""")

# 2. Боковая панель управления (Sidebar)
with st.sidebar:
    st.header("⚙️ Параметры системы")
    
    with st.expander("🧲 Свойства магнита", expanded=True):
        magnet_power = st.slider("Мощность (M)", 0.1, 50.0, 10.0, step=0.5)
        k_factor = st.number_input("Коэффициент калибровки (k)", value=500, help="Подстраивается под реальные весы")

    with st.expander("📐 Условия замера", expanded=True):
        mass_target = st.number_input("Масса объекта (г)", value=45)
        current_dist = st.slider("Текущий зазор (мм)", 1, 80, 25)

# 3. Подготовка данных
dist_range = np.linspace(2, 100, 400)
theoretical_force = (k_factor * magnet_power) / (dist_range**2)
current_force_val = (k_factor * magnet_power) / (current_dist**2)

# ПРИМЕР ТВОИХ ДАННЫХ (Замени цифры на свои реальные замеры!)
# Формат: [Расстояние в мм, Вес на весах в граммах]
my_data = [
    [10, 250], [15, 110], [20, 60], [25, 40], [30, 28]
]
df_real = pd.DataFrame(my_data, columns=['dist', 'mass'])

# 4. Создание графиков
fig = go.Figure()

# Линия теории
fig.add_trace(go.Scatter(
    x=dist_range, y=theoretical_force,
    name='Теоретическая кривая (1/d²)',
    line=dict(color='#1f77b4', width=4)
))

# Точки реальных экспериментов
fig.add_trace(go.Scatter(
    x=df_real['dist'], y=df_real['mass'],
    mode='markers',
    name='Реальные замеры (эксперимент)',
    marker=dict(size=12, color='#ff7f0e', symbol='circle', line=dict(width=2, color='white'))
))

# Рабочая точка (красный ромб)
fig.add_trace(go.Scatter(
    x=[current_dist], y=[current_force_val],
    mode='markers+text',
    name='Текущее состояние',
    text=[f"Сила: {current_force_val:.1f}г"],
    textposition="top center",
    marker=dict(size=18, color='#d62728', symbol='diamond')
))

# Настройка осей и стиля
fig.update_layout(
    height=600,
    xaxis_title="Расстояние между магнитами d (мм)",
    yaxis_title="Подъемная сила F (грамм)",
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    hovermode="x unified",
    template="plotly_white"
)

# 5. Вывод интерфейса
col_graph, col_info = st.columns([3, 1])

with col_graph:
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.subheader("📊 Аналитика")
    st.metric("Сила в точке", f"{current_force_val:.1f} г", delta=f"{current_force_val - mass_target:.1f} г")
    
    if current_force_val >= mass_target:
        st.success("✅ ЛЕВИТАЦИЯ")
        st.write("Магнитное поле достаточно сильное для удержания веса.")
    else:
        st.error("❌ ПАДЕНИЕ")
        st.write("Вес объекта превышает силу магнитного поля.")

st.markdown("---")
# Научный блок
col_math, col_table = st.columns(2)

with col_math:
    st.subheader("📝 Математическая модель")
    st.latex(r"F(d) = \frac{k \cdot M}{d^2}")
    st.info("Закон обратных квадратов описывает идеализированное взаимодействие магнитных полюсов.")

with col_table:
    st.subheader("📋 Данные эксперимента")
    st.table(df_real)
