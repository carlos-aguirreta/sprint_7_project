import streamlit as st
import pandas as pd
import plotly.express as px

st.header('Analisis Exploratorio de Datos de Vehiculos Usados')

#-------Carga inicial de los datos-------
data = pd.read_csv('vehicles_us.csv')
with st.expander('Vista previa de los datos'):
    st.write(data.head(50))

#-------Cargar histograma-------
st.subheader('Distribución de los precios de los vehículos')
if st.button('Ver distribución de precios'): #Crear boton que al hacer clic muestre el histograma
    price_histogram = px.histogram(data, x='price', nbins=50)
    st.plotly_chart(price_histogram)

st.divider()

#-------Creación de diagrama de dispersión-------
st.subheader('Relación entre el precio y el kilometraje de los vehículos') 
if st.button('Ver relación precio-kilometraje'): #Crear boton que al hacer clic muestre el diagrama
    scatter_plot = px.scatter(data, x='odometer', y='price', title='Precio vs Kilometraje', trendline='ols')
    st.plotly_chart(scatter_plot)

st.divider()

#-------Creación de diagrama dinámico-------
st.subheader('Diagráma dinámico condición del vehículo')

#1. Separar la data por condición del vehiculo
data_by_condition = data.groupby('condition').size().reset_index(name='count')
unique_conditions = data_by_condition['condition'].unique()

#2. Lista para almacenar los DataFrames de las condiciones seleccionadas
selected_data_list = []
selected_conditions = []

#3. Crear los checkbox para mostrar las condiciones de vehiculo seleccionado(s):

st.write("Selecciona el estado del vehiculo:")

for i, condition in enumerate(unique_conditions): # Usaremos un loop en lugar de copiar y pegar para condition1, condition2, etc.
    default_value = (i == 0) # la primer condición es True por defecto
    
    if st.checkbox(f'{condition}', value=default_value, key=f'condition_{i}'):
        # Si el checkbox está seleccionado, filtramos los datos y los guardamos
        condition_data = data[data['condition'] == condition]
        selected_data_list.append(condition_data)
        selected_conditions.append(condition)


#4 Verificar si hay datos seleccionados y graficar

if selected_data_list:
    combined_data = pd.concat(selected_data_list)# Concatenar todos los DataFrames seleccionados en uno solo
    
    st.subheader(f"Distribución de precios para: {', '.join(selected_conditions)}")
    
    #5. Crear un solo histograma usando Plotly Express
    combined_histogram = px.histogram(
        combined_data, 
        x='price', 
        color='condition', #Crea un histograma de colores múltiples
        nbins=50, 
        title='Distribución de Precios por Condición de Vehículos',
        barmode='overlay'
    )
    
    combined_histogram.update_traces(opacity=0.85) # Ajustar la opacidad
    
    #6. Mostrar el gráfico
    st.plotly_chart(combined_histogram, use_container_width=True)
    
else:
    st.warning("Por favor, selecciona al menos un color para mostrar el histograma.")
