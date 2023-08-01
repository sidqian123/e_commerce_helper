// Define global variables
let productData;
let chart;
let currentProduct;
let currentChartRow;

// Define event listeners
document.getElementById('productButton').addEventListener('click', () => {
  const product = document.getElementById('productInput').value.trim();
  if (product) {
    currentProduct = product.replace(' ', '+');
    fetchProductData(currentProduct);
  }
});

// Define functions
function createTableHeader() {
  const table = document.getElementById('productTable');
  let thead = table.createTHead();
  let headerRow = thead.insertRow(0);
  let headerData = ["Search Date", "ASIN", "Name", "Price", "Rating", "Review Amount", "Amazon Prime", "Sale", "Image", "URL", "Estimated Buyers per Day"];

  for (let i = 0; i < headerData.length; i++) {
    let cell = document.createElement("th");
    let cellText = document.createTextNode(headerData[i]);
    cell.appendChild(cellText);
    headerRow.appendChild(cell);
  }
}

function fetchProductData(product) {
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

  createTableHeader();

  fetch(`http://localhost:8000/${product}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        productData = data;
        console.log(productData);
        displayProductData(productData, document.getElementById('reviewIndex').value.trim() === '' ? '0.02' : document.getElementById('reviewIndex').value.trim());
      })
      .catch(error => console.error('Error:', error));
}

function displayProductData(data, reviewFactor) {
  const table = document.getElementById('productTable');

  // Display each product's data
  for (const asin in data) {
    const product = data[asin];
    const row = table.insertRow(-1);

    // Fill the row cells with data
    row.insertCell(0).textContent = product['Search Date'][product['Search Date'].length - 1];
    row.insertCell(1).textContent = product.ASIN;
    row.insertCell(2).textContent = product.Name;
    row.insertCell(3).textContent = product.Price[product.Price.length - 1];
    row.insertCell(4).textContent = product.Rating[product.Rating.length - 1];
    row.insertCell(5).textContent = product['Review Amount'][product['Review Amount'].length - 1];
    row.insertCell(6).textContent = product['Amazon Prime'] ? 'Yes' : 'No';
    row.insertCell(7).textContent = product.Sale[product.Sale.length - 1];

    const imgCell = row.insertCell(8);
    const img = document.createElement('img');
    img.src = product.Image;
    img.style.width = '100px';
    imgCell.appendChild(img);

    const urlCell = row.insertCell(9);
    const a = document.createElement('a');
    a.href = product.URL;
    a.textContent = 'Product Link';
    urlCell.appendChild(a);

    // Estimated buyers per day
    const reviews = product['Review Amount'].map(review => parseInt(review.replace(/,/g, ''), 10));
    let estimatedBuyersPerDay;
    let deltaReviews = reviews[reviews.length - 1] - reviews[0];
    let deltaDays = (new Date(product['Search Date'][reviews.length - 1]) - new Date(product['Search Date'][0])) / (1000 * 60 * 60 * 24);
    estimatedBuyersPerDay = (deltaReviews / parseFloat(reviewFactor) / deltaDays).toFixed(document.getElementById('reviewIndex').value === '0' ? 0 : 2);
    row.insertCell(10).textContent = estimatedBuyersPerDay;

    // Add event listener to the row
    row.addEventListener('click', () => {
      if (chart) {
        chart.destroy();
      }
      if (currentChartRow) {
        currentChartRow.remove();
      }

      let newRow = table.insertRow(row.rowIndex + 1);
      currentChartRow = newRow;
      let newCell = newRow.insertCell(0);
      newCell.colSpan = 12;
      let canvas = document.createElement('canvas');

      // Set width and height for the canvas
      canvas.style.width = '600px';
      canvas.style.height = '100px';

      newCell.appendChild(canvas);

      const ctx = canvas.getContext('2d');
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: product['Search Date'],
          datasets: [{
            label: 'Price',
            data: product['Price'],
            borderColor: 'rgb(75, 192, 192)',
            fill: false
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: {
              display: true,
              title: {
                display: true,
                text: 'Search Date'
              }
            },
            y: {
              display: true,
              title: {
                display: true,
                text: 'Price'
              }
            }
          }
        }
      });
    });

  }
}
