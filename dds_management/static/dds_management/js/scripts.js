document.getElementById('id_category').addEventListener('change', function() {
    const categoryId = this.value;
    fetch(`/get_subcategories/?category_id=${categoryId}`)
        .then(response => response.json())
        .then(data => {
            const subcategorySelect = document.getElementById('id_subcategory');
            subcategorySelect.innerHTML = '';
            data.forEach(subcategory => {
                const option = document.createElement('option');
                option.value = subcategory.id;
                option.textContent = subcategory.name;
                subcategorySelect.appendChild(option);
            });
        });
});