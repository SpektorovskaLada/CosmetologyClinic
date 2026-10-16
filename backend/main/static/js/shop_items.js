function showDialog(productId) {

    const productData =
        document.getElementById(`product-data-${productId}`);

    const title = productData.dataset.name;
    const description = productData.dataset.description;
    const price = productData.dataset.price;

    const dialog = document.getElementById('productDialog');

    document.getElementById('dialogContent').innerHTML = `
        <div class="product-modal-description">

            <h1>${title}</h1>

            <p><b>${price} грн</b></p>

            ${description.replace(/\n/g, '<br>')}

        </div>
    `;

    dialog.showModal();
}