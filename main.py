import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("Математическая модель Maglev")
st.write("Проект: Исследование зависимости силы левитации от расстояния")

# Слайдеры для параметров
mass = st.slider("Масса магнита (г)", 1, 100, 15)
distance = st.slider("Расстояние (мм)", 1, 50, 10)

# Простая формула для графика (обратные квадраты)
x = np.linspace(1, 50, 100)
y = mass * 100 / (x**2)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, name='Теория'))
fig.add_trace(go.Scatter(x=[distance], y=[mass * 100 / (distance**2)], 
                         mode='markers', marker=dict(size=15, color='red'), name='Текущая точка'))

fig.update_layout(xaxis_title="Расстояние (мм)", yaxis_title="Сила (у.е.)")
st.plotly_chart(fig)
