from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pymongo import MongoClient
from collections import Counter
import pandas as pd

# replace here with your mongodb url 
uri = "mongodb+srv://alexandrubites:IrvingConde@centeno.naivyqx.mongodb.net/?retryWrites=true&w=majority"

# Connect to meme MongoDB database

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.bdnosql
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

# streamlit run streamlit-mongo.py --server.enableCORS false --server.enableXsrfProtection false

st.title("Visualizacion de MongoDB")
# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    items = db.bdnosql_reactions.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_data()

def mostrar():
    listasdb = db.bdnosql_reactions.distinct("reactionId")
    listasdb = list(listasdb)
    return listasdb

print(mostrar())

items = get_data()

sidebar = st.sidebar
sidebar.title("Vladimir Alexander Garcia")
sidebar.write("Matricula: S18003199")
sidebar.write("zS180031999@estudiantes.uv.mx")
sidebar.markdown("_")
sidebar.image("Yo1.jpg")

#    
agree = sidebar.checkbox("Ver resultados raw (json) ? ")
if agree:
    st.header("Resultados...")
    st.write(items)
    st.markdown("_")

sidebar.markdown("_")
sidebar.markdown("Reacciones")
#
agree = sidebar.checkbox("Tabla de reactions")
if agree:
    st.subheader("Reactions...")
    st.dataframe(items)
    st.markdown("_")

############### reactions ################
if st.sidebar.checkbox('Grafica de barras reactions'):

    collection = db['bdnosql_reactions']
    registros = collection.find()

    # Obtener los "reactionId" y contar la cantidad de cada uno
    reaction_ids = [registro['reactionId'] for registro in registros]
    contador_reaction_ids = Counter(reaction_ids)

    # Obtener los datos para la gráfica
    reaction_ids_list = list(contador_reaction_ids.keys())
    cantidad_list = list(contador_reaction_ids.values())

    # Crear la gráfica de barras con Plotly
    fig = go.Figure(data=[go.Bar(x=reaction_ids_list, y=cantidad_list)])

    # Configurar el diseño de la gráfica
    fig.update_layout(
        title="Cantidad de reacciones por tipo",
        xaxis_title="Reaction ID",
        yaxis_title="Cantidad"
    )

    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig)
    st.markdown("_")
    
#
def reactionsDataframe():
    db = client['bdnosql']
    collection = db['bdnosql_reactions']
    documentos = collection.find()
    datos = []
    for documento in documentos:
        datos.append(documento)

    df = pd.DataFrame(datos)
    return df

datos_reactions= reactionsDataframe()

def grafico_pastel_reactions(datos_reactions):
    fig = px.pie(datos_reactions, names='reactionId')
    st.plotly_chart(fig)
def grafico_pastel_reactions(datos_reactions):
    fig = px.pie(datos_reactions, names='reactionId')
    st.plotly_chart(fig)
    
if st.sidebar.checkbox('Grafica de pastel reactions'):
    st.subheader("Cantidad de reactions por tipo, representado en gráfico de pastel:")
    grafico_pastel_reactions(datos_reactions)
    st.markdown("_")
    
################ comentarios ######################
sidebar.markdown("_")
sidebar.markdown("Comentarios")

if st.sidebar.checkbox('Tabla de comentarios'):
    st.header("Comentarios...")
    collection = db['bdnosql_comments']
    registros = collection.find()

    # Crear una lista con los campos "comment" y "objectId"
    data = [["Comentario", "Publicacion", "Usuario"]]
    for registro in registros:
        comment = registro['comment']
        objectId = registro['objectId']
        userId = registro['userId']
        data.append([comment, objectId, userId])

    # Mostrar la tabla en Streamlit
    st.table(data)
    st.markdown("_")


#histograma
def commentsDataframe():
    db = client['bdnosql']
    collection = db['bdnosql_comments']
    documentos = collection.find()
    datos = []
    for documento in documentos:
        datos.append(documento)

    df = pd.DataFrame(datos)
    return df

datos_df = commentsDataframe()

def grafico_barras_agrupadas(datos_df):
    fig = px.bar(datos_df, x='userId', y='comment', color='objectId', barmode='group')
    st.plotly_chart(fig)

if st.sidebar.checkbox('Grafica de barras comments'):
    st.header("Cantidad de comentarios por publicacion:")
    grafico_barras_agrupadas(datos_df)
    st.markdown("_")
    
def grafico_pastel_objetos(datos_df):
    fig = px.pie(datos_df, names='objectId')
    st.plotly_chart(fig)
    
if st.sidebar.checkbox('Grafica de pastel comments'):
    st.subheader("Cantidad de comentarios por publicacion:")
    grafico_pastel_objetos(datos_df)
    st.markdown("_")
    
    
############### usuarios #################
sidebar.markdown("_")
sidebar.markdown("Usuarios")

if st.sidebar.checkbox('Tabla de usuarios'):
    st.header("Usuarios...")
    collection = db['bdnosql_comments']
    registros = collection.find()

    # Crear una lista con los campos "comment" y "objectId"
    data = [["Comentario", "Usuario"]]
    for registro in registros:
        comment = registro['comment']
        userId = registro['userId']
        data.append([comment, userId])

    # Mostrar la tabla en Streamlit
    st.table(data)
    st.markdown("_")

def grafico_barras_usuarios(datos_df):
    fig = px.bar(datos_df.groupby('userId').count().reset_index(), x='userId', y='comment')
    st.plotly_chart(fig)
    
if st.sidebar.checkbox('Grafica de barras usuarios'):
    st.header("Cantidad de comentarios por usuario:")
    grafico_barras_usuarios(datos_df)
    st.markdown("_")
    
def grafico_pastel_users(datos_df):
    fig = px.pie(datos_df, names='userId')
    st.plotly_chart(fig)
    
if st.sidebar.checkbox('Grafica de pastel usuarios'):
    st.header("Cantidad de comentarios por usuario:")
    grafico_pastel_users(datos_df)
    st.markdown("_")
    
sidebar.markdown("_")