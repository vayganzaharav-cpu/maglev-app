import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Настройка страницы
st.set_page_config(page_title="Maglev Dynamic Model", layout="wide")

st.title("🧲 Динамическая модель магнитного поля")
st.markdown("---")

# 2. Управление в боковой панели
with st.sidebar:
    st.header("⚙️ Настройки")
    
    # Изменение мощности магнита теперь перестраивает всю функцию
    magnet_power = st.slider("Мощность магнита (M)", 0.5, 100.0, 15.0, step=0.5)
    k_factor = st.number_input("Коэффициент (k)", value=500)
    
    st.markdown("---")
    mass_target = st.number_input("Масса груза (г)", value=50)
    current_dist = st.slider("Расстояние (мм)", 1, 100, 20)

# 3. Расчеты
# Генерируем значения для всей гиперболы
d_axis = np.linspace(2, 100, 500)
# F = (k * M) / d^2
f_axis = (k_factor * magnet_power) / (d_axis**2)

# Сила в конкретной выбранной точке
f_at_point = (k_factor * magnet_power) / (current_dist**2)

# 4. Построение графика
fig = go.Figure()

# Основная динамическая гипербола
fig.add_trace(go.Scatter(
    x=d_axis, 
    y=f_axis,
    name='Кривая силы F(d)',
    line=dict(color='#1f77b4', width=4),
    fill='tozeroy', # Заливка под графиком для наглядности зоны влияния
    fillcolor='rgba(31, 119, 180, 0.1)'
))

# Порог массы (горизонтальная линия)
fig.add_trace(go.Scatter(
    x=d_axis, 
    y=[mass_target]*len(d_axis),
    name='Вес груза (порог)',
    line=dict(color='green', width=2, dash='dash')
))

# Точка текущего замера
fig.add_trace(go.Scatter(
    x=[current_dist], 
    y=[f_at_point],
    mode='markers+text',
    name='Текущий замер',
    text=[f"{f_at_point:.1f} г"],
    textposition="top right",
    marker=dict(size=15, color='red', symbol='circle', line=dict(width=2, color='white'))
))

fig.update_layout(
    height=600,
    xaxis_title="Расстояние d (мм)",
    yaxis_title="Сила левитации F (г)",
    yaxis_range=[0, max(mass_target * 1.5, f_at_point * 1.2)], # Автомасштаб
    template="plotly_white",
    hovermode="x unified"
)

# 5. Интерфейс
col_graph, col_stats = st.columns([3, 1])

with col_graph:
    st.plotly_chart(fig, use_container_width=True)

with col_stats:
    st.subheader("📊 Данные")
    st.metric("Сила магнита", f"{f_at_point:.1f} г")
    st.metric("Вес груза", f"{mass_target} г")
    
    delta = f_at_point - mass_target
    if delta >= 0:
        st.success(f"Левитация: ДА (+{delta:.1f} г)")
    else:
        st.error(f"Левитация: НЕТ ({delta:.1f} г)")

st.markdown("---")
st.latex(r"F(d) = \frac{k \cdot M}{d^2}")
st.info("При изменении мощности (M) меняется форма всей кривой, а не только положение точки.")
