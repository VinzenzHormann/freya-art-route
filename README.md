# Beyoğlu Art Route - Phase 1: Google Sheets as a Headless CMS

This repository contains the foundational phase of the **Beyoğlu Art Route** project. This version implements a lightweight, serverless "Headless CMS" using **Google Sheets** and **Google Apps Script** to power a dynamic web application.

## 🚀 The Concept
Instead of hardcoding museum and gallery data or setting up a complex database at the start, I leveraged Google Workspace tools to create a user-friendly data management system. This allows for real-time updates to the website by simply editing a spreadsheet.

---

## 🛠️ How It Works (The Architecture)

1. **Data Source (Google Sheets):** All venue information (Name, Lat/Lng, Address, Description, etc.) is stored in a structured Google Sheet.
   
2. **API Layer (Google Apps Script):** A JavaScript snippet (GAS) is attached to the sheet. It acts as a middleware that:
   * Reads the spreadsheet rows.
   * Converts the data into a **JSON format**.
   * Exposes a **Web App URL** that functions as a RESTful API endpoint (`GET`).

3. **Frontend (Vanilla JS):** The application uses the `fetch()` API to call the GAS URL, retrieve the venue list, and dynamically render UI cards and Google Maps markers.
