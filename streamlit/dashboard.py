# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import requests
import json
from PIL import Image
import io

########################################################
# Loading images to the website
########################################################
image = Image.open("images/pret-a-depenser.png")

def main():
    @st.cache
    def chargement_data(path):
        dataframe = pd.read_csv(path)
        liste_id = dataframe['SK_ID_CURR'].tolist()
        return dataframe, liste_id



    st.title('Prêt à dépenser - Default RisK')
    st.subheader("Prédictions de scoring client et comparaison à l'ensemble des clients")

    examples_file = 'storage/dashboard_examples.csv'
    dataframe, liste_id = chargement_data(examples_file)

    st.sidebar.image(image)
    st.sidebar.markdown("🛰️ **Navigation**")

    id_input = st.sidebar.selectbox(
        'Choisissez le client que vous souhaitez visualiser',
        liste_id)

    focus_var = st.sidebar.selectbox('Choisissez la variable de focus',
                                     ['EXT_SOURCE_1',
                                      'EXT_SOURCE_2',
                                      'EXT_SOURCE_3'])

    client_infos = dataframe[dataframe['SK_ID_CURR'] == id_input].drop(
        ['SK_ID_CURR'], axis=1)
    client_infos = client_infos.to_dict('record')[0]

    if st.sidebar.button("Predict"):

        # Afficher la décision avec la probabilité
        response = requests.post(
            "https://streamlit-fastapi-app.herokuapp.com/predict",
            data=json.dumps(client_infos,
                            allow_nan=True))
        prediction = response.text

        if '1' in prediction:
            st.error('Crédit Refusé')
        else:
            st.success('Crédit Accordé')



        # # Afficher les graphes d'aide à la décision
        #col1, col2 = st.columns(2)

        st.header("Graphique d'explication")

        response = requests.post("https://streamlit-fastapi-app.herokuapp.com/get_waterfall_graph",
                                 data=json.dumps(client_infos, allow_nan=True))
        waterfall_plot = Image.open(
            io.BytesIO(response.content)).convert("RGB")
        st.image(waterfall_plot,
                   use_column_width=True)
        st.header("Positionnement du client")

        if focus_var == 'EXT_SOURCE_1':
            response = requests.post("https://streamlit-fastapi-app.herokuapp.com/get_bar_plot_1",
                                     data=json.dumps(client_infos, allow_nan=True))
            bar_plot = Image.open(io.BytesIO(response.content)).convert("RGB")
            st.image(bar_plot,
                       use_column_width=True)
        if focus_var == 'EXT_SOURCE_2':
            response = requests.post("https://streamlit-fastapi-app.herokuapp.com/get_bar_plot_2",
                                     data=json.dumps(client_infos, allow_nan=True))
            bar_plot = Image.open(io.BytesIO(response.content)).convert("RGB")
            st.image(bar_plot,
                       use_column_width=True)
        if focus_var == 'EXT_SOURCE_3':
            response = requests.post("https://streamlit-fastapi-app.herokuapp.com/get_bar_plot_3",
                                     data=json.dumps(client_infos, allow_nan=True))
            bar_plot = Image.open(io.BytesIO(response.content)).convert("RGB")
            st.image(bar_plot,
                       use_column_width=True)



if __name__ == '__main__':
    main()
