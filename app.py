"""
## Exploratory Data Analysis (EDA)

This app explores data with a widely used approach in EDA.

Author: [João Vitor F. França](https://www.linkedin.com/in/vitor-fran%C3%A7a-370945124/)\n
Source: [Github](https://github.com/jvitorfranca/Exploratory-Data-Analysis.git)
"""

import matplotlib.pyplot as plt
import missingno as msno
import streamlit as st
import seaborn as sns
import altair as alt
import pandas as pd

from loguru import logger


def correlation_plot(dataframe, method):

    cor_data = (dataframe).corr(method=method).stack().reset_index().rename(
        columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})

    cor_data['correlation_label'] = cor_data['correlation'].map(
        '{:.2f}'.format)

    base = alt.Chart(cor_data, width=600, height=600).encode(
        x='variable2:O', y='variable:O')

    text = base.mark_text().encode(text='correlation_label', color=alt.condition(alt.datum.correlation > 0.5, alt.value('white'),
                                                                                 alt.value('black')))

    cor_plot = base.mark_rect().encode(
        color='correlation:Q')

    return cor_plot + text


def main():

    st.title('Exploratory Data Analysis')
    st.markdown('Simple approach to the first exploration in a data set')
    st.image('https://media.giphy.com/media/l4KibOaou932EC7Dy/giphy.gif', width=400)
    uploaded_file = st.file_uploader(
        'Choose a dataset you want to analyse (.csv)', type='csv')

    if uploaded_file is not None:

        logger.info('Opening as dataframe')

        select_method = st.radio('Separator :', (',', ';'))

        if select_method == ';':
            dataframe = pd.read_csv(uploaded_file, sep=';')

        else:
            dataframe = pd.read_csv(uploaded_file)

        rows = st.slider('Select the number of rows you want to visualize')

        st.dataframe(dataframe.head(rows))

        st.header("Let's get started")

        st.markdown('Number of rows')
        st.write(dataframe.shape[0])

        st.markdown('Number of columns')
        st.write(dataframe.shape[1])

        dtypes = st.checkbox('Columns and its dtypes')

        if dtypes:
            st.table(dataframe.dtypes.rename('Dtypes'))

        st.subheader('Analysing NaN values')

        tabular = st.radio('Way to analyse :', ('Tabular', 'Chart'))

        nan_values = (dataframe.isna().sum() / dataframe.shape[0] * 100)

        if tabular == 'Tabular':

            st.table(nan_values.rename('% NaN Values'))

        else:

            source = pd.DataFrame({
                'Columns': nan_values.index,
                '% NaN Values': nan_values.values
            })

            c = alt.Chart(source, height=600).mark_bar().encode(
                x='% NaN Values',
                y='Columns'
            )

            st.altair_chart(c, use_container_width=True)

        st.subheader('Value Counts')

        value_counts = st.selectbox('Select a column:', dataframe.columns)

        if value_counts is not None:

            count = st.radio('Way to analyse :', ('Histogram', 'Table'))

            if count == 'Table':

                st.table(dataframe[value_counts].value_counts())

            else:

                source = pd.DataFrame({
                    'Classes': dataframe[value_counts].value_counts().index,
                    'Count': dataframe[value_counts].value_counts().values
                })

                c = alt.Chart(source, height=600).mark_bar().encode(
                    x='Classes',
                    y='Count'
                )

                st.altair_chart(c, use_container_width=True)

        st.subheader('Univariate Statistics')

        describe = st.selectbox(
            'Select the variable you want to describe:', dataframe.columns)

        if describe is not None:

            st.table(dataframe[describe].describe())

            # base = alt.Chart(dataframe)

            # bar = base.mark_bar().encode(
            #     x=alt.X(describe, bin=True, axis=None),
            #     y='count()'
            # )

            # rule = base.mark_rule(color='red').encode(
            #     x='mean({0})'.format(describe),
            #     size=alt.value(5)
            # )

            # st.altair_chart(bar + rule, use_container_width=True)

            sns.set()
            sns.distplot(dataframe[describe])

            st.pyplot()

            st.markdown('The red line represents de mean of the data')

        st.subheader('Correlation')

        correlation = st.radio('Select the method :', ('Pearson', 'Spearman'))

        if correlation == 'Pearson':

            st.write(correlation_plot(dataframe, 'pearson'))

        else:

            st.write(correlation_plot(dataframe, 'spearman'))


if __name__ == "__main__":

    main()
