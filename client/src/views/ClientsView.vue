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
const clientPictureRef = ref();
const clientAddImageUrl = ref();
const clientEditPictureRef = ref();
const clientEditImageUrl = ref();
const imageModalUrl = ref('');

// Добавляем CSRF токен во все запросы
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

async function fetchClients() {
  try {
    const r = await axios.get("/api/clients/")  
    clients.value = r.data;
  } catch (error) {
    console.error('Ошибка загрузки клиентов:', error);
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

async function onClientAdd() {
  if (!clientToAdd.value.user || !clientToAdd.value.sphere) {
    alert('Заполните пользователя и сферу деятельности');
    return;
  }

  try {
    const formData = new FormData();
    
    // Добавляем файл если выбран
    if (clientPictureRef.value && clientPictureRef.value.files[0]) {
      formData.append('picture', clientPictureRef.value.files[0]);
    }
    
    // Добавляем остальные поля
    formData.set('user', clientToAdd.value.user);
    formData.set('sphere', clientToAdd.value.sphere);
    formData.set('company_name', clientToAdd.value.company_name);

    await axios.post("/api/clients/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    // Очищаем форму
    clientToAdd.value = {
      user: '',
      sphere: '',
      company_name: ''
    };
    clientAddImageUrl.value = null;
    if (clientPictureRef.value) {
      clientPictureRef.value.value = '';
    }
    
    // Обновляем список клиентов
    await fetchClients();
    
    alert('Клиент успешно добавлен!');
  } catch (error) {
    console.error('Ошибка при добавлении клиента:', error);
    alert('Ошибка при добавлении клиента');
  }
}

// Функция для предпросмотра картинки при добавлении
function clientAddPictureChange() {
  if (clientPictureRef.value && clientPictureRef.value.files[0]) {
    clientAddImageUrl.value = URL.createObjectURL(clientPictureRef.value.files[0]);
  }
}

// Функция для предпросмотра картинки при редактировании
function clientEditPictureChange() {
  if (clientEditPictureRef.value && clientEditPictureRef.value.files[0]) {
    clientEditImageUrl.value = URL.createObjectURL(clientEditPictureRef.value.files[0]);
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

// Удаление картинки клиента
async function onRemovePicture(client) {
  if (confirm('Удалить логотип компании?')) {
    try {
      // Отправляем запрос на удаление картинки
      await axios.patch(`/api/clients/${client.id}/`, {
        picture: null
      });
      
      await fetchClients();
      alert('Логотип удален!');
    } catch (error) {
      console.error('Ошибка при удалении логотипа:', error);
      alert('Ошибка при удалении логотипа');
    }
  }
}

// Редактирование клиента - открытие модального окна
function onClientEditClick(client) {
  clientToEdit.value = { ...client };
  clientEditImageUrl.value = client.picture || null;
  if (clientEditPictureRef.value) {
    clientEditPictureRef.value.value = '';
  }
}

// Сохранение изменений клиента
async function onUpdateClient() {
  try {
    const formData = new FormData();
    
    // Добавляем файл если выбран новый
    if (clientEditPictureRef.value && clientEditPictureRef.value.files[0]) {
      formData.append('picture', clientEditPictureRef.value.files[0]);
    }
    
    // Добавляем остальные поля
    formData.set('user', clientToEdit.value.user);
    formData.set('sphere', clientToEdit.value.sphere);
    formData.set('company_name', clientToEdit.value.company_name);

    await axios.put(`/api/clients/${clientToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    await fetchClients();
    alert('Клиент обновлен!');
  } catch (error) {
    console.error('Ошибка при обновлении клиента:', error);
    alert('Ошибка при обновлении клиента');
  }
}

// Удаление картинки в модальном окне редактирования
function removeEditPicture() {
  clientEditImageUrl.value = null;
  clientToEdit.value.picture = null;
  if (clientEditPictureRef.value) {
    clientEditPictureRef.value.value = '';
  }
}

// Открытие модального окна с картинкой
function openImageModal(imageUrl) {
  imageModalUrl.value = imageUrl;
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
          <select id="user-select" name="user" v-model="clientToAdd.user" class="form-select">
            <option value="">Выберите пользователя</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }} ({{ user.email }})
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="sphere-input" class="form-label">Сфера деятельности</label>
          <input id="sphere-input" name="sphere" v-model="clientToAdd.sphere" type="text" class="form-control" placeholder="Введите текст..."/>
        </div>
        <div class="col-md-4">
          <label for="company-input" class="form-label">Название компании</label>
          <input id="company-input" name="company" v-model="clientToAdd.company_name" type="text" class="form-control" placeholder="Введите текст..."/>
        </div>
      </div>
      
      <!-- Поле для загрузки картинки -->
      <div class="row mb-2">
        <div class="col-md-6">
          <label class="form-label">Логотип компании</label>
          <input class="form-control" type="file" ref="clientPictureRef" @change="clientAddPictureChange" accept="image/*">
        </div>
        <div class="col-md-6">
          <div v-if="clientAddImageUrl" class="mt-4">
            <img :src="clientAddImageUrl" style="max-height: 100px; max-width: 100%;" class="border rounded" alt="Предпросмотр">
          </div>
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
          <div class="d-flex align-items-center">
            <!-- Картинка клиента с возможностью увеличения -->
            <div v-if="item.picture" class="me-3 position-relative">
              <img 
                :src="item.picture" 
                style="max-height: 60px; max-width: 60px; cursor: pointer;" 
                class="border rounded" 
                alt="Логотип"
                @click="openImageModal(item.picture)"
                data-bs-toggle="modal" 
                data-bs-target="#imageModal"
              >
              <!-- Кнопка удаления картинки -->
              <button 
                class="btn btn-sm btn-danger position-absolute top-0 start-100 translate-middle"
                style="width: 20px; height: 20px; padding: 0; font-size: 10px;"
                @click="onRemovePicture(item)"
                title="Удалить логотип"
              >
                ×
              </button>
            </div>
            <div>
              <strong>Сфера деятельности:</strong> {{ item.sphere }}
              <span v-if="item.company_name"> | <strong>Компания:</strong> {{ item.company_name }}</span>
              <span v-if="item.user_username"> | <strong>Пользователь:</strong> {{ item.user_username }}</span>
            </div>
          </div>
          <div>
            <button class="btn btn-success btn-sm me-1" @click="onClientEditClick(item)" data-bs-toggle="modal" data-bs-target="#editClientModal">
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
                  <select class="form-select" v-model="clientToEdit.user">
                    <option value="">Выберите пользователя</option>
                    <option :value="user.id" v-for="user in users">
                      {{ user.username }} ({{ user.email }})
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
                    v-model="clientToEdit.sphere"
                  />
                  <label>Сфера деятельности</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <div class="form-floating mb-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="clientToEdit.company_name"
                  />
                  <label>Название компании</label>
                </div>
              </div>
            </div>
            
            <!-- Поле для изменения картинки -->
            <div class="row">
              <div class="col-md-6">
                <label class="form-label">Изменить логотип</label>
                <input class="form-control" type="file" ref="clientEditPictureRef" @change="clientEditPictureChange" accept="image/*">
              </div>
              <div class="col-md-6">
                <div class="mt-4 position-relative">
                  <div v-if="clientEditImageUrl">
                    <p class="small text-muted mb-1">Новое изображение:</p>
                    <img :src="clientEditImageUrl" style="max-height: 100px; max-width: 100%;" class="border rounded" alt="Предпросмотр">
                  </div>
                  <div v-else-if="clientToEdit.picture">
                    <p class="small text-muted mb-1">Текущее изображение:</p>
                    <div class="position-relative d-inline-block">
                      <img :src="clientToEdit.picture" style="max-height: 100px; max-width: 100%;" class="border rounded" alt="Текущий логотип">
                      <button 
                        class="btn btn-sm btn-danger position-absolute top-0 end-0"
                        style="transform: translate(50%, -50%); width: 20px; height: 20px; padding: 0; font-size: 10px;"
                        @click="removeEditPicture"
                        title="Удалить логотип"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                  <div v-else>
                    <p class="small text-muted">Логотип не установлен</p>
                  </div>
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

    <!-- Модальное окно для просмотра картинки -->
    <div class="modal fade" id="imageModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Просмотр изображения</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="imageModalUrl" style="max-width: 100%; max-height: 70vh;" class="img-fluid" alt="Увеличенное изображение">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
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

/* Стиль для кликабельных картинок */
img[style*="cursor: pointer"]:hover {
  opacity: 0.8;
  transform: scale(1.05);
  transition: all 0.2s ease;
}
</style>