function showFullImage(imageElement) {
	const modal = document.getElementById('full-image-modal') //взяти нашеєдине для всіх порожнє модальне вікно
	const fullImage = document.getElementById('full-image') //взяти картинку в середині модального вікна

	fullImage.src = imageElement.src // міняємо вміст невидимого контейнеру на вміст превью на яке ми клікнули та передали через this
	modal.style.display = 'flex' // відображаємо модальне вікно
}

function closeModal() {
	const modal = document.getElementById('full-image-modal')
	modal.style.display = 'none' // ховаємо модальне вікно
}
