<template>
  <button @click="showModal = true">Generar Reporte PDF</button>

  <!-- Modal for confirmation and filters -->
  <div v-if="showModal" class="modal">
    <div class="modal-content">

      <div>
        <h4 class="title">Filtrar Usuarios</h4>
        <label>
          Nombre:
          <input v-model="userFilter.name" type="text" placeholder="Nombre del usuario" class="form-control">
        </label>
        <h6 class="title">Seleccionar columnas</h6>
        <label><input type="checkbox" v-model="userColumns.id"> ID</label>
        <label><input type="checkbox" v-model="userColumns.name"> Nombre Completo</label>
        <label><input type="checkbox" v-model="userColumns.email"> Email</label>
        <label><input type="checkbox" v-model="userColumns.password"> Contraseña</label>
        <label><input type="checkbox" v-model="userColumns.date"> Fecha Registrada</label>
      </div>

      <div>
        <h4 class="title">Filtrar Destinos</h4>
        <label>
          Fecha de registro (Desde):
          <input v-model="destinationFilter.startDate" type="date" class="form-control">
        </label>
        <label>
          Fecha de registro (Hasta):
          <input v-model="destinationFilter.endDate" type="date" class="form-control">
        </label>
        <h5 class="title">Seleccionar columnas</h5>
        <label><input type="checkbox" v-model="destinationColumns.id"> ID</label>
        <label><input type="checkbox" v-model="destinationColumns.userId"> Usuario ID</label>
        <label><input type="checkbox" v-model="destinationColumns.startLocation"> Ub. Inicial</label>
        <label><input type="checkbox" v-model="destinationColumns.endLocation"> Ub. Final</label>
        <label><input type="checkbox" v-model="destinationColumns.duration"> Duracion Estimada</label>
        <label><input type="checkbox" v-model="destinationColumns.medium"> Medio Esperado</label>
        <label><input type="checkbox" v-model="destinationColumns.date"> Fecha Registrada</label>
      </div>

      <div>
        <h4 class="title">Filtrar Historial de Destinos</h4>
        <label>
          Medio usado:
          <select v-model="historyFilter.medioUsado" class="form-control">
            <option value="">Todos</option>
            <option value="Auto">Auto</option>
            <option value="Bicicleta">Bicicleta</option>
            <option value="A Pie">A Pie</option>
          </select>
        </label>
        <h5 class="title">Seleccionar columnas</h5>
        <label><input type="checkbox" v-model="historyColumns.id"> ID</label>
        <label><input type="checkbox" v-model="historyColumns.routeId"> Ruta ID</label>
        <label><input type="checkbox" v-model="historyColumns.userId"> Usuario ID</label>
        <label><input type="checkbox" v-model="historyColumns.startTime"> Hora Inicio</label>
        <label><input type="checkbox" v-model="historyColumns.endTime"> Hora Fin</label>
        <label><input type="checkbox" v-model="historyColumns.distance"> Distancia</label>
        <label><input type="checkbox" v-model="historyColumns.path"> Camino</label>
        <label><input type="checkbox" v-model="historyColumns.medium"> Medio Usado</label>
      </div>
      <div>
        <label>
          Enviar Reporte:
          <input v-model="userFilter.name" type="text" placeholder="Email..." class="form-control">
        </label>
      </div>

      <button class="btn edit" @click="applyFilters">Generar Reporte</button>
      <button class="btn cancel" @click="showModal = false">Cancelar</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import { api } from '../../Api'; 

const Users = ref([]);
const Destinations = ref([]);
const Histories = ref([]);
const showModal = ref(false);

// Filters for each table
const userFilter = ref({ name: '' });
const destinationFilter = ref({ startDate: '', endDate: '' });
const historyFilter = ref({ medioUsado: '' });

// Column selection
const userColumns = ref({ id: true, name: true, email: true, password: true, date: true });
const destinationColumns = ref({ id: true, userId: true, startLocation: true, endLocation: true, duration: true, medium: true, date: true });
const historyColumns = ref({ id: true, routeId: true, userId: true, startTime: true, endTime: true, distance: true, path: true, medium: true });

onMounted(async () => {
  await fetchData();
});

async function fetchData() {
  try {
    const usersResponse = await api.getUsers();
    const destinationsResponse = await api.getDestinations();
    const historiesResponse = await api.getHistories();

    Users.value = await usersResponse.json();
    Destinations.value = await destinationsResponse.json();
    Histories.value = await historiesResponse.json();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

function applyFilters() {
  // Apply filters to the data before generating the PDF
  const filteredUsers = Users.value.filter(user => 
    user.nombre.toLowerCase().includes(userFilter.value.name.toLowerCase())
  );

  const filteredDestinations = Destinations.value.filter(destination => {
    const creationDate = new Date(destination.fecha_creacion);
    const startDate = destinationFilter.value.startDate ? new Date(destinationFilter.value.startDate) : null;
    const endDate = destinationFilter.value.endDate ? new Date(destinationFilter.value.endDate) : null;

    return (!startDate || creationDate >= startDate) &&
           (!endDate || creationDate <= endDate);
  });

  const filteredHistories = Histories.value.filter(history => 
    history.medio_usado.includes(historyFilter.value.medioUsado)
  );

  // Generate PDF with the filtered data
  generatePDF(filteredUsers, filteredDestinations, filteredHistories);
  showModal.value = false;  // Close the modal
}

function resetFields() {
  // Reset all fields and checkboxes
  userFilter.value = { name: '' };
  destinationFilter.value = { startDate: '', endDate: '' };
  historyFilter.value = { medioUsado: '' };

  userColumns.value = { id: true, name: true, email: true, password: true, date: true };
  destinationColumns.value = { id: true, userId: true, startLocation: true, endLocation: true, duration: true, medium: true, date: true };
  historyColumns.value = { id: true, routeId: true, userId: true, startTime: true, endTime: true, distance: true, path: true, medium: true };
}

function addHeaderAndFooter(doc, pageNumber) {
  const totalPages = doc.internal.getNumberOfPages();
  doc.setFontSize(10);
  doc.text('Reporte de Usuarios, Destinos y Historial', 14, 10);
  doc.setFontSize(8);
  doc.text(`Página ${pageNumber} de ${totalPages}`, doc.internal.pageSize.width - 20, doc.internal.pageSize.height - 10);
}

function generatePDF(filteredUsers, filteredDestinations, filteredHistories) {
  const doc = new jsPDF();

  doc.setFontSize(22);
  doc.text('Reporte de Destinos y Rutas', doc.internal.pageSize.width / 2, 60, { align: 'center' });

  // Users Section
  if (filteredUsers.length > 0) {
    doc.addPage();
    addHeaderAndFooter(doc, doc.internal.getNumberOfPages());

    const userHeaders = [];
    if (userColumns.value.id) userHeaders.push("ID");
    if (userColumns.value.name) userHeaders.push("Nombre Completo");
    if (userColumns.value.email) userHeaders.push("Email");
    if (userColumns.value.password) userHeaders.push("Contraseña");
    if (userColumns.value.date) userHeaders.push("Fecha Registrada");

    const userBody = filteredUsers.map(user => {
      const row = [];
      if (userColumns.value.id) row.push(user.id);
      if (userColumns.value.name) row.push(user.nombre);
      if (userColumns.value.email) row.push(user.correo);
      if (userColumns.value.password) row.push(user.contraseña);
      if (userColumns.value.date) row.push(user.fecha_creacion);
      return row;
    });

    if (userHeaders.length) {
      doc.autoTable({ head: [userHeaders], body: userBody });
    }
  }

  // Destinations Section
  if (filteredDestinations.length > 0) {
    doc.addPage();
    addHeaderAndFooter(doc, doc.internal.getNumberOfPages());

    const destinationHeaders = [];
    if (destinationColumns.value.id) destinationHeaders.push("ID");
    if (destinationColumns.value.userId) destinationHeaders.push("Usuario ID");
    if (destinationColumns.value.startLocation) destinationHeaders.push("Ub. Inicial");
    if (destinationColumns.value.endLocation) destinationHeaders.push("Ub. Final");
    if (destinationColumns.value.duration) destinationHeaders.push("Duracion Estimada");
    if (destinationColumns.value.medium) destinationHeaders.push("Medio Esperado");
    if (destinationColumns.value.date) destinationHeaders.push("Fecha Registrada");

    const destinationBody = filteredDestinations.map(destination => {
      const row = [];
      if (destinationColumns.value.id) row.push(destination.id);
      if (destinationColumns.value.userId) row.push(destination.id_usuario);
      if (destinationColumns.value.startLocation) row.push(destination.ubicacion_inicial);
      if (destinationColumns.value.endLocation) row.push(destination.ubicacion_final);
      if (destinationColumns.value.duration) row.push(destination.duracion_estimada_minutos);
      if (destinationColumns.value.medium) row.push(destination.medio_esperado);
      if (destinationColumns.value.date) row.push(destination.fecha_creacion);
      return row;
    });

    if (destinationHeaders.length) {
      doc.autoTable({ head: [destinationHeaders], body: destinationBody });
    }
  }

  // Histories Section
  if (filteredHistories.length > 0) {
    doc.addPage();
    addHeaderAndFooter(doc, doc.internal.getNumberOfPages());

    const historyHeaders = [];
    if (historyColumns.value.id) historyHeaders.push("ID");
    if (historyColumns.value.routeId) historyHeaders.push("Ruta ID");
    if (historyColumns.value.userId) historyHeaders.push("Usuario ID");
    if (historyColumns.value.startTime) historyHeaders.push("Hora Inicio");
    if (historyColumns.value.endTime) historyHeaders.push("Hora Fin");
    if (historyColumns.value.distance) historyHeaders.push("Distancia");
    if (historyColumns.value.path) historyHeaders.push("Camino");
    if (historyColumns.value.medium) historyHeaders.push("Medio Usado");

    const historyBody = filteredHistories.map(history => {
      const row = [];
      if (historyColumns.value.id) row.push(history.id);
      if (historyColumns.value.routeId) row.push(history.id_ruta);
      if (historyColumns.value.userId) row.push(history.id_usuario);
      if (historyColumns.value.startTime) row.push(history.hora_inicio);
      if (historyColumns.value.endTime) row.push(history.hora_fin);
      if (historyColumns.value.distance) row.push(history.distanciakm);
      if (historyColumns.value.path) row.push(history.camino);
      if (historyColumns.value.medium) row.push(history.medio_usado);
      return row;
    });

    if (historyHeaders.length) {
      doc.autoTable({ head: [historyHeaders], body: historyBody });
    }
  }

  doc.save('reporte_destinos_rutas.pdf');

  // Reset fields after PDF generation
  resetFields();
}
</script>



<style scoped>
button {
  background-color: #482778; 
  color: white; 
  padding: 10px 15px; 
  border: none; 
  border-radius: 4px; 
  cursor: pointer; 
  transition: background-color 0.3s; 
}


button:hover {
  background-color: #6D56A0; 
}

.title {
  color: white;
  margin-bottom: 5px;
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
  width: 600px;
  
  color: white;
}

.modal-content h3 {
  color: white;
}

.modal-content button {
  width: 100%;
}
</style>
