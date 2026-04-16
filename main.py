Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import streamlit as st
... import plotly.graph_objects as go
... import numpy as np
... 
... st.title("Симулятор магнитного взаимодействия")
... 
... # Настройки в боковой панели
... st.sidebar.header("Параметры эксперимента")
... h_min = st.sidebar.slider("Минимальное расстояние (мм)", 1, 5, 2)
... h_max = st.sidebar.slider("Максимальное расстояние (мм)", 10, 50, 20)
... 
... # Генерация данных (модель обратных квадратов)
... h = np.linspace(h_min, h_max, 100)
... # Константа k подбирается под твои магниты
... k = 5000 
... F = k / (h**2)
... 
... # Создание графика через Plotly
... fig = go.Figure()
... fig.add_trace(go.Scatter(x=h, y=F, mode='lines', name='Сила F(h)'))
... 
... fig.update_layout(
...     xaxis_title="Расстояние h (мм)",
...     yaxis_title="Сила отталкивания F (мН)",
...     template="plotly_white"
... )
... 
... # Отображение в приложении
... st.plotly_chart(fig)
... 
