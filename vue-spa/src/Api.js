import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

export const api = {
  getUsers() {
    return axios.get(`${API_URL}/users`);
  },

  deleteUser(userId) {
    return axios.delete(`${API_URL}/users/${userId}`); 
  },

  editUser(user) {
    return axios.put(`${API_URL}/users/${user.id}`, {
      nombre: user.nombre,
      contraseña: user.contraseña,
      correo: user.correo,
    }); 
  },


  getDestinations() {
    return axios.get(`${API_URL}/destinations`);
  },

  deleteDestination(destinationId) {
    return axios.delete(`${API_URL}/destinations/${destinationId}`);
  },

  editDestination(destination) {
    return axios.put(`${API_URL}/destinations/${destination.id}`, {
      ubicacion_inicial: destination.ubicacion_inicial,
      ubicacion_final: destination.ubicacion_final,
      duracion_estimada_minutos: destination.duracion_estimada_minutos,
      medio_esperado: destination.medio_esperado,
    });
  },


  getHistories() {
    return axios.get(`${API_URL}/histories`);
  },

  deleteHistory(historyId) {
    return axios.delete(`${API_URL}/histories/${historyId}`);
  },
  

  
};
