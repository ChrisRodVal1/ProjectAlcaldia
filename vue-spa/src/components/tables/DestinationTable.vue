<template>
  <div>
    <h2 class="title">Destinos</h2>
    <input 
      v-model="searchTerm" 
      placeholder="Buscar destinos..." 
      class="form-control" 
    />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Usuario ID</th>
            <th>Ubicación Inicial</th>
            <th>Ubicación Final</th>
            <th>Duración (min)</th>
            <th>Medio Esperado</th>
            <th>Fecha Registrada</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="destination in filteredDestinations" :key="destination.id">
            <td>{{ destination.id }}</td>
            <td>{{ destination.id_usuario }}</td>
            <td>{{ destination.ubicacion_inicial }}</td>
            <td>{{ destination.ubicacion_final }}</td>
            <td>{{ destination.duracion_estimada_minutos }}</td>
            <td>{{ destination.medio_esperado }}</td>
            <td>{{ destination.fecha_creacion }}</td>
            <td>
              <button class="btn edit" @click="openEditModal(destination)">Edit</button>
              <button class="btn delete" @click="openDeleteModal(destination)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal">
      <div class="modal-content">
        <h3>¿Está seguro de que desea eliminar {{ selectedDestination.ubicacion_inicial }}?</h3>
        <button class="btn delete" @click="confirmDelete">Confirmar Eliminación</button>
        <button class="btn cancel" @click="closeDeleteModal">Cancelar</button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h3>Editar Destino: {{ selectedDestination.ubicacion_inicial }}</h3>
        <label for="editDeparture">Ubicación Inicial:</label>
        <input v-model="editDeparture" id="editDeparture" type="text" class="form-control" />
        <label for="editDestination">Ubicación Final:</label>
        <input v-model="editDestination" id="editDestination" type="text" class="form-control" />
        <label for="editDuration">Duración (min):</label>
        <input v-model="editDuration" id="editDuration" type="number" class="form-control" />
        <label for="editTransportation">Medio de Transporte:</label>
        <input v-model="editTransportation" id="editTransportation" type="text" class="form-control" />
        <button class="btn edit" @click="confirmEdit">Guardar Cambios</button>
        <button class="btn cancel" @click="closeEditModal">Cancelar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { api } from '../../Api'; 
import { bus } from '../../bus';

const searchTerm = ref('');
const destinations = ref([]);
const filteredDestinations = computed(() => {
  const term = searchTerm.value.toLowerCase();
  return destinations.value.filter(destination =>
    destination.ubicacion_inicial.toLowerCase().includes(term) 
  );
});

// Modal state management
const showDeleteModal = ref(false);
const showEditModal = ref(false);
const selectedDestination = ref(null);
const editDeparture = ref('');
const editDestination = ref('');
const editDuration = ref('');
const editTransportation = ref('');

// Fetch destinations from the backend
const fetchDestinations = async () => {
  try {
    const response = await api.getDestinations();
    destinations.value = response.data;
  } catch (error) {
    console.error('Error fetching destinations:', error);
  }
};

// Call fetchDestinations when the component is mounted
onMounted(() => {
  fetchDestinations();
  
  // Listen for the 'user-deleted' event
  bus.on('user-deleted', () => {
    fetchDestinations(); // Refresh destinations when a user is deleted
  });

  bus.on('user-updated', () => {
    fetchDestinations(); // Refresh destinations when a user is deleted
  });
});

// Functions to open/close modals
const openDeleteModal = (destination) => {
  selectedDestination.value = destination;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
};

const openEditModal = (destination) => {
  selectedDestination.value = destination;
  editDeparture.value = destination.ubicacion_inicial;
  editDestination.value = destination.ubicacion_final;
  editDuration.value = destination.duracion_estimada_minutos;
  editTransportation.value = destination.medio_esperado;
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
};

// Confirm delete and edit actions
const confirmDelete = async () => {
  if (selectedDestination.value) {
    showDeleteModal.value = false;
    try {
      await api.deleteDestination(selectedDestination.value.id); // Ensure this method exists in your API
      await fetchDestinations(); // Refresh the destination list after deletion
      bus.emit('user-deleted');
    } catch (error) {
      console.error('Error deleting destination:', error);
    }
  }
};

const confirmEdit = async () => {
  const updatedDestination = {
    id: selectedDestination.value.id,
    ubicacion_inicial: editDeparture.value,
    ubicacion_final: editDestination.value,
    duracion_estimada_minutos: editDuration.value,
    medio_esperado: editTransportation.value,
  };
  showEditModal.value = false;
  try {
    await api.editDestination(updatedDestination); // Ensure this method exists in your API
    await fetchDestinations(); // Refresh the destination list after editing
    bus.emit('user-updated');
  } catch (error) {
    console.error('Error updating destination:', error);
  }
};

onBeforeUnmount(() => {
  // Cleanup listener when the component is unmounted
  bus.off('user-deleted');
});
</script>

<style scoped>
.title {
  color: #482778; /* Title color */
  margin-bottom: 10px; /* Space below the title */
}

.form-control {
  width: 100%;
  padding: 10px; /* Add padding for better appearance */
  border: 1px solid #6D56A0; /* Medium Purple border */
  border-radius: 4px; /* Rounded corners */
  background-color: #482778; /* Tertiary Color for dark mode */
  color: white; /* White text for input */
}

.form-control::placeholder {
  color: white; /* White placeholder text */
  opacity: 0.7; /* Slightly reduce opacity */
}

.form-control:focus {
  background-color: #482778; /* Keep purple background when focused */
  color: white; /* White text when focused */
  border-color: #6D56A0; /* Keep the same border color */
  outline: none; /* Remove the default focus outline */
}

.table-container {
  max-height: 240px; /* Adjust height as needed */
  overflow-y: auto;  /* Enable vertical scrolling */
  border: 1px solid #6D56A0; /* Medium Purple border */
  position: relative;
  background-color: #6F565F; /* Background Color */
}

.table {
  width: 100%;
  border-collapse: collapse; /* Ensure borders collapse */
  color: white; /* White text for table */
}

.table th {
  position: sticky; /* Use sticky positioning for the header */
  top: 0; /* Stick to the top of the table container */
  background-color: #482778; /* Header background color */
  color: white; /* White text for header */
  z-index: 1; /* Ensure the header is above the scrolling content */
}

.table th,
.table td {
  padding: 8px; /* Add padding to cells */
  text-align: left; /* Align text to the left */
  white-space: nowrap; /* Prevent text from wrapping */
}

.table tbody tr:nth-of-type(odd) {
  background-color: #3C3C3B; /* Tertiary Color for odd rows */
}

.table tbody tr:hover {
  background-color: #6D56A0; /* Medium Purple for highlight on hover */
}

/* Button styling */
.btn {
  padding: 10px 15px; /* Add padding for buttons */
  border: none; /* Remove default border */
  border-radius: 4px; /* Rounded corners */
  color: white; /* White text for buttons */
  cursor: pointer; /* Pointer cursor on hover */
  transition: background-color 0.3s; /* Transition effect for background color */
}

/* Specific button styles */
.btn.edit {
  background-color: #6D56A0; /* Medium Purple background */
}

.btn.delete {
  background-color: #C32A2A; /* Red background for delete button */
}

.btn.cancel {
  background-color: #6F565F; /* Darker background for cancel button */
}

.btn:hover {
  opacity: 0.8; /* Slightly reduce opacity on hover */
}

.modal {
  position: fixed; /* Fixed positioning for modal */
  top: 0; /* Top of the viewport */
  left: 0; /* Left of the viewport */
  right: 0; /* Stretch to the right */
  bottom: 0; /* Stretch to the bottom */
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex; /* Flexbox for centering content */
  align-items: center; /* Center vertically */
  justify-content: center; /* Center horizontally */
}

.modal-content {
  background-color: #482778; /* Modal background color */
  padding: 20px; /* Padding for modal content */
  border-radius: 8px; /* Rounded corners for modal */
  width: 300px; /* Width of the modal */
  color: white;
}

.modal-content h3 {
  color: white; /* Title color in modal */
}

.modal-content button {
  width: 100%; /* Full width buttons in modal */
}
</style>
