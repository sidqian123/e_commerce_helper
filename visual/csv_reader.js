function processCSVData(csvData) {
  const rows = csvData.split('\n');
  const headers = rows[0].split(',');

  const table = document.getElementById('csvTable');

  // Create table header
  const headerRow = document.createElement('tr');
  headers.forEach(headerText => {
    const th = document.createElement('th');
    th.textContent = headerText.trim();
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  // Create table rows
  rows.slice(1).forEach(rowData => {
    const rowDataArray = rowData.split(',');

    const row = document.createElement('tr');
    rowDataArray.forEach(cellData => {
      const td = document.createElement('td');
      td.textContent = cellData.trim();
      row.appendChild(td);
    });
    table.appendChild(row);
  });
}

function loadCSVData() {
  fetch('../product_data/amazon_products.csv')
      .then(response => response.text())
      .then(csvData => processCSVData(csvData))
      .catch(error => console.error('Error fetching CSV file:', error));
}
