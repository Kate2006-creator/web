<script setup>
import axios from "axios"
import { onMounted, ref, computed } from 'vue';
import Cookies from 'js-cookie';

const projects = ref([]);
const clients = ref([]);
const projectToAdd = ref({
  name: '',
  client_user: '',
  deadline: '',
  budget: '',
  status: '',
  description: ''
});
const projectToEdit = ref({});

// Добавляем CSRF токен во все запросы
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

// Маппинг статусов на русский язык
const statusMap = {
  'planning': 'Планирование',
  'in_progress': 'В работе',
  'completed': 'Завершен',
  'on_hold': 'На паузе',
  'cancelled': 'Отменен'
};

// Computed свойство для проектов с русскими статусами
const projectsWithRussianStatus = computed(() => {
  return projects.value.map(project => ({
    ...project,
    status_russian: statusMap[project.status] || project.status
  }));
});

function getClientName(clientUserId) {
  const client = clients.value.find(c => c.user === clientUserId);
  if (!client) return 'Клиент не найден';
  
  return client.user_username || client.user_profile_fio || client.company_name || `Клиент #${client.id}`;
}

function getClientCompany(clientUserId) {
  const client = clients.value.find(c => c.user === clientUserId);
  return client?.company_name;
}

async function fetchProjects() {
  try {
    const r = await axios.get("/api/projects/")  
    projects.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки проектов:', error);
  }
}

async function fetchClients() {
  try {
    const r = await axios.get("/api/clients/")  
    clients.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки клиентов:', error);
  }
}

async function onProjectAdd() {
  if (!projectToAdd.value.name || !projectToAdd.value.client_user || !projectToAdd.value.deadline) {
    alert('Заполните обязательные поля: название проекта, клиент и срок сдачи');
    return;
  }

  try {
    await axios.post("/api/projects/", {
      ...projectToAdd.value
    });
    
    // Очищаем форму
    projectToAdd.value = {
      name: '',
      client_user: '',
      deadline: '',
      budget: '',
      status: '',
      description: ''
    };
    
    // Обновляем список проектов
    await fetchProjects();
    
    alert('Проект успешно добавлен!');
  } catch (error) {
    console.error('Ошибка при добавлении проекта:', error);
    alert('Ошибка при добавлении проекта');
  }
}

// Удаление проекта
async function onRemoveClick(project) {
  if (confirm(`Удалить проект "${project.name}"?`)) {
    try {
      await axios.delete(`/api/projects/${project.id}/`);
      await fetchProjects();
      alert('Проект удален!');
    } catch (error) {
      console.error('Ошибка при удалении проекта:', error);
      alert('Ошибка при удалении проекта');
    }
  }
}

// Редактирование проекта - открытие модального окна
function onProjectEditClick(project) {
  projectToEdit.value = { ...project };
}

// Сохранение изменений проекта
async function onUpdateProject() {
  try {
    await axios.put(`/api/projects/${projectToEdit.value.id}/`, {
      ...projectToEdit.value,
    });
    await fetchProjects();
    alert('Проект обновлен!');
  } catch (error) {
    console.error('Ошибка при обновлении проекта:', error);
    alert('Ошибка при обновлении проекта');
  }
}

onMounted(async () => {
  await fetchProjects();
  await fetchClients();
})
</script>

<template>
  <div class="p-3">
    <!-- Форма добавления проекта -->
    <div class="mb-3">
      <h5>Добавление проекта</h5>
      <div class="row mb-2">
        <div class="col-md-6">
          <label for="name-input" class="form-label">Название проекта</label>
          <input id="name-input" name="name" v-model="projectToAdd.name" type="text" class="form-control" placeholder="Введите название проекта..."/>
        </div>
        <div class="col-md-6">
          <label for="client-select" class="form-label">Клиент</label>
          <select id="client-select" name="client_user" v-model="projectToAdd.client_user" class="form-select">
            <option v-for="client in clients" :key="client.id" :value="client.user">
              {{ client.user_username }} 
              <span v-if="client.company_name">({{ client.company_name }})</span>
            </option>
          </select>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-md-4">
          <label for="deadline-input" class="form-label">Срок сдачи</label>
          <input id="deadline-input" name="deadline" v-model="projectToAdd.deadline" type="date" class="form-control"/>
        </div>
        <div class="col-md-4">
          <label for="budget-input" class="form-label">Бюджет</label>
          <input id="budget-input" name="budget" v-model="projectToAdd.budget" type="number" step="0.1" class="form-control" placeholder="..."/>
        </div>
        <div class="col-md-4">
          <label for="status-select" class="form-label">Статус</label>
          <select id="status-select" name="status" v-model="projectToAdd.status" class="form-select">
            <option value="planning">Планирование</option>
            <option value="in_progress">В работе</option>
            <option value="completed">Завершен</option>
            <option value="on_hold">На паузе</option>
            <option value="cancelled">Отменен</option>
          </select>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-12">
          <label for="description-input" class="form-label">Описание проекта</label>
          <textarea id="description-input" name="description" v-model="projectToAdd.description" class="form-control" rows="3" placeholder="Введите описание проекта..."></textarea>
        </div>
      </div>
      
      <button @click="onProjectAdd" class="btn btn-primary">
        <i class="bi bi-plus-square"></i> Добавить проект
      </button>
    </div>

    <div class="mb-3">
      <button @click="fetchProjects" class="btn btn-primary">Загрузить проекты</button>
      <span class="ms-2">Загружено: {{ projects.length }}</span>
    </div>
    
    <!-- Список проектов -->
    <div>
      <h5>Список проектов</h5>
      <div v-if="projects.length === 0" class="text-muted">
        Проектов нет
      </div>
      <div v-else>
        <div v-for="item in projectsWithRussianStatus" :key="item.id" class="mb-2 p-2 border d-flex justify-content-between align-items-center">
          <div>
            <strong>Название:</strong> {{ item.name }}<br>
            <strong>Клиент:</strong> {{ getClientName(item.client_user) }}
            <span v-if="getClientCompany(item.client_user)">({{ getClientCompany(item.client_user) }})</span><br>
            <strong>Срок сдачи:</strong> {{ item.deadline }} | 
            <strong>Бюджет:</strong> {{ item.budget }} | 
            <strong>Статус:</strong> {{ item.status_russian }}
            <div v-if="item.description">
              <strong>Описание:</strong> {{ item.description }}
            </div>
          </div>
          <div>
            <button
              class="btn btn-success btn-sm me-1"
              @click="onProjectEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editProjectModal"
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

    <!-- Модальное окно редактирования проекта -->
    <div class="modal fade" id="editProjectModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Редактировать проект
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
                    v-model="projectToEdit.name"
                  />
                  <label>Название проекта</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="projectToEdit.client_user">
                    <option :value="client.user" v-for="client in clients">
                      {{ client.user_username }} 
                      <span v-if="client.company_name">({{ client.company_name }})</span>
                    </option>
                  </select>
                  <label>Клиент</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-4">
                <div class="form-floating mb-3">
                  <input
                    type="date"
                    class="form-control"
                    v-model="projectToEdit.deadline"
                  />
                  <label>Срок сдачи</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating mb-3">
                  <input
                    type="number"
                    step="0.01"
                    class="form-control"
                    v-model="projectToEdit.budget"
                  />
                  <label>Бюджет</label>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="projectToEdit.status">
                    <option value="">Выберите статус</option>
                    <option value="planning">Планирование</option>
                    <option value="in_progress">В работе</option>
                    <option value="completed">Завершен</option>
                    <option value="on_hold">На паузе</option>
                    <option value="cancelled">Отменен</option>
                  </select>
                  <label>Статус</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <div class="form-floating">
                  <textarea
                    class="form-control"
                    v-model="projectToEdit.description"
                    style="height: 100px"
                  ></textarea>
                  <label>Описание проекта</label>
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
              @click="onUpdateProject"
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