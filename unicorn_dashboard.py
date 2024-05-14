import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./unicorns.csv')  

df['Date Joined'] = pd.to_datetime(df['Date Joined'])
df['Valuation ($B)'] = df['Valuation ($B)'].str.replace('$', '').astype(float)
df['Year Joined'] = df['Date Joined'].dt.year

st.title('Unicorn Companies Dashboard')

page = st.sidebar.selectbox('Choose a page', ['Investor Insights', 'Geographical and Industrial Insights'])

if page == 'Investor Insights':
    st.header('Investor Insights')

    df['Select Investors'] = df['Select Investors'].astype(str)
    investors = df['Select Investors'].str.split(', ', expand=True).stack().value_counts()
    top_10_investors = investors.head(10)

    selected_investor = st.selectbox('Select an Investor', top_10_investors.index)

    investor_data = df[df['Select Investors'].str.contains(selected_investor)]
    companies_funded = len(investor_data)
    total_valuation = investor_data['Valuation ($B)'].sum()

    st.write(f"{selected_investor} has funded {companies_funded} companies with a total valuation of ${total_valuation} billion.")

    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    sns.barplot(x=top_10_investors.index, y=top_10_investors.values, ax=axs[0], palette='viridis')
    axs[0].set_title('Number of Companies Invested In')
    axs[0].set_xlabel('Investor')
    axs[0].set_ylabel('Number of Companies')
    axs[0].tick_params(axis='x', rotation=45)

    sns.barplot(x=top_10_investors.index, y=[df[df['Select Investors'].str.contains(inv)]['Valuation ($B)'].sum() for inv in top_10_investors.index], ax=axs[1], palette='rocket')
    axs[1].set_title('Total Valuation of Investments')
    axs[1].set_xlabel('Investor')
    axs[1].set_ylabel('Valuation ($B)')
    axs[1].tick_params(axis='x', rotation=45)

    st.pyplot(fig)

elif page == 'Geographical and Industrial Insights':
    st.header('Geographical and Industrial Insights')

    countries = df['Country'].unique()
    selected_country = st.selectbox('Select a Country', countries)

    country_data = df[df['Country'] == selected_country]
    unicorns_per_year = country_data.groupby('Year Joined').size()

    fig, ax = plt.subplots()
    sns.lineplot(data=unicorns_per_year, marker='o', ax=ax)
    ax.set_title(f'Unicorn Companies per Year in {selected_country}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Companies')
    st.pyplot(fig)

    pivot_data = country_data.pivot_table(index='Year Joined', columns='Industry', values='Valuation ($B)', aggfunc='count', fill_value=0)
    fig, ax = plt.subplots()
    sns.heatmap(pivot_data, cmap='coolwarm', annot=True, ax=ax)
    ax.set_title(f'Industry Distribution in {selected_country}')
    st.pyplot(fig)


