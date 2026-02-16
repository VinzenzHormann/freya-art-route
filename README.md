# Beyoğlu Art Route - Phase 1: Google Sheets as a Headless CMS

This repository contains the foundational phase of the **Beyoğlu Art Route** project. This version implements a lightweight, serverless "Headless CMS" using **Google Sheets** and **Google Apps Script** to power a dynamic web application.

## The Concept
Instead of hardcoding museum and gallery data or setting up a complex database at the start, I leveraged Google Workspace tools to create a user-friendly data management system. This allows for real-time updates to the website by simply editing a spreadsheet.

## The Architecture

1. **Data Source (Google Sheets):** All venue information (Name, Lat/Lng, Address, Description, etc.) is stored in a structured Google Sheet.
   
2. **API Layer (Google Apps Script):** A JavaScript snippet (GAS) is attached to the sheet. It acts as a middleware that:
   * Reads the spreadsheet rows.
   * Converts the data into a **JSON format**.
   * Exposes a **Web App URL** that functions as a RESTful API endpoint (`GET`).

3. **Frontend (Vanilla JS):** The application uses the `fetch()` API to call the GAS URL, retrieve the venue list, and dynamically render UI cards and Google Maps markers.

## Roadmap

Phase 1 (Current) successfully synchronized gallery data via a Headless CMS. The next evolution of the project involves:

* **Advanced Data Pipeline:** Migrating to a cloud-native FastAPI backend solution for quicker loading times and more robust data pipeline, architecting the pipeline for high-traffic scalability.
* **Multi-Category Geospatial Layers:** Integrating new data entities including Historical Landmarks (Yellow), Curated Coffee Breaks (Orange), and Second-Hand/Vintage Shops (Blue).
* **Mood-Based Recommendation Engine:** Implementing a user preference filter to select venues based on atmosphere (e.g., "Quiet/Energetic" coffee shops or "Vinyl/Postcard" retail focus).
* **Dynamic Time-Optimization:** An algorithm that adjusts the walking route based on the user's available time (e.g., 1-hour "Quick Walk" vs. 4-hour "Deep Dive").


## Data Flow & Data Structure
Google Sheet (Data) -> Google Apps Script (API) -> Vanilla JS (Frontend) -> Google Maps API (Visualization)

## Data Flow & Schema

```text
       [ ADMIN ]                     [ BACKEND ]                    [ FRONTEND ]
    +--------------+            +--------------------+         +-----------------------+
    | Google Sheet |  ------->  | Google Apps Script | ------> | Vanilla JS (fetch API)|
    | (Data Entry) |            | (JSON API Endpoint)|         | (State Management)    |
    +--------------+            +--------------------+         +-----------+-----------+
                                                                           |
                                                                           v
                                                               +-----------------------+
                                                               |   Google Maps API     |
                                                               | (Path Rendering & UI) |
                                                               +-----------------------+
+-------------+--------------+------------------------------------------------------+
| Field       | Type         | Description                                          |
+-------------+--------------+------------------------------------------------------+
| id          | Integer      | Unique identifier for the venue                      |
| name        | String       | The official name of the Gallery or Museum           |
| type        | String       | Categorization: "museum" or "gallery"                |
| lat         | Float/Decimal| Latitude coordinate (e.g., 41.0360)                  |
| lng         | Float/Decimal| Longitude coordinate (e.g., 28.9876)                 |
| description | String       | Short blurb about the venue's current focus          |
| address     | String       | Physical street address in Beyoğlu                   |
| phone       | String       | Contact number                                       |
| website     | String (URL) | Link to the venue's official page                    |
+-------------+--------------+------------------------------------------------------+
