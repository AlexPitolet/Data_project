# Electricity and gas Consumption Dashboard – France (2011–2024)

This project is an interactive dashboard developed as part of the **E3 FI – Multidisciplinary Project 1** at **ESIEE Paris**. 
It focuses on the analysis and visualization of energy consumption in France between **2011 and 2024** through an interactive map, at both **regional** and **departmental** levels.

The dashboard is built using **Python**, **Dash**, and **Plotly-express**, and aims to provide clear insights into geographical and temporal disparities in electricity / gas usage.

---

## User Guide

To run the dashboard locally:

1. Clone the repository
2. Create and activate a virtual environment
3. Install the dependencies inside the virtual environment:
   pip install -r requirements.txt
4. Launch the app with python run main.py
5. Open an internet browser and go to http://127.0.0.1:8050

### The dashboard includes:
- A geographical map of electricity consumption (region / department) with interactive controls (year, scale, type of consumption)
- A dynamic histogram based on a categorical variable with interactive frame animation
- A non-categorical histogram showing the distribution of consumption across communes
"- Data analysis for each graphic"
- Several explanatory pages (Home, About)

#### Interactive Features

**Both Histograms:**
- **Zoom** : Select an area with your mouse to zoom into that region of the graph
- **Reset** : Double-click on the graph to reset the view to its default state (useful if visualization becomes unclear)

**Non-Categorical Histogram (`Total Energy Consumption Distribution`):**
- **Year Slider** : Move the cursor to select the year to observe
- Displays the distribution of consumption across communes for the selected year

**Dynamic Histogram (`Dynamic Energy Consumption by Region`):**
- **Animation Controls** : At the bottom of the graph, a control bar allows you to :
  - Play/Pause automatic animation (play/pause button)
  - Navigate manually between years by dragging the cursor
- **Year Slider (left panel)** : Allows manual selection of the year
- **Metric Dropdown (left panel)** : Choose between "National Average", "Minimum Consumption", or "Maximum Consumption"
- **KPI (left panel)** : Displays the value of the selected metric for the current year

**Known Behavior** : When you move the slider or change the dropdown, the animation frame returns to the year 2011 by default (even though the animation bar may not visually reflect this). This is due to the internal handling of Dash callbacks.

## Data
The data used in this project comes from public open data sources under the Apache 2.0 license.
It describes the annual electricity and gas consumption in France at the municipal level.

Dataset source:
https://www.data.gouv.fr/datasets/consommation-annuelle-delectricite-et-gaz-par-commune

The data processing pipeline follows this structure:
- data/raw/ → original datasets
- data/cleaned/ → cleaned and aggregated datasets (department & region levels). Keeping only useful datas to ligthen the dashboard.

## Developper Guide

Data_project/\
│\
├── data/\
│   ├── raw/                # Raw datasets downloaded from open data sources\
│   └── cleaned/            # Cleaned and aggregated datasets used by the dashboard\
│\
├── src/\
│   ├── pages/              # Dashboard pages (multi-page Dash app)\
│   │   ├── __init__.py\
│   │   ├── home.py\
│   │   ├── map.py\
│   │   ├── hist.py\
│   │   ├── dynamic.py\
│   │   └── about.py\
│   │\
│   ├── components/         # Reusable UI components\
│   │   ├── __init__.py\
│   │   ├── header.py\
│   │   ├── footer.py\
│   │   └── navbar.py\
│   │\
│   ├── utils/              # Data pipeline and utility functions\
│   │   ├── __init__.py\
│   │   ├── get_data.py     # Data download and availability check\
│   │   ├── clean_data.py   # Data cleaning and aggregation\
│   │   └── common_functions.py  # Shared data selection logic\
│   │\
│   └── __init__.py\
│\
├── main.py                 # Entry point of the Dash application\
├── requirements.txt        # Project dependencies\
└── README.md               # Project documentation\

### Data pipeline
The data pipeline is divided into two main steps:
1. Data acquisition
    - Implemented in src/utils/get_data.py
    - Downloads or verifies the presence of raw datasets
    - Stores files in data/raw/
    - Ensures reproducibility of the project
2. Data cleaning and aggregation
    - Implemented in src/utils/clean_data.py
    - Filters useful columns
    - Aggregates data at commune, department, and region levels
    - Outputs cleaned CSV files in data/cleaned/
    - This separation allows the dashboard to rely only on lightweight, preprocessed datasets.

### Dashboard architecture
The application is a multi-page Dash dashboard:
- main.py initializes the Dash app and handles page routing using dcc.Location
- Each page in src/pages/ defines:
    - Its own layout
    - Its own callbacks via a register_callback(app) function
- This design avoids callback conflicts and keeps each page independent

## Rapport d'analyse
The dashboard highlights strong geographical disparities in electricity consumption across France.

Key observations:
- Highly urbanized and densely populated areas show significantly higher electricity consumption.

- Major metropolitan regions and industrial areas appear as the darkest zones on the map.

- Rural and less industrialized departments display lower consumption levels.

- Switching from a regional to a departmental scale reveals important intra-regional disparities.

These differences can be explained by a combination of factors:
- Population density

- Industrial activity

- Urbanization level

- Tertiary sector concentration

- Energy usage patterns (housing, transport, data centers)

The visualizations emphasize that electricity consumption is not uniformly distributed and depends strongly on socio-economic dynamics rather than geography alone.

## Copyright
We declare that the code provided in this project was produced entirely by ourselves,
except for the following lines: 
```python
#1 (common_functions.py -> select_data())
data[col_name] = data[col_name].astype(str).str.zfill(2)
# source : chat gpt
```