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