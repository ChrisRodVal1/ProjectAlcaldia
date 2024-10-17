<template>
  <div>
    <h2 class="title">Usuarios Registrados</h2>
    <input 
      v-model="searchTerm" 
      placeholder="Buscar usuarios..." 
      class="form-control" 
    />

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre Completo</th>
            <th>Email</th>
            <th>Password</th>
            <th>Fecha Registrada</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.nombre }}</td>
            <td>{{ user.correo }}</td>
            <td>{{ user.contraseña }}</td>
            <td>{{ user.fecha_creacion }}</td>
            <td>
              <button class="btn edit" @click="openEditModal(user)">Edit</button>
              <button class="btn delete" @click="openDeleteModal(user)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal">
      <div class="modal-content">
        <h3>¿Está seguro de que desea eliminar {{ selectedUser.nombre }}?</h3>
        <button class="btn delete" @click="confirmDelete">Confirm Delete</button>
        <button class="btn cancel" @click="closeDeleteModal">Cancel</button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h3>Editar Usuario: {{ selectedUser.nombre }}</h3>
        <label for="editName">Name:</label>
        <input v-model="editUserName" id="editName" type="text" class="form-control"/>
        <label for="editEmail">Email:</label>
        <input v-model="editUserEmail" id="editEmail" type="email" class="form-control"/>
        <label for="editPassword">Password:</label>
        <input v-model="editUserPassword" id="editPassword" type="password" class="form-control"/>
        <button class="btn edit" @click="confirmEdit">Save Changes</button>
        <button class="btn cancel" @click="closeEditModal">Cancel</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue';
import { api } from '../../Api'; 
import { bus } from '../../bus';

const searchTerm = ref('');
const users = ref([]);
const filteredUsers = computed(() => {
  const term = searchTerm.value.toLowerCase();
  return users.value.filter(user =>
    user.nombre.toLowerCase().includes(term) 
  );
});

// Modal state management
const showDeleteModal = ref(false);
const showEditModal = ref(false);
const selectedUser = ref(null);
const editUserName = ref('');
const editUserEmail = ref('');
const editUserPassword = ref('');

// Fetch users from the backend
const fetchUsers = async () => {
  try {
    const response = await api.getUsers();
    users.value = response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

// Call fetchUsers when the component is mounted
onMounted(() => {
  fetchUsers();
  bus.on('user-deleted', fetchUsers);
  bus.on('user-updated', fetchUsers);
});

// Functions to open/close modals
const openDeleteModal = (user) => {
  selectedUser.value = user;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
};

const openEditModal = (user) => {
  selectedUser.value = user;
  editUserName.value = user.nombre;
  editUserEmail.value = user.correo;
  editUserPassword.value = user.contraseña;
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
};

// Confirm delete and edit actions
const confirmDelete = async () => {
  if (selectedUser.value) {
    showDeleteModal.value = false;
    try {
      await api.deleteUser(selectedUser.value.id); 
      await fetchUsers(); 
      bus.emit('user-deleted'); 
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  }
};

const confirmEdit = async () => {
  const updatedUser = {
    id: selectedUser.value.id,
    nombre: editUserName.value,
    contraseña: editUserPassword.value,
    correo: editUserEmail.value,
  };
  showEditModal.value = false;
  try {
    await api.editUser(updatedUser); 
    await fetchUsers(); 
    bus.emit('user-updated');
  } catch (error) {
    console.error('Error updating user:', error);
  }
};
</script>

<style scoped>
.title {
  color: #482778;
  margin-bottom: 10px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #6D56A0;
  border-radius: 4px;
  background-color: #482778;
  color: white;
}

.form-control::placeholder {
  color: white;
  opacity: 0.7;
}

.form-control:focus {
  background-color: #482778;
  color: white;
  border-color: #6D56A0;
  outline: none;
}

.table-container {
  max-height: 230px;
  overflow-y: auto;
  border: 1px solid #6D56A0;
  position: relative;
  background-color: #6F565F;
}

.table {
  width: 100%;
  border-collapse: collapse;
  color: white;
}

.table th {
  position: sticky;
  top: 0;
  background-color: #482778;
  color: white;
  z-index: 1;
}

.table th,
.table td {
  padding: 8px; 
  text-align: left; 
  white-space: nowrap; 
}

.table tbody tr:nth-of-type(odd) {
  background-color: #3C3C3B; 
}

.table tbody tr:hover {
  background-color: #6D56A0; 
}


.btn {
  padding: 10px 15px; 
  border: none; 
  border-radius: 4px; 
  color: white;
  cursor: pointer;
  transition: background-color 0.3s; 
}


.btn.edit {
  background-color: #6D56A0; 
}

.btn.delete {
  background-color: #C32A2A; 
}

.btn.cancel {
  background-color: #6F565F; 
}

.btn:hover {
  opacity: 0.8; 
}

.modal {
  position: fixed;
  top: 0;
  left: 0; 
  right: 0; 
  bottom: 0; 
  background-color: rgba(0, 0, 0, 0.5);
  display: flex; 
  align-items: center; 
  justify-content: center; 
}

.modal-content {
  background-color: #482778; 
  padding: 20px; 
  border-radius: 8px; 
  width: 300px; 
  color: white;
}

.modal-content h3 {
  color: white; 
}

.modal-content button {
  width: 100%; 
}
</style>


