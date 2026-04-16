import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Maglev Model", layout="wide")

st.title("🧲 Интерактивная модель магнитной левитации")
st.write("Эта модель показывает, как сила магнита и расстояние влияют на способность удерживать груз.")

# Боковая панель с настройками
st.sidebar.header("Параметры системы")
magnet_power = st.sidebar.slider("Сила (мощность) магнита", 0.1, 5.0, 1.0, help="Магнитная индукция в условных единицах")
mass_target = st.sidebar.slider("Масса груза (г)", 1, 100, 20)
current_dist = st.sidebar.slider("Текущее расстояние (мм)", 1, 50, 15)

# Константа пропорциональности
k = 500 

# Расчет данных для графика
distances = np.linspace(2, 60, 200) # Расстояние от 2 до 60 мм
# Формула: Сила = (Константа * Сила магнита) / Расстояние^2
force_line = (k * magnet_power) / (distances**2)

# Расчет текущей силы в выбранной точке
current_force = (k * magnet_power) / (current_dist**2)

# Создание графика
fig = go.Figure()

# Линия теоретической силы
fig.add_trace(go.Scatter(
    x=distances, y=force_line, 
    name='Кривая силы',
    line=dict(color='blue', width=3)
))

# Точка текущего положения
fig.add_trace(go.Scatter(
    x=[current_dist], y=[current_force],
    mode='markers+text',
    name='Ваше положение',
    text=[f"{current_force:.1f} г"],
    textposition="top right",
    marker=dict(size=15, color='red', symbol='diamond')
))

# Линия веса груза (горизонтальная)
fig.add_trace(go.Scatter(
    x=distances, y=[mass_target]*len(distances),
    name='Вес груза (порог левитации)',
    line=dict(color='green', dash='dash')
))

fig.update_layout(
    xaxis_title="Расстояние d (мм)",
    yaxis_title="Удерживающая сила F (г)",
    hovermode="x unified"
)

# Вывод графика
st.plotly_chart(fig, use_container_width=True)

# Научный вывод
st.subheader("Математическая справка")
st.latex(r"F \approx \frac{k \cdot M}{d^2}")
st.write(f"При силе магнита **{magnet_power}** и расстоянии **{current_dist} мм**, система может удерживать до **{current_force:.1f} грамм**.")

if current_force >= mass_target:
    st.success("✅ Левитация возможна! Магнитная сила превышает вес груза.")
else:
    st.error("❌ Груз упадет. Магнитная сила слишком слаба для такого расстояния.")
