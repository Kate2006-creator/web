<script setup>
import axios from "axios"
import { onMounted, ref } from 'vue';
import Cookies from 'js-cookie';

const reviews = ref([]);
const projects = ref([]);
const reviewToAdd = ref({
  project: '',
  rating: 5,
  feedback: ''
  // Убрали is_published
});
const reviewToEdit = ref({});

// Добавляем CSRF токен во все запросы
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

async function fetchReviews() {
    const r = await axios.get("/api/reviews/")  
    reviews.value = r.data;
}

async function fetchProjects() {
    const r = await axios.get("/api/projects/")  
    projects.value = r.data;
}

async function onReviewAdd() {
  if (!reviewToAdd.value.project || !reviewToAdd.value.feedback) {
    alert('Заполните обязательные поля: проект и текст отзыва');
    return;
  }

  try {
    await axios.post("/api/reviews/", {
      ...reviewToAdd.value
    });
    
    // Очищаем форму
    reviewToAdd.value = {
      project: '',
      rating: 5,
      feedback: ''
      // Убрали is_published
    };
    
    // Обновляем список отзывов
    await fetchReviews();
    
    alert('Отзыв успешно добавлен!');
  } catch (error) {
    console.error('Ошибка при добавлении отзыва:', error);
    alert('Ошибка при добавлении отзыва');
  }
}

// Удаление отзыва
async function onRemoveClick(review) {
  if (confirm(`Удалить отзыв на проект "${review.project_name}"?`)) {
    try {
      await axios.delete(`/api/reviews/${review.id}/`);
      await fetchReviews();
      alert('Отзыв удален!');
    } catch (error) {
      console.error('Ошибка при удалении отзыва:', error);
      alert('Ошибка при удалении отзыва');
    }
  }
}

// Редактирование отзыва - открытие модального окна
function onReviewEditClick(review) {
  reviewToEdit.value = { ...review };
}

// Сохранение изменений отзыва
async function onUpdateReview() {
  try {
    await axios.put(`/api/reviews/${reviewToEdit.value.id}/`, {
      ...reviewToEdit.value,
    });
    await fetchReviews();
    alert('Отзыв обновлен!');
  } catch (error) {
    console.error('Ошибка при обновлении отзыва:', error);
    alert('Ошибка при обновлении отзыва');
  }
}

// Функция для получения названия проекта
function getProjectName(projectId) {
  const project = projects.value.find(p => p.id === projectId);
  return project?.name || 'Проект не найден';
}

// Функция для отображения звезд рейтинга
function getRatingStars(rating) {
  return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

onMounted(async () => {
  await fetchReviews();
  await fetchProjects();
})
</script>

<template>
  <div class="p-3">
    <!-- Форма добавления отзыва -->
    <div class="mb-3">
      <h5>Добавление отзыва</h5>
      <div class="row mb-2">
        <div class="col-md-6">
          <label for="project-select" class="form-label">Проект</label>
          <select id="project-select" name="project" v-model="reviewToAdd.project" class="form-select">
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name }} ({{ project.client_user_username || 'Клиент' }})
            </option>
          </select>
        </div>
        <div class="col-md-6">
          <label for="rating-select" class="form-label">Оценка</label>
          <select id="rating-select" name="rating" v-model="reviewToAdd.rating" class="form-select">
            <option value="1">1 ★</option>
            <option value="2">2 ★★</option>
            <option value="3">3 ★★★</option>
            <option value="4">4 ★★★★</option>
            <option value="5">5 ★★★★★</option>
          </select>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-12">
          <label for="feedback-input" class="form-label">Текст отзыва</label>
          <textarea id="feedback-input" name="feedback" v-model="reviewToAdd.feedback" class="form-control" rows="4" placeholder="Введите текст отзыва..."></textarea>
        </div>
      </div>
      
      <button @click="onReviewAdd" class="btn btn-primary">
        <i class="bi bi-plus-square"></i> Добавить отзыв
      </button>
    </div>

    <div class="mb-3">
      <button @click="fetchReviews" class="btn btn-primary">Загрузить отзывы</button>
      <span class="ms-2">Загружено: {{ reviews.length }}</span>
    </div>
    
    <!-- Список отзывов -->
    <div>
      <h5>Список отзывов</h5>
      <div v-if="reviews.length === 0" class="text-muted">
        Отзывов нет
      </div>
      <div v-else>
        <div v-for="item in reviews" :key="item.id" class="mb-2 p-2 border d-flex justify-content-between align-items-center">
          <div class="flex-grow-1">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <strong>Проект:</strong> {{ item.project_name || getProjectName(item.project) }}<br>
                <strong>Оценка:</strong> 
                <span class="text-warning">{{ getRatingStars(item.rating) }}</span> 
                ({{ item.rating }}/5)<br>
                <strong>Дата:</strong> {{ new Date(item.created_at).toLocaleDateString() }}
              </div>
            </div>
            <div class="mt-2">
              <strong>Отзыв:</strong> {{ item.feedback }}
            </div>
          </div>
          <div class="ms-3">
            <button
              class="btn btn-success btn-sm me-1"
              @click="onReviewEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editReviewModal"
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

    <!-- Модальное окно редактирования отзыва -->
    <div class="modal fade" id="editReviewModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Редактировать отзыв
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
                  <select class="form-select" v-model="reviewToEdit.project">
                    <option :value="project.id" v-for="project in projects">
                      {{ project.name }} ({{ project.client_user_username || 'Клиент' }})
                    </option>
                  </select>
                  <label>Проект</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="reviewToEdit.rating">
                    <option value="1">1 ★</option>
                    <option value="2">2 ★★</option>
                    <option value="3">3 ★★★</option>
                    <option value="4">4 ★★★★</option>
                    <option value="5">5 ★★★★★</option>
                  </select>
                  <label>Оценка</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <div class="form-floating">
                  <textarea
                    class="form-control"
                    v-model="reviewToEdit.feedback"
                    style="height: 150px"
                  ></textarea>
                  <label>Текст отзыва</label>
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
              @click="onUpdateReview"
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
.text-warning {
  color: #ffc107 !important;
}
</style>