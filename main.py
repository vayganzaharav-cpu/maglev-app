import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Настройка страницы
st.set_page_config(page_title="Maglev Research Lab", layout="wide")

st.title("🔬 Исследование магнитной левитации (Maglev)")
st.markdown("---")

# 2. Панель управления в боковой колонке
with st.sidebar:
    st.header("⚙️ Параметры системы")
    
    with st.expander("🧲 Свойства магнита", expanded=True):
        magnet_power = st.slider("Мощность магнита (M)", 0.1, 50.0, 10.0, step=0.5)
        k_factor = st.number_input("Коэффициент калибровки (k)", value=500)

    with st.expander("📐 Условия эксперимента", expanded=True):
        mass_target = st.number_input("Масса объекта (г)", value=45)
        current_dist = st.slider("Текущий зазор (мм)", 1, 80, 25)

# 3. Математические расчеты
dist_range = np.linspace(2, 100, 400)
theoretical_force = (k_factor * magnet_power) / (dist_range**2)
current_force_val = (k_factor * magnet_power) / (current_dist**2)

# 4. Визуализация (График)
fig = go.Figure()

# Теоретическая кривая
fig.add_trace(go.Scatter(
    x=dist_range, y=theoretical_force,
    name='Теоретическая кривая силы',
    line=dict(color='#1f77b4', width=4)
))

# Рабочая точка (Текущий замер)
fig.add_trace(go.Scatter(
    x=[current_dist], y=[current_force_val],
    mode='markers+text',
    name='Текущее состояние',
    text=[f"{current_force_val:.1f}г"],
    textposition="top center",
    marker=dict(size=18, color='#d62728', symbol='diamond')
))

fig.update_layout(
    height=600,
    xaxis_title="Расстояние между магнитами d (мм)",
    yaxis_title="Подъемная сила F (грамм)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
)

# 5. Вывод интерфейса
col_graph, col_info = st.columns([3, 1])

with col_graph:
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.subheader("📊 Аналитика")
    st.metric("Сила в точке", f"{current_force_val:.1f} г", 
              delta=f"{current_force_val - mass_target:.1f} г")
    
    if current_force_val >= mass_target:
        st.success("✅ ЛЕВИТАЦИЯ")
    else:
        st.error("❌ ПАДЕНИЕ")

st.markdown("---")

# Математический блок
st.subheader("📝 Математическая модель")
st.latex(r"F = \frac{k \cdot M}{d^2}")
st.info("Модель построена на основе закона обратных квадратов.")
