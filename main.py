import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Maglev Pro Model", layout="wide")

st.title("🧲 Расширенная модель магнитной левитации")
st.write("В этой версии увеличен предел мощности магнита для тестирования сильных полей.")

# Боковая панель
st.sidebar.header("Настройки симуляции")
# Увеличили max_value до 50.0
magnet_power = st.sidebar.slider("Сила магнита (M)", 0.1, 50.0, 5.0, step=0.1)
mass_target = st.sidebar.slider("Масса груза (г)", 1, 500, 50)
current_dist = st.sidebar.slider("Текущее расстояние (мм)", 1, 100, 20)

# Константа (можно менять для калибровки под реальные весы)
k = 500 

# Расчет
distances = np.linspace(1, 120, 300) 
force_line = (k * magnet_power) / (distances**2)
current_force = (k * magnet_power) / (current_dist**2)

# График
fig = go.Figure()

# Теоретическая кривая
fig.add_trace(go.Scatter(x=distances, y=force_line, name='Магнитная сила', line=dict(color='blue', width=3)))

# Линия массы (порог)
fig.add_trace(go.Scatter(x=distances, y=[mass_target]*len(distances), name='Вес груза', line=dict(color='green', dash='dash')))

# Точка замера
fig.add_trace(go.Scatter(
    x=[current_dist], y=[current_force],
    mode='markers+text',
    name='Рабочая точка',
    text=[f"{current_force:.1f} г"],
    textposition="top right",
    marker=dict(size=15, color='red', symbol='diamond')
))

fig.update_layout(
    xaxis_title="Расстояние (мм)",
    yaxis_title="Сила удержания (г)",
    yaxis_range=[0, mass_target * 2 if current_force < mass_target * 2 else current_force * 1.2],
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Индикаторы
col1, col2 = st.columns(2)
with col1:
    st.metric("Сила в точке", f"{current_force:.1f} г")
with col2:
    if current_force >= mass_target:
        st.success("УДЕРЖИТ")
    else:
        st.error("УПАДЕТ")

st.latex(r"F = \frac{k \cdot M}{d^2}")
