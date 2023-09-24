import streamlit as st
import plotly.express as px
import seaborn as sns

st.title("plotly")
df = sns.load_dataset("titanic")
fig = px.box(df, x='class', y = 'age')
st.plotly_chart(fig)
# df = px.data.gapminder().query("continent == 'Oceania'")
# fig = px.line(df, x='year', y='lifeExp', color='country', markers=True)
# fig.show()


# data_canada = px.data.gapminder().query("country == 'Canada'")
# fig = px.bar(data_canada, x='year', y='pop')
# fig.show()


# long_df = px.data.medals_long()

# fig = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")
# fig.show()