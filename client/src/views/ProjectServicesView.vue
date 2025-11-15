<script setup>
import axios from "axios"
import { onMounted, ref, computed } from 'vue';
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
  'cancelled': 'Отменена',
  'approval': 'На согласовании'
};

async function fetchProjectServices() {
  try {
    const r = await axios.get("/api/project-services/")  
    projectServices.value = r.data;
    console.log('Загружено услуг в проектах:', projectServices.value);
  } catch (error) {
    console.error('Ошибка загрузки услуг в проектах:', error);
  }
}

async function fetchProjects() {
  try {
    const r = await axios.get("/api/projects/")  
    projects.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки проектов:', error);
  }
}

async function fetchFavours() {
  try {
    const r = await axios.get("/api/favours/")  
    favours.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки услуг:', error);
  }
}

async function fetchEmployees() {
  try {
    const r = await axios.get("/api/employees/")  
    employees.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки сотрудников:', error);
  }
}

async function onProjectServiceAdd() {
  if (!projectServiceToAdd.value.project || !projectServiceToAdd.value.favour) {
    alert('Заполните обязательные поля: проект и услуга');
    return;
  }

  try {
    console.log('Данные для отправки:', projectServiceToAdd.value);
    
    // Подготовка данных в соответствии с моделью Django
    const requestData = {
      project: parseInt(projectServiceToAdd.value.project),
      favour: parseInt(projectServiceToAdd.value.favour),
      employee_user: projectServiceToAdd.value.employee_user ? 
        parseInt(projectServiceToAdd.value.employee_user) : null,
      status: projectServiceToAdd.value.status,
      end_date: projectServiceToAdd.value.end_date || null,
      hours_spent: parseFloat(projectServiceToAdd.value.hours_spent) || 0,
      notes: projectServiceToAdd.value.notes || ''
    };

    console.log('Отправляемые данные:', requestData);
    
    const response = await axios.post("/api/project-services/", requestData);
    
    console.log('Ответ сервера:', response.data);
    
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
    
    await fetchProjectServices();
    alert('Услуга успешно привязана к проекту!');
  } catch (error) {
    console.error('Полная ошибка при привязке услуги к проекту:', error);
    
    // Детальная обработка ошибок
    if (error.response) {
      console.error('Статус ошибки:', error.response.status);
      console.error('Данные ошибки:', error.response.data);
      
      // Пытаемся извлечь полезную информацию из ошибки
      let errorMessage = 'Неизвестная ошибка сервера';
      
      if (error.response.data && typeof error.response.data === 'object') {
        // Если ошибка в формате JSON
        if (error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response.data.non_field_errors) {
          errorMessage = error.response.data.non_field_errors.join(', ');
        } else {
          // Собираем все ошибки полей
          const fieldErrors = [];
          for (const [field, errors] of Object.entries(error.response.data)) {
            fieldErrors.push(`${field}: ${Array.isArray(errors) ? errors.join(', ') : errors}`);
          }
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join('; ');
          }
        }
      } else if (typeof error.response.data === 'string') {
        // Если ошибка в виде HTML, пытаемся извлечь текст
        const match = error.response.data.match(/<pre class="exception_value">([^<]+)<\/pre>/);
        if (match) {
          errorMessage = match[1].trim();
        }
      }
      
      alert(`Ошибка при привязке услуги к проекту: ${errorMessage}`);
    } else if (error.request) {
      alert('Не удалось подключиться к серверу');
    } else {
      alert(`Ошибка: ${error.message}`);
    }
  }
}

// Удаление услуги из проекта
async function onRemoveClick(projectService) {
  const favourName = getFavourName(projectService.favour) || 'услугу';
  if (confirm(`Удалить услугу "${favourName}" из проекта?`)) {
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
  // Копируем данные, преобразуя в простые значения для формы
  projectServiceToEdit.value = {
    id: projectService.id,
    project: typeof projectService.project === 'object' ? projectService.project.id : projectService.project,
    favour: typeof projectService.favour === 'object' ? projectService.favour.id : projectService.favour,
    employee_user: projectService.employee_user ? 
      (typeof projectService.employee_user === 'object' ? projectService.employee_user.id : projectService.employee_user) : '',
    status: projectService.status,
    end_date: projectService.end_date || '',
    hours_spent: parseFloat(projectService.hours_spent) || 0,
    notes: projectService.notes || ''
  };
}

// Сохранение изменений услуги в проекте
async function onUpdateProjectService() {
  try {
    console.log('Данные для обновления:', projectServiceToEdit.value);
    
    const requestData = {
      project: parseInt(projectServiceToEdit.value.project),
      favour: parseInt(projectServiceToEdit.value.favour),
      employee_user: projectServiceToEdit.value.employee_user ? 
        parseInt(projectServiceToEdit.value.employee_user) : null,
      status: projectServiceToEdit.value.status,
      end_date: projectServiceToEdit.value.end_date || null,
      hours_spent: parseFloat(projectServiceToEdit.value.hours_spent) || 0,
      notes: projectServiceToEdit.value.notes || ''
    };
    
    console.log('Отправляемые данные для обновления:', requestData);
    
    await axios.put(`/api/project-services/${projectServiceToEdit.value.id}/`, requestData);
    
    await fetchProjectServices();
    alert('Услуга в проекте обновлена!');
  } catch (error) {
    console.error('Ошибка при обновлении услуги в проекте:', error);
    console.error('Детали ошибки:', error.response?.data);
    alert(`Ошибка при обновлении услуги в проекте: ${error.response?.data?.detail || error.message}`);
  }
}

// Функция для получения названия проекта
function getProjectName(projectId) {
  if (!projectId) return 'Проект не указан';
  
  // Если projectId - это объект
  if (typeof projectId === 'object') {
    return projectId.name || `Проект #${projectId.id || 'unknown'}`;
  }
  
  // Если projectId - это число или строка
  const projectIdStr = String(projectId);
  const project = projects.value.find(p => String(p.id) === projectIdStr);
  
  return project?.name || `Проект #${projectId}`;
}

// Функция для получения названия услуги
function getFavourName(favourId) {
  if (!favourId) return 'Услуга не указана';
  
  // Если favourId - это объект
  if (typeof favourId === 'object') {
    return favourId.name || `Услуга #${favourId.id || 'unknown'}`;
  }
  
  // Если favourId - это число или строка
  const favourIdStr = String(favourId);
  const favour = favours.value.find(f => String(f.id) === favourIdStr);
  
  return favour?.name || `Услуга #${favourId}`;
}

// Функция для получения имени сотрудника
function getEmployeeName(employeeUserId) {
  if (!employeeUserId) return 'Не назначен';
  
  // Если employeeUserId - это объект
  if (typeof employeeUserId === 'object') {
    return employeeUserId.username || 
           employeeUserId.first_name + ' ' + employeeUserId.last_name || 
           `Сотрудник #${employeeUserId.id || 'unknown'}`;
  }
  
  // Если employeeUserId - это число или строка
  const employeeIdStr = String(employeeUserId);
  const employee = employees.value.find(e => String(e.user) === employeeIdStr || String(e.id) === employeeIdStr);
  
  if (!employee) return 'Не назначен';
  
  return employee.user_username || 
         (employee.first_name && employee.last_name ? `${employee.first_name} ${employee.last_name}` : 'Сотрудник') || 
         `Сотрудник #${employee.id}`;
}

// Функция для получения даты начала (если есть в данных)
function getStartDate(projectService) {
  return projectService.start_date || 'Автоматически';
}

// Группировка услуг по проектам с использованием computed
const groupedProjectServices = computed(() => {
  const grouped = {};
  projectServices.value.forEach(service => {
    // Получаем ID проекта
    let projectId;
    if (typeof service.project === 'object') {
      projectId = service.project.id;
    } else {
      projectId = service.project;
    }
    
    if (!grouped[projectId]) {
      grouped[projectId] = {
        project: getProjectName(service.project),
        projectId: projectId,
        services: []
      };
    }
    grouped[projectId].services.push(service);
  });
  return grouped;
});

// Функция для форматирования Decimal часов
function formatHours(hours) {
  if (!hours) return '0';
  return parseFloat(hours).toFixed(2);
}

onMounted(async () => {
  await Promise.all([
    fetchProjectServices(),
    fetchProjects(),
    fetchFavours(),
    fetchEmployees()
  ]);
});
</script>

<template>
  <div class="p-3">
    <!-- Форма привязки услуги к проекту -->
    <div class="mb-4 card">
      <div class="card-header">
        <h5 class="mb-0">Привязать услугу к проекту</h5>
      </div>
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-4">
            <label for="project-select" class="form-label">Проект *</label>
            <select id="project-select" name="project" v-model="projectServiceToAdd.project" class="form-select" required>
              <option value="">Выберите проект</option>
              <option v-for="project in projects" :key="project.id" :value="project.id">
                {{ project.name }} ({{ project.client_user_username || 'Клиент' }})
              </option>
            </select>
          </div>
          <div class="col-md-4">
            <label for="favour-select" class="form-label">Услуга *</label>
            <select id="favour-select" name="favour" v-model="projectServiceToAdd.favour" class="form-select" required>
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
                {{ employee.user_username || (employee.first_name && employee.last_name ? `${employee.first_name} ${employee.last_name}` : `Сотрудник #${employee.id}`) }} 
                <template v-if="employee.position">({{ employee.position }})</template>
              </option>
            </select>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col-md-3">
            <label for="status-select" class="form-label">Статус</label>
            <select id="status-select" name="status" v-model="projectServiceToAdd.status" class="form-select">
              <option value="in_progress">В работе</option>
              <option value="completed">Завершена</option>
              <option value="on_hold">На паузе</option>
              <option value="cancelled">Отменена</option>
              <option value="approval">На согласовании</option>
            </select>
          </div>
          <div class="col-md-3">
            <label for="end-date-input" class="form-label">Дата завершения</label>
            <input id="end-date-input" name="end_date" v-model="projectServiceToAdd.end_date" type="date" class="form-control"/>
          </div>
          <div class="col-md-3">
            <label for="hours-input" class="form-label">Затрачено часов</label>
            <input id="hours-input" name="hours_spent" v-model="projectServiceToAdd.hours_spent" type="number" step="0.01" min="0" class="form-control" placeholder="0.00"/>
          </div>
          <div class="col-md-3">
            <label for="notes-input" class="form-label">Примечания</label>
            <input id="notes-input" name="notes" v-model="projectServiceToAdd.notes" type="text" class="form-control" placeholder="Введите примечания..."/>
          </div>
        </div>
        
        <button @click="onProjectServiceAdd" class="btn btn-primary">
          <i class="bi bi-plus-square"></i> Привязать услугу
        </button>
        <small class="form-text text-muted d-block mt-1">* - обязательные поля</small>
      </div>
    </div>

    <div class="mb-3">
      <button @click="fetchProjectServices" class="btn btn-outline-primary">
        <i class="bi bi-arrow-clockwise"></i> Обновить список
      </button>
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
            <div class="card-header bg-light d-flex justify-content-between align-items-center">
              <h6 class="mb-0">Проект: {{ group.project }}</h6>
              <span class="badge bg-primary">Услуг: {{ group.services.length }}</span>
            </div>
            <div class="card-body p-0">
              <div v-for="item in group.services" :key="item.id" class="border-bottom p-3">
                <div class="d-flex justify-content-between align-items-start">
                  <div class="flex-grow-1">
                    <div class="row">
                      <div class="col-md-6">
                        <strong>Услуга:</strong> {{ getFavourName(item.favour) }}<br>
                        <strong>Исполнитель:</strong> {{ getEmployeeName(item.employee_user) }}<br>
                        <strong>Статус:</strong> 
                        <span :class="{
                          'badge bg-primary': item.status === 'in_progress',
                          'badge bg-success': item.status === 'completed',
                          'badge bg-warning': item.status === 'on_hold' || item.status === 'approval',
                          'badge bg-danger': item.status === 'cancelled'
                        }">
                          {{ statusMap[item.status] || item.status }}
                        </span>
                      </div>
                      <div class="col-md-6">
                        <strong>Дата начала:</strong> {{ getStartDate(item) }}<br>
                        <strong>Дата завершения:</strong> {{ item.end_date || 'Не указана' }}<br>
                        <strong>Затрачено часов:</strong> {{ formatHours(item.hours_spent) }}
                      </div>
                    </div>
                    <div v-if="item.notes && item.notes.trim() && item.notes !== '-'" class="mt-2">
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
                    <option :value="project.id" v-for="project in projects" :key="project.id">
                      {{ project.name }} ({{ project.client_user_username || 'Клиент' }})
                    </option>
                  </select>
                  <label>Проект *</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="projectServiceToEdit.favour">
                    <option value="">Выберите услугу</option>
                    <option :value="favour.id" v-for="favour in favours" :key="favour.id">
                      {{ favour.name }} ({{ favour.price }} ₽)
                    </option>
                  </select>
                  <label>Услуга *</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <select class="form-select" v-model="projectServiceToEdit.employee_user">
                    <option value="">Выберите исполнителя</option>
                    <option :value="employee.user" v-for="employee in employees" :key="employee.id">
                      {{ employee.user_username || (employee.first_name && employee.last_name ? `${employee.first_name} ${employee.last_name}` : `Сотрудник #${employee.id}`) }} 
                      <template v-if="employee.position">({{ employee.position }})</template>
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
                    <option value="approval">На согласовании</option>
                  </select>
                  <label>Статус</label>
                </div>
              </div>
              <div class="col-md-3">
                <div class="form-floating mb-3">
                  <input
                    type="number"
                    step="0.01"
                    min="0"
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
                    placeholder="Введите примечания..."
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
              :disabled="!projectServiceToEdit.project || !projectServiceToEdit.favour"
            >
              Сохранить изменения
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
.badge {
  font-size: 0.75em;
}
</style>