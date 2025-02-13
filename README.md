# Game Analytics: Unlocking Tennis Data with SportRadar API
An end-to-end sports analytics solution that extracts, stores, and visualizes tennis data from the SportRadar API.
This project leverages Python for API integration, SQL for structured data storage, and Streamlit for an interactive user interface.

### Project Description
-- Extracts tennis competition and complex data from the SportRadar API.
-- Transforms nested JSON responses into a flat, relational schema.
-- Stores structured data in a SQL database.
-- Visualizes and analyzes data using a Streamlit web application.

## Technologies Used
-- Python: For API integration, data extraction, and scripting.
-- SQL   : For database design and efficient data querying (PostgreSQL).
-- Streamlit: For building an interactive dashboard and user interface.
-- SportRadar API: For accessing comprehensive tennis data

#### Architecture and Approach
# Data Extraction:
-- Parse JSON responses from the SportRadar API endpoints for competitions, complexes, and doubles competitor rankings.
-- Transform nested JSON structures into a flat relational schema.

## Data Storage:
--  Design a SQL database schema with tables for Categories, Competitions, Complexes, Venues, Competitor Rankings, and Competitors.
--  Utilize foreign key relationships to maintain data integrity.

### Data Analysis:
--  Execute SQL queries to list competitions with categories, count events, filter by type (e.g., 'doubles'), and more.

## Streamlit Application:
-- Connect to the SQL database to display real-time query results.
-- Provide interactive dashboards with filters and detailed data views.

# Application Features
# Dashboard:
    -- Provides summary statistics such as total competitors, number of countries represented, and the highest points scored.

##  Search & Filter:
    -- Allows users to search competitors by name and filter based on rank range, country, or points threshold.

## Competitor Details Viewer:
    -- Displays detailed information including rank, movement, competitions played, and country.

## Country-Wise Analysis:
    -- Aggregates and displays competitor data by country.

## Leaderboards:
    -- Presents tables for top-ranked competitors and those with the highest points.

## Interactive Visualizations:
    -- Real-time data display with tables, charts, and dashboards using Streamlit.
