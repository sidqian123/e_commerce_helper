let productData;
let chart;

fetch('../product_data/amz_chair_2023-07-15_.json')
    .then(response => response.json())
    .then(data => {
      productData = data;
      displayProductData(productData);
    })
    .catch(error => console.error('Error:', error));

function displayProductData(data) {
  const table = document.getElementById('productTable');

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
    fetchHistoricalData(data[index].ASIN, 'chair');
  });
}

function fetchHistoricalData(asin, keyword) {
  fetch('../product_data/amz_' + keyword + '_2023-07-16_.json')
      .then(response => {
        if (!response.ok) throw new Error('HTTP error ' + response.status);
        return response.json();
      })
      .then(data => {
        const dates = [];
        const prices = [];

        data.forEach(item => {
          if (item.ASIN === asin) {
            dates.push(item['Search Date']);
            prices.push(item.Price);
          }
        });

        createGraph(dates, prices, asin);
      })
      .catch(error => {
        console.log('Fetch failed:', error);
        const dates = [new Date().toISOString().slice(0, 10)];
        const prices = [item.Price];
        createGraph(dates, prices, asin);
      });
}

function createGraph(dates, prices, asin) {
  const ctx = document.getElementById('priceChart').getContext('2d');

  if (chart) chart.destroy();

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
