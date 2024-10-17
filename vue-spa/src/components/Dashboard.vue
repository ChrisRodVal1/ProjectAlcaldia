<template>
  <div>
    <Header @logout="logout" />

    <div class="container mt-3">

      <PDFReport />
      
      <div class="table-wrapper">
        <UserTable />
      </div>

      <div class="table-wrapper">
        <DestinationTable />
      </div>

      <div class="table-wrapper">
        <HistoryTable />
      </div>

      <h2>Mapa</h2>
      <div class="map-wrapper">
        <Map />
      </div>
    </div>

    <div class="container mt-3">
      <LiveChat /> <!-- Use your own icon here -->
    </div>

    <Footer />
  </div>
</template>


<script setup>
import Header from './layout/Header.vue';
import Footer from './layout/Footer.vue';
import UserTable from './tables/UserTable.vue';
import DestinationTable from './tables/DestinationTable.vue';
import HistoryTable from './tables/HistoryTable.vue';
import Map from './other/Map.vue';
import PDFReport from './other/PDFReport.vue';
import { defineEmits } from 'vue';
import LiveChat from './other/LiveChat.vue';

// Define emit for logout
const emit = defineEmits(['logout']);


// Methods for actions
function logout() {
  emit('logout');
}
</script>


<style scoped>
.container {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.table-wrapper {
  margin-bottom: 20px;
}

.map-wrapper {
  margin-bottom: 50px;
}

h2 {
  color: #482778;
}

.filter-input {
  margin-bottom: 10px;
  display: block;
  border: 1px solid #6D56A0;
  padding: 8px;
  border-radius: 4px;
}

button {
  background-color: #482778;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #6D56A0;
}

.table {
  border: 1px solid #3C3C3B;
}

.table-header {
  background-color: #6D56A0;
  color: white;
}

.table-row:hover {
  background-color: #EDEDED;
}

footer {
  background-color: #6F565F;
  color: white;
  padding: 10px;
  text-align: center;
  border-radius: 0 0 8px 8px;
}

.map {
  border: 1px solid #482778;
  border-radius: 8px;
  overflow: hidden;
}

.header {
  background-color: #6D56A0;
  color: white;
  padding: 15px;
  text-align: center;
}

.footer {
  background-color: #6F565F;
  color: white;
  padding: 10px;
  text-align: center;
}
</style>

