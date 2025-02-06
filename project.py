import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection
DB_URL = "postgresql://postgres:1997@localhost:5432/Project"

@st.cache_data
def load_data():
    engine = create_engine(DB_URL)
    query = """
    SELECT 
    competitors_table.competitor_id, 
    competitors_table.name, 
    competitor_rankings_table.point,  
    competitors_table.country, 
    competitors_table.country_code, 
    competitors_table.abbreviation, 
    competitor_rankings_table.rank, 
    competitor_rankings_table.movement,
    competitor_rankings_table.competitions_played
    
FROM 
    competitors_table
JOIN 
    competitor_rankings_table 
ON 
    competitors_table.competitor_id = competitor_rankings_table.competitor_id;


    """
    return pd.read_sql(query, engine)

data = load_data()

# Homepage Dashboard
st.title("Sports Competition Dashboard")
col1, col2, col3,col4 = st.columns(4)
col1.metric("Total Competitors", len(data))
col2.metric("Countries Represented", data['country'].nunique())
col3.metric("Highest Points Scored", data['point'].max())
col4.metric('Highest Rank',data['rank'].max())
st.divider()

# Sidebar Filters


search_query = st.sidebar.text_input("Search Competitor by Name")

# Apply Search Filter
filtered_data = data[data['name'].astype(str).str.contains(search_query, case=False, na=False)] if search_query else None

# Display Table Only When There Is a Search Query
if search_query and not filtered_data.empty:
    st.header("Search Results")
    st.dataframe(filtered_data[["competitor_id", "name", "point", "country", "country_code", "abbreviation", "rank", "movement"]])
elif search_query:
    st.warning("No competitor found with that name. Try a different search.")

# Sidebar Filters
st.sidebar.header("Search & Filter")

# Rank Range Filter
rank_range = st.sidebar.slider(
    "Filter by Rank", 
    int(data['rank'].min()), 
    int(data['rank'].max()), 
    (int(data['rank'].min()), int(data['rank'].max()))
)

# Points Threshold Filter
points_threshold = st.sidebar.slider(
    "Minimum Points", 
    int(data['point'].min()), 
    int(data['point'].max()), 
    
)

# Country Filter
selected_country = st.sidebar.selectbox(
    "Filter by Country", 
    ["All"] + sorted(data['country'].dropna().unique())
)

# Apply Filters (Without Search Query)
filtered_data = data[
    (data['rank'].between(*rank_range)) & 
    (data['point'] >= points_threshold)
]

if selected_country != "All":
    filtered_data = filtered_data[filtered_data['country'] == selected_country]

# Display Competitor List
st.header("Competitor List")
st.dataframe(filtered_data)

st.divider()

st.title("🏆 Competitor Details Viewer")

# Select a competitor
selected_competitor = st.selectbox("Select a Competitor", data["name"])

# Filter data for the selected competitor
competitor_details = data[data["name"] == selected_competitor].iloc[0]

# Display details
st.subheader(f"Details for {selected_competitor}")
st.write(f"**Rank:** {competitor_details['rank']}")
st.write(f"**Rank Movement:** {competitor_details['movement']}")
st.write(f"**Competitions Played:** {competitor_details['competitions_played']}")
st.write(f"**Country:** {competitor_details['country']}")

st.title("🌍 Country-Wise Analysis")

# Group by country and calculate total competitors and average points
country_analysis = data.groupby('country').agg(
    total_competitors=('name', 'count'),
    avg_points=('point', 'mean')
).reset_index()

# Display the country analysis
st.subheader("Country-wise Breakdown")
st.write(country_analysis)

st.title("🏆 Leaderboards")

# Top-ranked competitors (Sorted by rank)
top_ranked = data.sort_values(by='rank').head(5).reset_index(drop=True)

# Competitors with the highest points (Sorted by points)
highest_points = data.sort_values(by='point', ascending=False).head(5).reset_index(drop=True)

# Display the Leaderboards
st.subheader("Top-Ranked Competitors")
st.write(top_ranked[['name', 'rank', 'country']].reset_index(drop=True))

st.subheader("Competitors with Highest Points")
st.write(highest_points[['name', 'point', 'country']].reset_index(drop=True))

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection string
DB_URL = "postgresql://postgres:1997@localhost:5432/Project"

# Function to fetch data from PostgreSQL
def fetch_data(query):
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

st.divider()



import streamlit as st
import psycopg2
import pandas as pd

# Database connection details
DB_CONNECTION = "postgresql://postgres:1997@localhost:5432/Project"

# Function to execute SQL query
def run_query(query):
    with psycopg2.connect(DB_CONNECTION) as conn:
        df = pd.read_sql(query, conn)
    return df

# Streamlit UI
st.title("Sports Data Analysis")

# Select analysis type
analysis_type = st.selectbox(
    "Select Analysis Type:",
    ["Competition Analysis", "Venues Analysis", "Rank Analysis"]
)

# Show the corresponding analysis section based on the selected type
if analysis_type == "Competition Analysis":
    st.header("Competition Analysis")
    query_option = st.selectbox(
        "Choose a query to execute:",
        [
            "List all competitions with their category name",
            "Count the number of competitions in each category",
            "Find all competitions of type 'doubles'",
            "Get competitions that belong to a specific category (e.g., ITF Men)",
            "Identify parent competitions and their sub-competitions",
            "Analyze the distribution of competition types by category",
            "List all competitions with no parent (top-level competitions)"
        ]
    )

    # Query execution based on selection
    if query_option == "List all competitions with their category name":
        query = """
        SELECT c.competition_name, cat.category_name
        FROM competition_table c
        JOIN category_table cat ON c.category_id = cat.category_id;
        """
    
    elif query_option == "Count the number of competitions in each category":
        query = """
        SELECT cat.category_name, COUNT(c.competition_id) AS competition_count
        FROM category_table cat
        LEFT JOIN competition_table c ON c.category_id = cat.category_id
        GROUP BY cat.category_name;
        """
    
    elif query_option == "Find all competitions of type 'doubles'":
        query = """
        SELECT c.competition_name, c.type, cat.category_name
        FROM competition_table c
        JOIN category_table cat ON c.category_id = cat.category_id
        WHERE c.type = 'doubles';
        """
    
    elif query_option == "Get competitions that belong to a specific category (e.g., ITF Men)":
        category_query = "SELECT DISTINCT category_name FROM category_table ORDER BY category_name;"
        category_list = run_query(category_query)
        category_input = st.selectbox("Select a Category", category_list['category_name'])
        query = f"""
        SELECT c.competition_name, cat.category_name
        FROM competition_table c
        JOIN category_table cat ON c.category_id = cat.category_id
        WHERE cat.category_name = '{category_input}';
        """
    
    elif query_option == "Identify parent competitions and their sub-competitions":
       query = """SELECT 
            parent.competition_name AS parent_competition, 
            child.competition_name AS sub_competition
        FROM competition_table AS child
        JOIN competition_table AS parent 
            ON child.parent_id = parent.competition_id;

      """
    
    elif query_option == "Analyze the distribution of competition types by category":
        query = """
        SELECT cat.category_name, c.type, COUNT(c.competition_id) AS type_count
        FROM category_table cat
        JOIN competition_table c ON c.category_id = cat.category_id
        GROUP BY cat.category_name, c.type
        ORDER BY cat.category_name, c.type;
        """
    
    elif query_option == "List all competitions with no parent (top-level competitions)":
        query = """
        SELECT competition_name
        FROM competition_table
        WHERE parent_id IS NULL;
        """

if analysis_type == "Venues Analysis":
    st.title("Venues and Complexes Data Analysis")

    # Select box for SQL queries in the sidebar
    query_option = st.selectbox(
        "Choose a query to execute:",
        [
            "List all venues along with their associated complex name",
            "Count the number of venues in each complex",
            "Get details of venues in a specific country (e.g., Chile)",
            "Identify all venues and their timezones",
            "Find complexes that have more than one venue",
            "List venues grouped by country",
            "Find all venues for a specific complex (e.g., Nacional)"
        ]
        
    )

    # Query execution logic
    if query_option == "List all venues along with their associated complex name":
        query = """
        SELECT v.venues_name, c.complex_name
        FROM venues_table v
        JOIN complexes_table c ON v.complex_id = c.complex_id;
        """

    elif query_option == "Count the number of venues in each complex":
        query = """
        SELECT c.complex_name, COUNT(v.venues_id) AS venue_count
        FROM complexes_table c
        LEFT JOIN venues_table v ON v.complex_id = c.complex_id
        GROUP BY c.complex_name;
        """

    elif query_option == "Get details of venues in a specific country (e.g., Chile)":
        country_list = run_query("SELECT DISTINCT country_name FROM venues_table ORDER BY country_name;")
        #country_list2=run_query(country_list)
        country = st.selectbox("Select a Country", country_list['country_name'])
        query = f"""
        SELECT v.venues_name, v.country_name, v.timezone
        FROM venues_table v
        WHERE v.country_name = '{country}';"""

    elif query_option == "Identify all venues and their timezones":
        query = """
        SELECT v.venues_name, v.timezone
        FROM venues_table v;
        """

    elif query_option == "Find complexes that have more than one venue":
        query = """
        SELECT c.complex_name
        FROM complexes_table c
        JOIN venues_table v ON v.complex_id = c.complex_id
        GROUP BY c.complex_name
        HAVING COUNT(v.venues_id) > 1;
        """

    elif query_option == "List venues grouped by country":
        query = """
        SELECT v.country_name, COUNT(v.venues_id) AS venue_count
        FROM venues_table v
        GROUP BY v.country_name
        ORDER BY v.country_name;
        """

    elif query_option == "Find all venues for a specific complex (e.g., Nacional)":
        complex_list = run_query("SELECT DISTINCT complex_name FROM complexes_table ORDER BY complex_name;")
        complex_input = st.selectbox("Select a Complex", complex_list['complex_name'], index=0)

        query = f"""
        SELECT v.venues_name
        FROM venues_table v
        JOIN complexes_table c ON v.complex_id = c.complex_id
        WHERE c.complex_name = '{complex_input}';
        """


if analysis_type=='Rank Analysis':
    st.header("Rank Data Analysis")
    query_option = st.selectbox(
        "Choose a query to execute:",
        [
            "Get all competitors with their rank and points",
            "Find competitors ranked in the top 5",
            "List competitors with no rank movement (stable rank)",
            "Get the total points of competitors from a specific country",
            "Count the number of competitors per country",
            "Find competitors with the highest points in the current week"
        ]
    )

# Query execution based on user selection
if query_option == "Get all competitors with their rank and points":
    query = """SELECT c.name, cr."rank", cr.point 
            FROM competitors_table AS c 
            JOIN competitor_rankings_table AS cr 
            ON c.competitor_id = cr.competitor_id 
            ORDER BY cr.rank;"""

elif query_option == "Find competitors ranked in the top 5":
    query = """SELECT c.name, cr."rank", cr.point FROM competitors_table as c
            JOIN competitor_rankings_table AS cr 
            ON c.competitor_id = cr.competitor_id WHERE cr.rank <=5 ORDER BY cr.rank;"""

elif query_option == "List competitors with no rank movement (stable rank)":
    query = """SELECT c.name, cr.rank, cr.point, cr.movement
                FROM competitors_table AS c
                JOIN competitor_rankings_table AS cr 
                ON c.competitor_id = cr.competitor_id
                WHERE cr.movement = 0 
                ORDER BY cr.rank;
                                    """

elif query_option == "Get the total points of competitors from a specific country":
    # Fetch the list of countries
    country_list = run_query("SELECT DISTINCT country FROM competitors_table ORDER BY country;")
    country = st.selectbox("Select a Country", country_list['country'])

    # Query to get total points for the selected country
    query = f"""
    SELECT c.country, SUM(cr.point) AS total_points
    FROM competitors_table c
    JOIN competitor_rankings_table cr ON c.competitor_id = cr.competitor_id
    WHERE c.country = '{country}'
    GROUP BY c.country;
    """


elif query_option == "Count the number of competitors per country":
    query = "SELECT country, COUNT(competitor_id) AS competitor_count FROM competitors_table GROUP BY country ORDER BY competitor_count DESC;"

elif query_option == "Find competitors with the highest points in the current week":
    query = """
    SELECT c.name AS competitor_name, cr.rank, cr.point
    FROM competitors_table c
    JOIN competitor_rankings_table cr ON c.competitor_id = cr.competitor_id
    ORDER BY cr.point DESC
    LIMIT 1;
    """


# Execute the selected query and display the result
df = run_query(query)
st.dataframe(df)
