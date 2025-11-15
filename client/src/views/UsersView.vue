<script setup>
import axios from "axios"
import { onMounted, ref } from 'vue';
import Cookies from 'js-cookie';

const users = ref([]);
const userToAdd = ref({
  username: '',
  email: '',
  password: '',
  password_confirmation: '',
  fio: '',
  birthday: ''
});
const userToEdit = ref({});

// Добавляем CSRF токен во все запросы
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

async function fetchUsers() {
  try {
    const r = await axios.get("/api/users/")  
    users.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки пользователей:', error);
  }
}

async function onUserAdd() {
  if (!userToAdd.value.username || !userToAdd.value.password) {
    alert('Заполните обязательные поля: имя пользователя и пароль');
    return;
  }

  if (userToAdd.value.password !== userToAdd.value.password_confirmation) {
    alert('Пароли не совпадают');
    return;
  }

  try {
    await axios.post("/api/users/", {
      username: userToAdd.value.username,
      email: userToAdd.value.email,
      password: userToAdd.value.password
      // FIO и birthday будут созданы автоматически через сигнал
    });
    
    // Очищаем форму
    userToAdd.value = {
      username: '',
      email: '',
      password: '',
      password_confirmation: '',
      fio: '',
      birthday: ''
    };
    
    // Обновляем список пользователей
    await fetchUsers();
    
    alert('Пользователь успешно создан!');
  } catch (error) {
    console.error('Ошибка при создании пользователя:', error);
    alert('Ошибка при создании пользователя: ' + (error.response?.data?.detail || error.message));
  }
}

// Удаление пользователя
async function onRemoveClick(user) {
  if (confirm(`Удалить пользователя "${user.username}"?`)) {
    try {
      await axios.delete(`/api/users/${user.id}/`);
      await fetchUsers();
      alert('Пользователь удален!');
    } catch (error) {
      console.error('Ошибка при удалении пользователя:', error);
      alert('Ошибка при удалении пользователя');
    }
  }
}

// Редактирование пользователя - открытие модального окна
function onUserEditClick(user) {
  userToEdit.value = { 
    ...user,
    fio: user.userprofile?.fio || '',
    birthday: user.userprofile?.birthday || ''
  };
}

// Сохранение изменений пользователя
async function onUpdateUser() {
  try {
    // Для обновления нужно отправить отдельный запрос для User и UserProfile
    await axios.put(`/api/users/${userToEdit.value.id}/`, {
      username: userToEdit.value.username,
      email: userToEdit.value.email,
      // Пароль не обновляем если не изменен
    });
    
    // Обновляем UserProfile если есть изменения
    if (userToEdit.value.fio || userToEdit.value.birthday) {
      await axios.patch(`/api/user-profiles/${userToEdit.value.id}/`, {
        fio: userToEdit.value.fio,
        birthday: userToEdit.value.birthday
      });
    }
    
    await fetchUsers();
    alert('Пользователь обновлен!');
  } catch (error) {
    console.error('Ошибка при обновлении пользователя:', error);
    alert('Ошибка при обновлении пользователя');
  }
}

// Функция для форматирования даты
function formatDate(dateString) {
  if (!dateString) return 'Не указана';
  return new Date(dateString).toLocaleDateString();
}

onMounted(async () => {
  await fetchUsers();
})
</script>

<template>
  <div class="p-3">
    <!-- Форма добавления пользователя -->
    <div class="mb-3">
      <h5>Добавление пользователя</h5>
      <div class="row mb-2">
        <div class="col-md-6">
          <label for="username-input" class="form-label">Имя пользователя *</label>
          <input id="username-input" name="username" v-model="userToAdd.username" type="text" class="form-control" placeholder="Введите имя пользователя..." required/>
        </div>
        <div class="col-md-6">
          <label for="email-input" class="form-label">Email</label>
          <input id="email-input" name="email" v-model="userToAdd.email" type="email" class="form-control" placeholder="Введите email..."/>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-md-6">
          <label for="password-input" class="form-label">Пароль *</label>
          <input id="password-input" name="password" v-model="userToAdd.password" type="password" class="form-control" placeholder="Введите пароль..." required/>
        </div>
        <div class="col-md-6">
          <label for="password-confirm-input" class="form-label">Подтверждение пароля *</label>
          <input id="password-confirm-input" name="password_confirmation" v-model="userToAdd.password_confirmation" type="password" class="form-control" placeholder="Подтвердите пароль..." required/>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-md-6">
          <label for="fio-input" class="form-label">ФИО</label>
          <input id="fio-input" name="fio" v-model="userToAdd.fio" type="text" class="form-control" placeholder="Введите ФИО..."/>
        </div>
        <div class="col-md-6">
          <label for="birthday-input" class="form-label">Дата рождения</label>
          <input id="birthday-input" name="birthday" v-model="userToAdd.birthday" type="date" class="form-control"/>
        </div>
      </div>
      
      <button @click="onUserAdd" class="btn btn-primary">
        <i class="bi bi-plus-square"></i> Добавить пользователя
      </button>
      <small class="form-text text-muted d-block mt-1">* - обязательные поля</small>
    </div>

    <div class="mb-3">
      <button @click="fetchUsers" class="btn btn-primary">Загрузить пользователей</button>
      <span class="ms-2">Загружено: {{ users.length }}</span>
    </div>
    
    <!-- Список пользователей -->
    <div>
      <h5>Список пользователей</h5>
      <div v-if="users.length === 0" class="text-muted">
        Пользователей нет
      </div>
      <div v-else>
        <div v-for="item in users" :key="item.id" class="mb-2 p-2 border d-flex justify-content-between align-items-center">
          <div class="flex-grow-1">
            <strong>Имя пользователя:</strong> {{ item.username }}<br>
            <strong>Email:</strong> {{ item.email || 'Не указан' }}<br>
            <strong>ФИО:</strong> {{ item.userprofile?.fio || 'Не указано' }}<br>
            <strong>Дата рождения:</strong> {{ formatDate(item.userprofile?.birthday) }}
          </div>
          <div>
            <button
              class="btn btn-success btn-sm me-1"
              @click="onUserEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editUserModal"
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

    <!-- Модальное окно редактирования пользователя -->
    <div class="modal fade" id="editUserModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Редактировать пользователя
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
                    v-model="userToEdit.username"
                  />
                  <label>Имя пользователя</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <input
                    type="email"
                    class="form-control"
                    v-model="userToEdit.email"
                  />
                  <label>Email</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="userToEdit.fio"
                  />
                  <label>ФИО</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <input
                    type="date"
                    class="form-control"
                    v-model="userToEdit.birthday"
                  />
                  <label>Дата рождения</label>
                </div>
              </div>
            </div>
            <div class="alert alert-info">
              <small>Для смены пароля используйте специальную функцию сброса пароля.</small>
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
              @click="onUpdateUser"
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