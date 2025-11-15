<script setup>
import axios from "axios"
import { onMounted, ref } from 'vue';
import Cookies from 'js-cookie';

const clients = ref([]);
const users = ref([]);
const clientToAdd = ref({
  user: '',
  sphere: '',
  company_name: ''
});
const clientToEdit = ref({});

// Добавляем CSRF токен во все запросы
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

async function fetchClients() {
    const r = await axios.get("/api/clients/")  
    clients.value = r.data;
}

async function fetchUsers() {
    const r = await axios.get("/api/users/")  
    users.value = r.data;
}

async function onClientAdd() {
  if (!clientToAdd.value.user || !clientToAdd.value.sphere) {
    alert('Заполните пользователя и сферу деятельности');
    return;
  }

  try {
    await axios.post("/api/clients/", {
      ...clientToAdd.value
    });
    
    // Очищаем форму
    clientToAdd.value = {
      user: '',
      sphere: '',
      company_name: ''
    };
    
    // Обновляем список клиентов
    await fetchClients();
    
    alert('Клиент успешно добавлен!');
  } catch (error) {
    console.error('Ошибка при добавлении клиента:', error);
    alert('Ошибка при добавлении клиента');
  }
}

// Удаление клиента
async function onRemoveClick(client) {
  if (confirm(`Удалить клиента ${client.company_name || 'без названия'}?`)) {
    try {
      await axios.delete(`/api/clients/${client.id}/`);
      await fetchClients();
      alert('Клиент удален!');
    } catch (error) {
      console.error('Ошибка при удалении клиента:', error);
      alert('Ошибка при удалении клиента');
    }
  }
}

// Редактирование клиента - открытие модального окна
function onClientEditClick(client) {
  clientToEdit.value = { ...client };
}

// Сохранение изменений клиента
async function onUpdateClient() {
  try {
    await axios.put(`/api/clients/${clientToEdit.value.id}/`, {
      ...clientToEdit.value,
    });
    await fetchClients();
    alert('Клиент обновлен!');
  } catch (error) {
    console.error('Ошибка при обновлении клиента:', error);
    alert('Ошибка при обновлении клиента');
  }
}

onMounted(async () => {
  await fetchClients();
  await fetchUsers();
})
</script>

<template>
  <div class="p-3">
    <!-- Форма добавления клиента -->
    <div class="mb-3">
      <h5>Добавление клиента</h5>
      <div class="row mb-2">
        <div class="col-md-4">
          <label for="user-select" class="form-label">Пользователь</label>
          <select id="user-select" name="user" autocomplete="username" v-model="clientToAdd.user" class="form-select">
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }} ({{ user.email }})
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="sphere-input" class="form-label">Сфера деятельности</label>
          <input id="sphere-input" name="sphere" autocomplete="organization-title" v-model="clientToAdd.sphere" type="text" class="form-control" placeholder="Введите текст..."/>
        </div>
        <div class="col-md-4">
          <label for="company-input" class="form-label">Название компании</label>
          <input id="company-input" name="company" autocomplete="organization" v-model="clientToAdd.company_name" type="text" class="form-control" placeholder="Введите текст..."/>
        </div>
      </div>
      
      <button @click="onClientAdd" class="btn btn-primary">
        Добавить клиента
      </button>
    </div>

    <div class="mb-3">
      <button @click="fetchClients" class="btn btn-primary">Загрузить клиентов</button>
      <span class="ms-2">Загружено: {{ clients.length }}</span>
    </div>
    
    <!-- Список клиентов -->
    <div>
      <h5>Список клиентов</h5>
      <div v-if="clients.length === 0" class="text-muted">
        Клиентов нет
      </div>
      <div v-else>
        <div v-for="item in clients" :key="item.id" class="mb-2 p-2 border d-flex justify-content-between align-items-center">
          <div>
            <strong>Сфера деятельности:</strong> {{ item.sphere }}
            <span v-if="item.company_name"> | <strong>Компания:</strong> {{ item.company_name }}</span>
            <span v-if="item.user_username"> | <strong>Пользователь:</strong> {{ item.user_username }}</span>
          </div>
          <div>
            <button
              class="btn btn-success btn-sm me-1"
              @click="onClientEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editClientModal"
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

    <!-- Модальное окно редактирования клиента -->
    <div class="modal fade" id="editClientModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Редактировать клиента
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
                    v-model="clientToEdit.sphere"
                  />
                  <label>Сфера деятельности</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="clientToEdit.company_name"
                  />
                  <label>Название компании</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="clientToEdit.user">
                    <option :value="user.id" v-for="user in users">
                      {{ user.username }} ({{ user.email }})
                    </option>
                  </select>
                  <label>Пользователь</label>
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
              @click="onUpdateClient"
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