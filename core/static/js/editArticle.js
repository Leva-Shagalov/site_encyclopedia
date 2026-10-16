const path = window.location.pathname;

fetch(`/api/content/${path.split("/").at(-1)}`)
  .then((response) => {
    // Проверяем, что сервер ответил успешно
    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }
    // Автоматически декодируем JSON (включая все \r\n и кавычки)
    return response.json();
  })
  .then((content) => {
    // Здесь данные уже полностью готовы к работе
    console.log("Данные успешно получены:", content);

    const titleFieldElement = document.getElementById("id_title");
    const contentFieldElement = document.getElementById("id_content");
    const topicFieldElement = document.getElementById("id_topic");
    const statusFieldElement = document.getElementById("id_status");
    const resetButtonElement = document.getElementById("reset_button");
    const formElement = document.getElementById("form");

    titleFieldElement.value = content.title;
    contentFieldElement.value = content.content;
    topicFieldElement.value = content.topic;
    statusFieldElement.removeAttribute("multiple");
    statusFieldElement.value = content.status;

    resetButtonElement.addEventListener("click", () => {
      const content = tinymce.get("id_content");

      formElement.reset();
      content.setContent("");
    });
  });
