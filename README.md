# BMI706: Data Visualization Project Mortality Data
---
Authors: Benedikt Geiger, Mirja Mittermaier, Fiona Song, Lantian Xu <br>
April 2022
---


The goal of our project is to gain insights from state- and county-level visualizations of US mortality data.
The data ranges from 1968 to 2016 and is stratified by state, (county), year, race, gender, age group and ICD group.

Please read the `README_data_generation.md` file in the `data_generation` folder for further details on the data.

Our visualizations use large files with mortality information on a county level. <strong>Before</strong> running the `project_app.py` via

```bash
streamlit run project_app.py
```

<strong>it is necessary</strong> to run the `generate_files.sh` script located in the `data_generation` folder to automatically download and generate
the required files. Running the script takes approximately 5-10 minutes.

Regarding our visualiuations, we used Altair and Streamlit to solve the following tasks:
* Identify difference in US state and county mortality rates
* Reveal mortality rate trends for different ICD groups
* Detect gender, race and age group mortality differences
* Display population growth per state, race and age group


