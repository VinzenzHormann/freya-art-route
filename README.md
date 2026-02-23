# Beyoğlu Art Route - Phase 2: Scale-Up to a production-grade, cloud-native FastAPI infrastructure

This repository houses the improved data backend for the **Beyoğlu Art Route**. This version implements the migration from a basic CMS to a production-grade, cloud-native FastAPI infrastructure designed for speed, security, and global scalability. While Phase 1 (Google Sheets CMS) was great for prototyping, it had limitations in speed and concurrency. For Phase 2, I completely re-engineered the backend to handle high traffic and complex geospatial data.

## The New Cloud Infrastructure

I moved the logic from a Google Apps Script attached to a google sheets table into a containerized FastAPI application on Google Cloud. This allows us to keep the data "hot" and ready for instant requests.

The changes include: 

* **Dockerization:** The entire backend is containerized using Docker, ensuring "write once, run anywhere" consistency and easy scaling across cloud clusters.

* **FastAPI Framework:** Leverages asynchronous programming (ASGI) to handle multiple requests simultaneously, significantly reducing latency compared to the previous Google Apps Script solution.

* **High-Traffic Readiness:** The move to a dedicated cloud instance allows for load balancing and auto-scaling to support thousands of concurrent users.

## Enhanced Data Schema
We have expanded the data footprint to provide a richer user experience. Every venue now includes:

* **Operational Metadata:** Opening days.

* **Economic Data:** Entry fees/pricing information.

* **Direct Links:** "Info Websites" of each venue (if present) for opening hours and pricing.

* **New Venues:** Two new venues added.

## Security & User Experience Improvements
As the project moved from a local prototype to a public-facing cloud application, I implemented a "Security-First" layer to protect both the user data and the cloud infrastructure.

1. **Hardcoded Fail-Safe & API Sync**
To ensure a seamless User Experience (UX), I implemented a hybrid data loading strategy:

* **The Fail-Safe:** The HTML includes a hardcoded "Base State" of key venues. If the user has a slow connection or the API call is delayed, the site is never blank.

* **The Dynamic Update:** Immediately upon page load, a call is made to the Cloud FastAPI backend. This script dynamically updates the DOM, ensuring the user sees the most current exhibition dates, opening hours, and new venues without a page refresh.

2. **API Key Protection & Infrastructure Budgeting**
Since the Google Maps API key is inherently visible in frontend client-side code, I took proactive measures to prevent unauthorized usage and "billing surprises":

* **Domain Restriction (Referrer Whitelisting):** The API key is strictly restricted at the Google Cloud Console level to only allow requests originating from https://www.freyartt.com/*. This makes the key useless if stolen or used on any other website.

* **Budgetary Guardrails:** I configured automated billing alerts in Google Cloud. If the API usage exceeds a predefined daily threshold, I receive an instant notification, preventing unexpected costs.

3. **Protection Against Injection (XSS)**
Because the application fetches data from an external API and renders it into the browser, I implemented a custom Sanitization Layer to prevent Cross-Site Scripting (XSS) attacks.

* **The Measure:** Every piece of text (Description, Address, Phone) is passed through an escapeHTML function before being injected into the DOM.

* **The Result:** This ensures that even if a database entry were compromised, no malicious <script> tags or HTML code could be executed in the user's browser.

## Roadmap

Phase 1 (Done) successfully synchronized gallery data via a Headless CMS. The next evolution of the project involves:
Phase 2 (Current) Migrating to a cloud-native FastAPI backend solution for quicker loading times and more robust data pipeline, architecting the pipeline for high-traffic scalability.

* **Multi-Category Geospatial Layers:** Integrating new data entities including Historical Landmarks (Yellow), Curated Coffee Breaks (Orange), and Second-Hand/Vintage Shops (Blue).
* **Mood-Based Recommendation Engine:** Implementing a user preference filter to select venues based on atmosphere (e.g., "Quiet/Energetic" coffee shops or "Vinyl/Postcard" retail focus).
* **Dynamic Time-Optimization:** An algorithm that adjusts the walking route based on the user's available time (e.g., 1-hour "Quick Walk" vs. 4-hour "Deep Dive").

## UPDATED: Data Flow & Data Structure

```text
[ USER ]                   [ SECURITY LAYER ]             [ CLOUD BACKEND ]
          |                              |                             |
          |  GET /api/venues             |                             |
          |----------------------------> |  Is Request from            |
          |                              |  freyartt.com?  (CORS)      |
          |                              |-------------+               |
          |                              |             | Yes           |
          |                              |             v               |
          | <----------------------------|       [ FastAPI App ] <-----+
          |       JSON Response          |       [ Dockerized  ]       |
          |                              |                             |


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
| opening_days| String       | Bool value for every day    	                    |
| price       | String       | Standart price for turkish citizen full price        |
| info_website| String (URL) | Link to the venue's pricing/opening hours site       |
+-------------+--------------+------------------------------------------------------+

```

---
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
