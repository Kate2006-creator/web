<script setup>
import axios from "axios"
import { onMounted, ref } from 'vue';
import Cookies from 'js-cookie';

const favours = ref([]);
const favourToAdd = ref({
  name: '',
  description: '',
  price: '',
  category: ''
});
const favourToEdit = ref({});

// Добавляем CSRF токен во все запросы
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

async function fetchFavours() {
    const r = await axios.get("/api/favours/")  
    favours.value = r.data;
}

async function onFavourAdd() {
  if (!favourToAdd.value.name || !favourToAdd.value.price || !favourToAdd.value.category) {
    alert('Заполните обязательные поля: название услуги, цена и категория');
    return;
  }

  try {
    await axios.post("/api/favours/", {
      ...favourToAdd.value
    });
    
    // Очищаем форму
    favourToAdd.value = {
      name: '',
      description: '',
      price: '',
      category: ''
    };
    
    // Обновляем список услуг
    await fetchFavours();
    
    alert('Услуга успешно добавлена!');
  } catch (error) {
    console.error('Ошибка при добавлении услуги:', error);
    alert('Ошибка при добавлении услуги');
  }
}

// Удаление услуги
async function onRemoveClick(favour) {
  if (confirm(`Удалить услугу "${favour.name}"?`)) {
    try {
      await axios.delete(`/api/favours/${favour.id}/`);
      await fetchFavours();
      alert('Услуга удалена!');
    } catch (error) {
      console.error('Ошибка при удалении услуги:', error);
      alert('Ошибка при удалении услуги');
    }
  }
}

// Редактирование услуги - открытие модального окна
function onFavourEditClick(favour) {
  favourToEdit.value = { ...favour };
}

// Сохранение изменений услуги
async function onUpdateFavour() {
  try {
    await axios.put(`/api/favours/${favourToEdit.value.id}/`, {
      ...favourToEdit.value,
    });
    await fetchFavours();
    alert('Услуга обновлена!');
  } catch (error) {
    console.error('Ошибка при обновлении услуги:', error);
    alert('Ошибка при обновлении услуги');
  }
}

onMounted(async () => {
  await fetchFavours();
})
</script>

<template>
  <div class="p-3">
    <!-- Форма добавления услуги -->
    <div class="mb-3">
      <h5>Добавление услуги</h5>
      <div class="row mb-2">
        <div class="col-md-6">
          <label for="name-input" class="form-label">Название услуги</label>
          <input id="name-input" name="name" v-model="favourToAdd.name" type="text" class="form-control" placeholder="Введите название услуги..."/>
        </div>
        <div class="col-md-3">
          <label for="price-input" class="form-label">Цена</label>
          <input id="price-input" name="price" v-model="favourToAdd.price" type="number" step="0.1" class="form-control" placeholder="..."/>
        </div>
        <div class="col-md-3">
          <label for="category-select" class="form-label">Категория</label>
          <select id="category-select" name="category" v-model="favourToAdd.category" class="form-select">
            <option value="design">Дизайн</option>
            <option value="development">Разработка</option>
            <option value="marketing">Маркетинг</option>
            <option value="consulting">Консалтинг</option>
            <option value="support">Поддержка</option>
          </select>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-12">
          <label for="description-input" class="form-label">Описание услуги</label>
          <textarea id="description-input" name="description" v-model="favourToAdd.description" class="form-control" rows="3" placeholder="Введите описание услуги..."></textarea>
        </div>
      </div>
      
      <button @click="onFavourAdd" class="btn btn-primary">
        <i class="bi bi-plus-square"></i> Добавить услугу
      </button>
    </div>

    <div class="mb-3">
      <button @click="fetchFavours" class="btn btn-primary">Загрузить услуги</button>
      <span class="ms-2">Загружено: {{ favours.length }}</span>
    </div>
    
    <!-- Список услуг -->
    <div>
      <h5>Список услуг</h5>
      <div v-if="favours.length === 0" class="text-muted">
        Услуг нет
      </div>
      <div v-else>
        <div v-for="item in favours" :key="item.id" class="mb-2 p-2 border d-flex justify-content-between align-items-center">
          <div>
            <strong>Название:</strong> {{ item.name }}<br>
            <strong>Цена:</strong> {{ item.price }} | 
            <strong>Категория:</strong> {{ item.category }}
            <div v-if="item.description">
              <strong>Описание:</strong> {{ item.description }}
            </div>
          </div>
          <div>
            <button
              class="btn btn-success btn-sm me-1"
              @click="onFavourEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editFavourModal"
            >
              <i class="bi bi-pencil-square"></i>
            </button>
            <button class="btn btn-danger btn-sm" @click="onRemoveClick(item)">
              <i class="bi bi-trash3"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования услуги -->
    <div class="modal fade" id="editFavourModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Редактировать услугу
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="favourToEdit.name"
                  />
                  <label>Название услуги</label>
                </div>
              </div>
              <div class="col-md-3">
                <div class="form-floating mb-3">
                  <input
                    type="number"
                    step="0.01"
                    class="form-control"
                    v-model="favourToEdit.price"
                  />
                  <label>Цена</label>
                </div>
              </div>
              <div class="col-md-3">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="favourToEdit.category">
                    <option value="design">Дизайн</option>
                    <option value="development">Разработка</option>
                    <option value="marketing">Маркетинг</option>
                    <option value="consulting">Консалтинг</option>
                    <option value="support">Поддержка</option>
                  </select>
                  <label>Категория</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <div class="form-floating">
                  <textarea
                    class="form-control"
                    v-model="favourToEdit.description"
                    style="height: 100px"
                  ></textarea>
                  <label>Описание услуги</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateFavour"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border {
  border-radius: 5px;
}
</style>