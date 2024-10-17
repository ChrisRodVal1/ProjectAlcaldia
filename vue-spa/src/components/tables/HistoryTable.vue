<template>
  <div>
    <h2 class="title">Historial de Destinos Registrados</h2>
    <input 
      v-model="searchTerm" 
      placeholder="Buscar por Hora de Inicio..." 
      class="form-control" 
    />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Ruta ID</th>
            <th>Usuario ID</th>
            <th>Hora Inicio</th>
            <th>Hora Fin</th>
            <th>Camino</th>
            <th>Distancia</th>
            <th>Medio Usado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="history in filteredHistories" :key="history.id">
            <td>{{ history.id }}</td>
            <td>{{ history.id_ruta }}</td>
            <td>{{ history.id_usuario }}</td>
            <td>{{ history.hora_inicio }}</td>
            <td>{{ history.hora_fin }}</td>
            <td>{{ showFirstAndLastCoordinates(history.camino) }}</td>
            <td>{{ history.distanciakm }} km</td>
            <td>{{ history.medio_usado }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue';
import { api } from '../../Api';
import { bus } from '../../bus';

const searchTerm = ref('');
const histories = ref([]);

// Function to fetch histories from the backend
const fetchHistories = async () => {
  try {
    const response = await api.getHistories();
    console.log('Histories:', response.data);
    histories.value = response.data;
  } catch (error) {
    console.error('Error fetching histories:', error);
  }
};

// Fetch histories when the component is mounted
onMounted(() => {
  fetchHistories();

  // Listen for the 'user-deleted' event
  bus.on('user-deleted', () => {
    fetchHistories(); // Refresh destinations when a user is deleted
  });

  bus.on('user-updated', () => {
    fetchHistories(); // Refresh destinations when a user is deleted
  });
});

// Filter histories based on search term
const filteredHistories = computed(() => {
  const term = searchTerm.value.toLowerCase();
  return histories.value.filter(history =>
    history.hora_inicio.toLowerCase().includes(term)
  );
});

// Function to display the first and last coordinates from a path
function showFirstAndLastCoordinates(camino) {
  if (!camino || camino.length === 0) return 'N/A';
  return `${camino[0]} a ${camino[camino.length - 1]}`;
}


onBeforeUnmount(() => {
  // Cleanup listener when the component is unmounted
  bus.off('user-deleted');
});
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

.form-control:focus {
  background-color: #482778;
  color: white;
  border-color: #6D56A0;
  outline: none;
}

.form-control::placeholder {
  color: white;
  opacity: 0.7;
}

.form-control::-webkit-input-placeholder {
  color: white;
}

.form-control:-moz-placeholder {
  color: white;
}

.form-control::-moz-placeholder {
  color: white;
}

.form-control:-ms-input-placeholder {
  color: white;
}

.table-container {
  max-height: 170px;
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

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #3C3C3B;
}

.table-striped tbody tr:hover {
  background-color: #6D56A0;
}
</style>
