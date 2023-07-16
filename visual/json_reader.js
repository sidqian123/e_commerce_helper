// main.js

window.onload = function() {
  fetch('../product_data/amz_chair_2023-07-15_.json')
      .then(response => response.json())
      .then(data => {
        var table = document.getElementById('productTable').getElementsByTagName('tbody')[0];

        data.forEach(function(item) {
          var newRow = table.insertRow();

          Object.keys(item).forEach(function(key) {
            var newCell = newRow.insertCell();
            if (key === 'Image') {
              var img = document.createElement('img');
              img.src = item[key];
              img.style.width = '100px';
              img.style.height = '100px';
              newCell.appendChild(img);
            } else if (key === 'URL') {
              var anchor = document.createElement('a');
              anchor.href = item[key];
              anchor.textContent = 'Product Link';
              newCell.appendChild(anchor);
            } else {
              var newText = document.createTextNode(item[key]);
              newCell.appendChild(newText);
            }
          });
        });
      })
      .catch(error => console.error('Error:', error));
}
