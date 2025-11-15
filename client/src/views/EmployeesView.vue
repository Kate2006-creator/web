<script setup>
import axios from "axios"
import { onMounted, ref } from 'vue';
import Cookies from 'js-cookie';

const employees = ref([]);
const users = ref([]);
const employeeToAdd = ref({
  user: '',
  position: '',
  start_work_date: ''
});
const employeeToEdit = ref({});

// Добавляем CSRF токен во все запросы
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

async function fetchEmployees() {
  try {
    const r = await axios.get("/api/employees/")  
    employees.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки сотрудников:', error);
  }
}

async function fetchUsers() {
  try {
    const r = await axios.get("/api/users/")  
    users.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки пользователей:', error);
  }
}

async function onEmployeeAdd() {
  if (!employeeToAdd.value.user || !employeeToAdd.value.position || !employeeToAdd.value.start_work_date) {
    alert('Заполните обязательные поля: пользователь, должность и дата приема на работу');
    return;
  }

  try {
    await axios.post("/api/employees/", {
      ...employeeToAdd.value
    });
    
    // Очищаем форму
    employeeToAdd.value = {
      user: '',
      position: '',
      start_work_date: ''
    };
    
    // Обновляем список сотрудников
    await fetchEmployees();
    
    alert('Сотрудник успешно добавлен!');
  } catch (error) {
    console.error('Ошибка при добавлении сотрудника:', error);
    alert('Ошибка при добавлении сотрудника');
  }
}

// Удаление сотрудника
async function onRemoveClick(employee) {
  if (confirm(`Удалить сотрудника "${employee.position}"?`)) {
    try {
      await axios.delete(`/api/employees/${employee.id}/`);
      await fetchEmployees();
      alert('Сотрудник удален!');
    } catch (error) {
      console.error('Ошибка при удалении сотрудника:', error);
      alert('Ошибка при удалении сотрудника');
    }
  }
}

// Редактирование сотрудника - открытие модального окна
function onEmployeeEditClick(employee) {
  employeeToEdit.value = { ...employee };
}

// Сохранение изменений сотрудника
async function onUpdateEmployee() {
  try {
    await axios.put(`/api/employees/${employeeToEdit.value.id}/`, {
      ...employeeToEdit.value,
    });
    await fetchEmployees();
    alert('Сотрудник обновлен!');
  } catch (error) {
    console.error('Ошибка при обновлении сотрудника:', error);
    alert('Ошибка при обновлении сотрудника');
  }
}

// Функция для получения имени пользователя
function getUserName(userId) {
  const user = users.value.find(u => u.id === userId);
  if (!user) return 'Пользователь не найден';
  
  return user.userprofile?.fio || user.username || `Пользователь #${userId}`;
}

function getUserEmail(userId) {
  const user = users.value.find(u => u.id === userId);
  return user?.email;
}

onMounted(async () => {
  await fetchEmployees();
  await fetchUsers();
})
</script>

<template>
  <div class="p-3">
    <!-- Форма добавления сотрудника -->
    <div class="mb-3">
      <h5>Добавление сотрудника</h5>
      <div class="row mb-2">
        <div class="col-md-4">
          <label for="user-select" class="form-label">Пользователь</label>
          <select id="user-select" name="user" v-model="employeeToAdd.user" class="form-select">
            <option value="">Выберите пользователя</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.userprofile?.fio || user.username }} ({{ user.email }})
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="position-input" class="form-label">Должность</label>
          <input id="position-input" name="position" v-model="employeeToAdd.position" type="text" class="form-control" placeholder="Введите должность..."/>
        </div>
        <div class="col-md-4">
          <label for="start-work-date-input" class="form-label">Дата приема на работу</label>
          <input id="start-work-date-input" name="start_work_date" v-model="employeeToAdd.start_work_date" type="date" class="form-control"/>
        </div>
      </div>
      
      <button @click="onEmployeeAdd" class="btn btn-primary">
        <i class="bi bi-plus-square"></i> Добавить сотрудника
      </button>
    </div>

    <div class="mb-3">
      <button @click="fetchEmployees" class="btn btn-primary">Загрузить сотрудников</button>
      <span class="ms-2">Загружено: {{ employees.length }}</span>
    </div>
    
    <!-- Список сотрудников -->
    <div>
      <h5>Список сотрудников</h5>
      <div v-if="employees.length === 0" class="text-muted">
        Сотрудников нет
      </div>
      <div v-else>
        <div v-for="item in employees" :key="item.id" class="mb-2 p-2 border d-flex justify-content-between align-items-center">
          <div>
            <strong>Пользователь:</strong> {{ getUserName(item.user) }} 
            <span v-if="getUserEmail(item.user)">({{ getUserEmail(item.user) }})</span><br>
            <strong>Должность:</strong> {{ item.position }} | 
            <strong>Дата приема:</strong> {{ item.start_work_date }}
          </div>
          <div>
            <button
              class="btn btn-success btn-sm me-1"
              @click="onEmployeeEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editEmployeeModal"
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

    <!-- Модальное окно редактирования сотрудника -->
    <div class="modal fade" id="editEmployeeModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Редактировать сотрудника
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
                  <select class="form-select" v-model="employeeToEdit.user">
                    <option value="">Выберите пользователя</option>
                    <option :value="user.id" v-for="user in users">
                      {{ user.userprofile?.fio || user.username }} ({{ user.email }})
                    </option>
                  </select>
                  <label>Пользователь</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="employeeToEdit.position"
                  />
                  <label>Должность</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <div class="form-floating">
                  <input
                    type="date"
                    class="form-control"
                    v-model="employeeToEdit.start_work_date"
                  />
                  <label>Дата приема на работу</label>
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
              @click="onUpdateEmployee"
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