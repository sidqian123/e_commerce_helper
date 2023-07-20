let productData;
let chart;
let currentProduct;
let currentChartRow;

document.getElementById('productButton').addEventListener('click', () => {
  const product = document.getElementById('productInput').value.trim();
  if (product) {
    currentProduct = product.replace(' ', '+');
    fetchLatestFile(currentProduct);
  }
});

function fetchLatestFile(product) {
  // Clear the table before fetching new data
  const table = document.getElementById('productTable');
  while (table.rows.length > 0) {
    table.deleteRow(0);
  }

  // Clear the chart if it exists
  if (chart) {
    chart.destroy();
    chart = null;
  }

  // Remove chart row if exists
  if (currentChartRow) {
    currentChartRow.remove();
    currentChartRow = null;
  }

  fetch(`http://localhost:8000/${product}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        productData = data;
        displayProductData(productData);
      })
      .catch(error => console.error('Error:', error));
}

function displayProductData(data) {
  const table = document.getElementById('productTable');
  const headerRow = table.insertRow(-1);
  ['Search Date', 'ASIN', 'Name', 'Price', 'Rating', 'Review Amount', 'Amazon Prime', 'Sale', 'Brand', 'Image', 'URL']
      .forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
      });
  data.forEach((item, index) => {
    const row = table.insertRow(-1);
    row.id = 'row-' + index;
    row.insertCell(0).textContent = item['Search Date'];
    row.insertCell(1).textContent = item.ASIN;
    row.insertCell(2).textContent = item.Name;
    row.insertCell(3).textContent = item.Price;
    row.insertCell(4).textContent = item.Rating;
    row.insertCell(5).textContent = item['Amazon Prime'] ? 'Yes' : 'No';
    row.insertCell(6).textContent = item.Sale;
    row.insertCell(7).textContent = item.Brand;

    const imgCell = row.insertCell(8);
    const img = document.createElement('img');
    img.src = item.Image;
    img.style.width = '100px';
    imgCell.appendChild(img);

    const urlCell = row.insertCell(9);
    const a = document.createElement('a');
    a.href = item.URL;
    a.textContent = 'Product Link';
    urlCell.appendChild(a);
  });

  table.addEventListener('click', (event) => {
    const row = event.target.closest('tr');
    if (!row || !row.id || !row.id.startsWith('row-')) return;
    const index = Number(row.id.split('-')[1]);

    // Remove existing chart row if present
    if (currentChartRow) {
      currentChartRow.remove();
      currentChartRow = null;
    }

    // Create a canvas right under the clicked row
    currentChartRow = table.insertRow(row.rowIndex + 1);
    currentChartRow.id = 'chart-row-' + index;
    const chartCell = currentChartRow.insertCell(0);
    chartCell.colSpan = 10;
    const canvas = document.createElement('canvas');
    canvas.id = 'chart-' + index;
    chartCell.appendChild(canvas);

    fetchHistoricalData(data[index].ASIN, canvas.id);
  });

  function fetchHistoricalData(asin, canvasId) {
    console.log('Fetching historical data for:', asin);  // Debug: check the ASIN we're requesting
    fetch(`http://localhost:8000/${currentProduct}/history/${asin}`)  // Modified fetch URL as per server code
        .then(response => {
          if (!response.ok) throw new Error('HTTP error ' + response.status);
          return response.json();
        })
        .then(data => {
          console.log('Received history data:', data);  // Debug: check the history data we received
          if (!data || data.length === 0) {
            console.log('Error: No history data received for this ASIN.');
          } else {
            const dates = [];
            const prices = [];

            data.forEach(item => {
              dates.push(item['Search Date']);
              prices.push(item.Price);
            });

            console.log('Dates:', dates);  // Debug: check the dates array
            console.log('Prices:', prices);  // Debug: check the prices array

            createGraph(dates, prices, asin, canvasId);  // Pass canvasId here
          }
        })
        .catch(error => console.log('Fetch failed:', error));
  }
}


function createGraph(dates, prices, asin, canvasId) {  // Include canvasId in arguments
  if (chart) chart.destroy();

  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  canvas.style.width = '800px'; // set width
  canvas.style.height = '100px'; // set height

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: 'Price of ' + asin,
        data: prices,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: false,
        pointRadius: dates.length === 1 ? 5 : 1
      }]
    },
    options: {
      responsive: true,
      title: {
        display: true,
        text: 'Price Trend'
      },
      scales: {
        x: {
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Date'
          }
        },
        y: {
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Price'
          }
        }
      }
    }
  });
}
