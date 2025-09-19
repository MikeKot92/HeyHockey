// Функция для показа и скрытия сообщения
document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("popupMessage");

    // Показываем сообщение
    popup.classList.add("show");

    // Скрываем сообщение через 5 секунд
    setTimeout(() => {
        popup.classList.remove("show");

        // Удаляем сообщение из DOM после завершения анимации
        setTimeout(() => {
            popup.remove();
        }, 300); // 300ms — время анимации исчезновения
    }, 3000); // 3000ms = 3 секунд
});

// Функция сброса формы фильтров
function resetForm() {
    // Получаем текущий URL
    let url = new URL(window.location);

    // Определяем базовый путь
    let basePath = url.pathname;

    // Проверяем, есть ли поисковый параметр
    const searchParams = new URLSearchParams(url.search);
    const searchQuery = searchParams.get('q');

    // Создаем новый URL без параметров фильтров
    if (searchQuery) {
        // Если есть поисковый запрос, сохраняем только его
        window.location.href = basePath + '?q=' + encodeURIComponent(searchQuery);
    } else {
        // Если нет поискового запроса, просто перезагружаем страницу без параметров
        window.location.href = basePath;
    }
}

// Функция переключения изображений
function changeImage(element) {
    document.getElementById('mainImage').src = element.src;
    document.querySelectorAll('.thumbnail-image').forEach(img => img.classList.remove('active'));
    element.classList.add('active');
}




