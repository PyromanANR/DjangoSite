document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault();

        var name = document.querySelector('input[name="name"]').value;
        var minCost = document.querySelector('input[name="min-cost"]').value;
        var maxCost = document.querySelector('input[name="max-cost"]').value;
        var category = document.querySelector('select[name="category"]').value;

        var products = document.querySelectorAll('.product');
        products.forEach(function(product) {
            var productName = product.querySelector('h2').textContent;
            var productCost = parseFloat(product.querySelector('p').textContent);
            var productCategory = product.querySelector('.product-category').textContent;

            var showProduct = true;

            if (name && !productName.includes(name)) {
                showProduct = false;
            }

            if (minCost && productCost < parseFloat(minCost)) {
                showProduct = false;
            }

            if (maxCost && productCost > parseFloat(maxCost)) {
                showProduct = false;
            }

            if (category && productCategory !== category) {
                showProduct = false;
            }

            product.style.display = showProduct ? '' : 'none';
        });
    });
});
