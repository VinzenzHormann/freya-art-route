function doGet(e) {
 
  const sheetId = YOUR_SHEET_ID; 
  const sheetName = YOUR_SHEET_NAME
  
  // Get the data
  const ss = SpreadsheetApp.openById(sheetId);
  const sheet = ss.getSheetByName(sheetName);
  
  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({error: "Sheet not found"})).setMimeType(ContentService.MimeType.JSON);
  }
  
  const range = sheet.getDataRange();
  const values = range.getValues();
  
  if (values.length < 2) {
    return ContentService.createTextOutput(JSON.stringify({data: []})).setMimeType(ContentService.MimeType.JSON);
  }

  // First row is headers
  const headers = values[0].map(h => h.toString().toLowerCase().trim());
  const data = [];
  
  // Convert rows to array of objects
  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    const venue = {};
    headers.forEach((header, index) => {
      let key = header.replace(/\s/g, ''); // Remove spaces from key
      
      // Ensure numerical data types for ID, Lat, and Lng
      if (key === 'lat' || key === 'lng') {
          venue[key] = parseFloat(row[index]);
      } else if (key === 'id') {
          venue[key] = parseInt(row[index]);
      } else {
          venue[key] = row[index];
      }
    });
    data.push(venue);
  }
  
  // **THIS IS THE CORRECTED RETURN:**
  // Return JSON data. GAS adds CORS headers automatically if "Who has access" is "Anyone."
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}