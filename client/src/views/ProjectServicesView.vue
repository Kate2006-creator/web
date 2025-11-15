<script setup>
import axios from "axios"
import { onMounted, ref } from 'vue';
import Cookies from 'js-cookie';

const projectServices = ref([]);
const projects = ref([]);
const favours = ref([]);
const employees = ref([]);
const projectServiceToAdd = ref({
  project: '',
  favour: '',
  employee_user: '',
  status: 'in_progress',
  end_date: '',
  hours_spent: 0,
  notes: ''
});
const projectServiceToEdit = ref({});

// Добавляем CSRF токен во все запросы
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

// Маппинг статусов на русский язык
const statusMap = {
  'in_progress': 'В работе',
  'completed': 'Завершена',
  'on_hold': 'На паузе',
  'cancelled': 'Отменена'
};

async function fetchProjectServices() {
    const r = await axios.get("/api/project-services/")  
    projectServices.value = r.data;
}

async function fetchProjects() {
    const r = await axios.get("/api/projects/")  
    projects.value = r.data;
}

async function fetchFavours() {
    const r = await axios.get("/api/favours/")  
    favours.value = r.data;
}

async function fetchEmployees() {
    const r = await axios.get("/api/employees/")  
    employees.value = r.data;
}

async function onProjectServiceAdd() {
  if (!projectServiceToAdd.value.project || !projectServiceToAdd.value.favour) {
    alert('Заполните обязательные поля: проект и услуга');
    return;
  }

  try {
    await axios.post("/api/project-services/", {
      ...projectServiceToAdd.value
    });
    
    // Очищаем форму
    projectServiceToAdd.value = {
      project: '',
      favour: '',
      employee_user: '',
      status: 'in_progress',
      end_date: '',
      hours_spent: 0,
      notes: ''
    };
    
    // Обновляем список услуг в проектах
    await fetchProjectServices();
    
    alert('Услуга успешно привязана к проекту!');
  } catch (error) {
    console.error('Ошибка при привязке услуги к проекту:', error);
    alert('Ошибка при привязке услуги к проекту');
  }
}

// Удаление услуги из проекта
async function onRemoveClick(projectService) {
  if (confirm(`Удалить услугу "${projectService.favour_name}" из проекта?`)) {
    try {
      await axios.delete(`/api/project-services/${projectService.id}/`);
      await fetchProjectServices();
      alert('Услуга удалена из проекта!');
    } catch (error) {
      console.error('Ошибка при удалении услуги из проекта:', error);
      alert('Ошибка при удалении услуги из проекта');
    }
  }
}

// Редактирование услуги в проекте - открытие модального окна
function onProjectServiceEditClick(projectService) {
  projectServiceToEdit.value = { ...projectService };
}

// Сохранение изменений услуги в проекте
async function onUpdateProjectService() {
  try {
    await axios.put(`/api/project-services/${projectServiceToEdit.value.id}/`, {
      ...projectServiceToEdit.value,
    });
    await fetchProjectServices();
    alert('Услуга в проекте обновлена!');
  } catch (error) {
    console.error('Ошибка при обновлении услуги в проекте:', error);
    alert('Ошибка при обновлении услуги в проекте');
  }
}

// Функция для получения названия проекта
function getProjectName(projectId) {
  const project = projects.value.find(p => p.id === projectId);
  return project?.name || 'Проект не найден';
}

// Функция для получения названия услуги
function getFavourName(favourId) {
  const favour = favours.value.find(f => f.id === favourId);
  return favour?.name || 'Услуга не найдена';
}

// Функция для получения имени сотрудника
function getEmployeeName(employeeUserId) {
  const employee = employees.value.find(e => e.user === employeeUserId);
  if (!employee) return 'Не назначен';
  
  return employee.user_username || employee.user_profile_fio || `Сотрудник #${employee.id}`;
}

// Группировка услуг по проектам
const groupedProjectServices = ref({});

function groupServicesByProject() {
  const grouped = {};
  projectServices.value.forEach(service => {
    const projectId = service.project;
    if (!grouped[projectId]) {
      grouped[projectId] = {
        project: getProjectName(projectId),
        services: []
      };
    }
    grouped[projectId].services.push(service);
  });
  return grouped;
}

// Обновляем группировку при изменении данных
import { watch } from 'vue';
watch([projectServices, projects, favours, employees], () => {
  groupedProjectServices.value = groupServicesByProject();
}, { immediate: true });

onMounted(async () => {
  await fetchProjectServices();
  await fetchProjects();
  await fetchFavours();
  await fetchEmployees();
})
</script>

<template>
  <div class="p-3">
    <!-- Форма привязки услуги к проекту -->
    <div class="mb-3">
      <h5>Привязать услугу к проекту</h5>
      <div class="row mb-2">
        <div class="col-md-4">
          <label for="project-select" class="form-label">Проект</label>
          <select id="project-select" name="project" v-model="projectServiceToAdd.project" class="form-select">
            <option value="">Выберите проект</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name }} ({{ project.client_user_username || 'Клиент' }})
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="favour-select" class="form-label">Услуга</label>
          <select id="favour-select" name="favour" v-model="projectServiceToAdd.favour" class="form-select">
            <option value="">Выберите услугу</option>
            <option v-for="favour in favours" :key="favour.id" :value="favour.id">
              {{ favour.name }} ({{ favour.price }} ₽)
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="employee-select" class="form-label">Исполнитель</label>
          <select id="employee-select" name="employee_user" v-model="projectServiceToAdd.employee_user" class="form-select">
            <option value="">Выберите исполнителя</option>
            <option v-for="employee in employees" :key="employee.id" :value="employee.user">
              {{ employee.user_username || employee.user_profile_fio }} ({{ employee.position }})
            </option>
          </select>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-md-3">
          <label for="status-select" class="form-label">Статус</label>
          <select id="status-select" name="status" v-model="projectServiceToAdd.status" class="form-select">
            <option value="in_progress">В работе</option>
            <option value="completed">Завершена</option>
            <option value="on_hold">На паузе</option>
            <option value="cancelled">Отменена</option>
          </select>
        </div>
        <div class="col-md-3">
          <label for="end-date-input" class="form-label">Дата завершения</label>
          <input id="end-date-input" name="end_date" v-model="projectServiceToAdd.end_date" type="date" class="form-control"/>
        </div>
        <div class="col-md-3">
          <label for="hours-input" class="form-label">Затрачено часов</label>
          <input id="hours-input" name="hours_spent" v-model="projectServiceToAdd.hours_spent" type="number" step="0.5" class="form-control" placeholder="0.0"/>
        </div>
        <div class="col-md-3">
          <label for="notes-input" class="form-label">Примечания</label>
          <input id="notes-input" name="notes" v-model="projectServiceToAdd.notes" type="text" class="form-control" placeholder="Введите примечания..."/>
        </div>
      </div>
      
      <button @click="onProjectServiceAdd" class="btn btn-primary">
        <i class="bi bi-plus-square"></i> Привязать услугу
      </button>
    </div>

    <div class="mb-3">
      <button @click="fetchProjectServices" class="btn btn-primary">Загрузить услуги в проектах</button>
      <span class="ms-2">Загружено: {{ projectServices.length }}</span>
    </div>
    
    <!-- Список услуг по проектам -->
    <div>
      <h5>Услуги в проектах</h5>
      <div v-if="projectServices.length === 0" class="text-muted">
        Услуги в проектах не найдены
      </div>
      <div v-else>
        <div v-for="(group, projectId) in groupedProjectServices" :key="projectId" class="mb-4">
          <div class="card">
            <div class="card-header bg-light">
              <h6 class="mb-0">Проект: {{ group.project }}</h6>
            </div>
            <div class="card-body p-0">
              <div v-for="item in group.services" :key="item.id" class="border-bottom p-3 d-flex justify-content-between align-items-center">
                <div class="flex-grow-1">
                  <strong>Услуга:</strong> {{ item.favour_name || getFavourName(item.favour) }}<br>
                  <strong>Исполнитель:</strong> {{ item.employee_user_username || getEmployeeName(item.employee_user) }} | 
                  <strong>Статус:</strong> 
                  <span :class="{
                    'text-primary': item.status === 'in_progress',
                    'text-success': item.status === 'completed',
                    'text-warning': item.status === 'on_hold',
                    'text-danger': item.status === 'cancelled'
                  }">
                    {{ statusMap[item.status] || item.status }}
                  </span><br>
                  <strong>Часы:</strong> {{ item.hours_spent }} | 
                  <strong>Дата завершения:</strong> {{ item.end_date || 'Не указана' }}
                  <div v-if="item.notes" class="mt-1">
                    <strong>Примечания:</strong> {{ item.notes }}
                  </div>
                </div>
                <div class="ms-3">
                  <button
                    class="btn btn-success btn-sm me-1"
                    @click="onProjectServiceEditClick(item)"
                    data-bs-toggle="modal"
                    data-bs-target="#editProjectServiceModal"
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
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования услуги в проекте -->
    <div class="modal fade" id="editProjectServiceModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Редактировать услугу в проекте
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
                  <select class="form-select" v-model="projectServiceToEdit.project">
                    <option value="">Выберите проект</option>
                    <option :value="project.id" v-for="project in projects">
                      {{ project.name }} ({{ project.client_user_username || 'Клиент' }})
                    </option>
                  </select>
                  <label>Проект</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="projectServiceToEdit.favour">
                    <option value="">Выберите услугу</option>
                    <option :value="favour.id" v-for="favour in favours">
                      {{ favour.name }} ({{ favour.price }} ₽)
                    </option>
                  </select>
                  <label>Услуга</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="projectServiceToEdit.employee_user">
                    <option value="">Выберите исполнителя</option>
                    <option :value="employee.user" v-for="employee in employees">
                      {{ employee.user_username || employee.user_profile_fio }} ({{ employee.position }})
                    </option>
                  </select>
                  <label>Исполнитель</label>
                </div>
              </div>
              <div class="col-md-3">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="projectServiceToEdit.status">
                    <option value="in_progress">В работе</option>
                    <option value="completed">Завершена</option>
                    <option value="on_hold">На паузе</option>
                    <option value="cancelled">Отменена</option>
                  </select>
                  <label>Статус</label>
                </div>
              </div>
              <div class="col-md-3">
                <div class="form-floating mb-3">
                  <input
                    type="number"
                    step="0.5"
                    class="form-control"
                    v-model="projectServiceToEdit.hours_spent"
                  />
                  <label>Затрачено часов</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <input
                    type="date"
                    class="form-control"
                    v-model="projectServiceToEdit.end_date"
                  />
                  <label>Дата завершения</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <textarea
                    class="form-control"
                    v-model="projectServiceToEdit.notes"
                    style="height: 100px"
                  ></textarea>
                  <label>Примечания</label>
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
              @click="onUpdateProjectService"
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