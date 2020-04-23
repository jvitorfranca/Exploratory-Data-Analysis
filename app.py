"""
## Exploratory Data Analysis (EDA)

This app explores data with a widely used approach in EDA.

Author: [João Vitor F. França](https://www.linkedin.com/in/vitor-fran%C3%A7a-370945124/)\n
Source: [Github](https://github.com/jvitorfranca/Exploratory-Data-Analysis.git)
"""

import streamlit as st
import pandas as pd

from loguru import logger


def main():
    st.title('Exploratory Data Analysis')
    st.markdown('Simple approach to the first exploration in a data set')
    uploaded_file = st.file_uploader(
        'Choose a dataset you want to analyse (.csv)', type='csv')
    if uploaded_file is not None:

        logger.info('Opening as dataframe')

        dataframe = pd.read_csv(uploaded_file)

        rows = st.slider('Select the number of rows you want to visualize')

        st.write(dataframe.head(rows))

        st.header("Let's get started")

        st.markdown('Number of rows')
        st.write(dataframe.shape[0])

        st.markdown('Number of columns')
        st.write(dataframe.shape[1])

        st.markdown('Columns and its dtypes')
        dtypes = dataframe.dtypes
        st.write(dtypes)


if __name__ == "__main__":

    main()
