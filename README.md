# HackRU 2024 Data Research

**HackRU** is Rutgers University's premier hackathon, held twice annually. As part of the HackRU data research team, this repository is dedicated to exploring past event data and leveraging it to improve decisions and guide future hackathon planning.

## Goals

1. **Data Analysis**: Understand historical trends, patterns, and performance metrics.
2. **Predictive Models**: Use machine learning to forecast key metrics and outcomes.
3. **Data Visualization**: Create interactive visuals to communicate insights to stakeholders.

## Objectives for 2024

- Analyze participant demographics, engagement levels, and project outcomes.
- Identify factors contributing to successful events and areas for improvement.
- Develop predictive models to support data-driven decision-making.
- Visualize findings to enhance transparency and collaboration.

---

## About HackRU

HackRU is Rutgers University's **biannual hackathon**, bringing together students, developers, and innovators for 24 hours of creativity, collaboration, and learning. Learn more at [HackRU's official website](https://hackru.org).

---

## How to Use This Repository

This repository will evolve over the course of 2024. It contains:

- **Data**: Processed datasets from past hackathons.
- **Scripts**: Python notebooks and scripts for analysis and visualization.
- **Models**: Machine learning models for predictive analysis.

Stay tuned for updates!

---

## Dependencies

To set up the required dependencies for this project, run the following command:

```bash
pip install python-dotenv pandas pymongo
```
or 

```bash
pip install -r requirements.txt
```

---

## Steps to Get Data

Follow these steps to retrieve data from MongoDB and store it locally:

1. **Set Up the MongoDB Key**:
   - Add your MongoDB URI (key) as an environment variable. This can be done by creating a `.env` file in the root directory of the project with the following content:
     ```env
     MONGO_URI=your-mongodb-uri
     ```

2. **Run the Scripts**:
   - Navigate to the `data_scripts` directory and run the relevant scripts to fetch data from MongoDB. For example:
     ```bash
     python ./data_scripts/mongo_to_csv.py
     ```

3. **Check the Output**:
   - Retrieved data will be saved in the `data` folder. Check this folder for JSON or CSV files containing the exported data.

---


