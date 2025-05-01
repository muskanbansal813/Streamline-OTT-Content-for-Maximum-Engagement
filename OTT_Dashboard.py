import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------- LOGIN SETUP -----------------
USERNAME = "muskan"
PASSWORD = "Muskan@2025"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to Access Dashboard")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

    st.stop()

# ----------------- LOAD DATA -----------------

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("content_data.csv")  # Replace with your CSV file name

df = load_data()

# Title
st.markdown(
    """
    <h1 style='text-align: center; color: #7a3776; font-family: "Cambria", sans-serif; font-size: 44px;'>
        Streamline OTT Content for Maximum Engagement
    </h1>
    """, 
    unsafe_allow_html=True
)

# Sidebar filters
st.sidebar.header("🔍 Filters")
content_type_options = ["All"] + sorted(df["Content Type"].dropna().unique())
genre_options = ["All"] + sorted(df["Genre"].dropna().unique())
seasonality_options = ["All"] + sorted(df["Seasonality"].dropna().unique())


content_type = st.sidebar.selectbox("Content Type", content_type_options)
genre = st.sidebar.selectbox("Genre", genre_options)
seasonality = st.sidebar.selectbox("Seasonality", seasonality_options)

# Apply filters
filtered_df = df.copy()
if seasonality != "All":
    filtered_df = filtered_df[filtered_df["Seasonality"] == seasonality]
if content_type != "All":
    filtered_df = filtered_df[filtered_df["Content Type"] == content_type]
if genre != "All":
    filtered_df = filtered_df[filtered_df["Genre"] == genre]

# Display current filters
st.markdown(f"<h4 style='text-align: center; color: #af7bbd;'>Filtered By → Seasonality: `{seasonality}`, Content Type: `{content_type}`, Genre: `{genre}`</h4>", unsafe_allow_html=True)

# ---- DASHBOARD VISUALS ----

# 1. Top 5 Genres by Viewership
st.subheader("1️⃣ Top 5 Genres by Viewership")
genre_viewership = filtered_df['Genre'].value_counts().nlargest(5)
genre_viewership_rounded = genre_viewership.round(2)  # Round to 2 decimal places
fig1 = px.bar(genre_viewership_rounded, 
              x=genre_viewership_rounded.index,  # x-axis will be the genre names
              y=genre_viewership_rounded.values,  # y-axis will be the count of viewership
              color=genre_viewership_rounded.values,  # Color based on the actual values (viewership count)
              color_discrete_sequence=['#741b48'])  # Choose a continuous color scale

fig1.update_layout(
    title="Top 5 Genres by Viewership", 
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    xaxis_title="Genre", yaxis_title="Viewership", 
    xaxis_tickangle=45
)

# Add data labels
fig1.update_traces(text=genre_viewership_rounded.values, textposition='auto')

# Display the plot
st.plotly_chart(fig1)

# 2. Content Type by Viewership
st.subheader("2️⃣ Content Type by Viewership")
content_viewership = filtered_df['Content Type'].value_counts()
content_viewership_rounded = content_viewership.round(2)  # Round to 2 decimal places
fig2 = px.pie(values=content_viewership_rounded.values, names=content_viewership_rounded.index, title='Viewership by Content Type',
              color_discrete_sequence=px.colors.diverging.Tealrose)
fig2.update_traces(textinfo='percent', pull=[0.1, 0.1, 0.1])  # Add pull effect to highlight
st.plotly_chart(fig2, use_container_width=True)

# 3. Average Watch Time by Seasonality
st.subheader("3️⃣ Average Watch Time by Seasonality")
avg_watch_time_seasonality = filtered_df.groupby('Seasonality')['Average Watch Time (mins)'].mean().sort_values(ascending=False)
avg_watch_time_seasonality_rounded = avg_watch_time_seasonality.round(2)  # Round to 2 decimal places
fig3 = px.bar(x=avg_watch_time_seasonality_rounded.index, y=avg_watch_time_seasonality_rounded.values, 
              labels={'x': 'Seasonality', 'y': 'Average Watch Time (mins)'}, title='Average Watch Time by Seasonality',
              color_discrete_sequence=['#af77bd'])
# Add data labels
fig3.update_traces(text=avg_watch_time_seasonality_rounded.values, textposition='auto')

st.plotly_chart(fig3, use_container_width=True)

# 4. Engagement Rate by Content Type and Viewer Age
st.subheader("4️⃣ Engagement Rate Analysis")
filtered_df['Engagement Rate'] = filtered_df['Average Watch Time (mins)'] / filtered_df['Duration (mins)']
engagement_df = filtered_df.groupby(['Content Type', 'Viewer Age'])['Engagement Rate'].mean().reset_index()
engagement_df['Engagement Rate'] = engagement_df['Engagement Rate'].round(2)  # Round to 2 decimal places
fig_engagement = px.bar(engagement_df, x='Content Type', y='Engagement Rate', color='Viewer Age', barmode='group', 
                        title='Engagement Rate by Content Type and Viewer Age', color_discrete_sequence=px.colors.qualitative.Set2)
# Add data labels
fig_engagement.update_traces(text=engagement_df['Engagement Rate'], textposition='auto')

st.plotly_chart(fig_engagement, use_container_width=True)

# 5. Gender Analysis by Viewership
st.subheader("5️⃣ Gender Analysis by Viewership")
gender_viewership = filtered_df['Viewer Gender'].value_counts()
gender_viewership_rounded = gender_viewership.round(2)  # Round to 2 decimal places
fig4 = px.pie(values=gender_viewership_rounded.values, names=gender_viewership_rounded.index, title='Viewership by Gender',
              color_discrete_sequence=['#2083bd'])
fig4.update_traces(textinfo='percent')  # Fixed the error
st.plotly_chart(fig4, use_container_width=True)

# 6. Promotion Analysis by Viewership
st.subheader("6️⃣ Promotion by Viewership")
promo_viewership = filtered_df['Promotion Data'].value_counts()
promo_viewership_rounded = promo_viewership.round(2)  # Round to 2 decimal places
fig5 = px.bar(x=promo_viewership_rounded.index, y=promo_viewership_rounded.values, labels={'x': 'Promotion Applied', 'y': 'Viewership'},
              title='Viewership by Promotion Applied', color_discrete_sequence=['#d577a5'])
# Add data labels
fig5.update_traces(text=promo_viewership_rounded.values, textposition='auto')

st.plotly_chart(fig5, use_container_width=True)

# 7. Top 5 Locations by Genre
st.subheader("7️⃣ Top 5 Locations by Viewership")
location_genre = filtered_df.groupby('Viewer Location')['Viewership'].sum().nlargest(5)
location_genre_rounded = location_genre.round(2)  # Round to 2 decimal places

# Create the bar chart with custom color
fig7 = px.bar(location_genre_rounded, 
              x=location_genre_rounded.index, 
              y=location_genre_rounded.values, 
              labels={'x': 'Viewer Location', 'y': 'Sum of Viewership'},
              title='Top 5 Locations by Viewership',
              color_discrete_sequence=['#008ca6'])  # Custom color

# Add data labels
fig7.update_traces(text=location_genre_rounded.values, textposition='auto')

# Display the chart
st.plotly_chart(fig7, use_container_width=True)

# 8. Subscription Data by Month
st.subheader("8️⃣ Subscription Data by Month")
if "Subscription Data" in filtered_df.columns and "Release Date" in filtered_df.columns:
    filtered_df["Release Date"] = pd.to_datetime(filtered_df["Release Date"])
    filtered_df["Month"] = filtered_df["Release Date"].dt.month_name()
    filtered_df = filtered_df[filtered_df["Month"].isin(["July", "August", "September"])]
    subscription_data = filtered_df.groupby("Month")["Subscription Data"].sum().reset_index()
    month_order = ["July", "August", "September"]
    subscription_data["Month"] = pd.Categorical(subscription_data["Month"], categories=month_order, ordered=True)
    subscription_data = subscription_data.sort_values("Month")
    subscription_data["Subscription Data"] = subscription_data["Subscription Data"].round(2)  # Round to 2 decimal places
    fig7 = px.bar(subscription_data, x="Month", y="Subscription Data", 
                  title="Subscription Data by Month (Number of Subscriptions)", 
                  color="Month", color_discrete_sequence=px.colors.qualitative.Set2)
    # Add data labels
    fig7.update_traces(text=subscription_data["Subscription Data"], textposition='auto')

    st.plotly_chart(fig7, use_container_width=True)
else:
    st.warning("⚠️ 'Subscription Data' or 'Release Date' column is missing.")

# 9. Viewership by Content Popularity (Donut Chart)
st.subheader("9️⃣  Viewership by Content Popularity")
if "Content Popularity" in filtered_df.columns and "Viewership" in filtered_df.columns:
    viewership_by_popularity = filtered_df.groupby("Content Popularity")["Viewership"].sum().reset_index()
    viewership_by_popularity["Viewership"] = viewership_by_popularity["Viewership"].round(2)  # Round to 2 decimal places
    fig8 = px.pie(viewership_by_popularity, names="Content Popularity", values="Viewership", 
                  title="Viewership by Content Popularity", hole=0.3, 
                  color_discrete_sequence=px.colors.sequential.Purp)
    st.plotly_chart(fig8, use_container_width=True)
else:
    st.warning("⚠️ 'Content Popularity' or 'Viewership' column is missing.")

# 10. Average Rating by Viewer Age
st.subheader("🔟 Average User Rating by Viewer Age")
avg_rating_age = filtered_df.groupby('Viewer Age')['User Ratings'].mean().sort_values(ascending=False)
avg_rating_age_rounded = avg_rating_age.round(2)  # Round to 2 decimal places
fig9 = px.bar(x=avg_rating_age_rounded.index, y=avg_rating_age_rounded.values, labels={'x': 'Viewer Age', 'y': 'Average Rating'}, 
              title='Average Rating by Viewer Age Group', color_discrete_sequence=['#5479a2'])
# Add data labels
fig9.update_traces(text=avg_rating_age_rounded.values, textposition='auto')

st.plotly_chart(fig9, use_container_width=True)
