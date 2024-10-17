<template>
  <div ref="map" class="map-container"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { bus } from '../../bus';
import { api } from '../../Api'; 

const map = ref(null);
const directionsRenderers = ref([]); 
const initializeMap = async () => {
  const googleMap = new window.google.maps.Map(map.value, {
    center: { lat: -17.3895000, lng: -66.1568000 },
    zoom: 13,
  });

  const directionsService = new window.google.maps.DirectionsService();
  await fetchHistories(directionsService, googleMap);

  // Set up event listener for user-deleted event
  bus.on('user-deleted', async () => {
    await fetchHistories(directionsService, googleMap);
  });
};

const fetchHistories = async (directionsService, googleMap) => {
  // Clear existing directions
  directionsRenderers.value.forEach(renderer => renderer.setMap(null));
  directionsRenderers.value = []; 

  try {
    // Fetch histories data from the backend
    const response = await api.getHistories();
    const histories = response.data;

    // Loop through each history and draw the paths on the map
    histories.forEach(history => {
      const pathCoords = history.camino; 
      const waypoints = [];

      // Create LatLng objects for each coordinate pair
      for (let i = 0; i < pathCoords.length; i++) {
        const coords = pathCoords[i].split(',').map(Number); 
        waypoints.push({ location: new window.google.maps.LatLng(coords[0], coords[1]), stopover: false });
      }

      if (waypoints.length < 2) return;

      const request = {
        origin: waypoints[0].location,
        destination: waypoints[waypoints.length - 1].location,
        waypoints: waypoints.slice(1, -1), // All waypoints except the first and last
        travelMode: window.google.maps.TravelMode.DRIVING, // Change to WALKING or BICYCLING as needed
      };

      // Create a new DirectionsRenderer for each path with a unique color
      const directionsRenderer = new window.google.maps.DirectionsRenderer({
        polylineOptions: {
          strokeColor: getRandomColor(), // Assign a random color for each path
          strokeWeight: 4,
        },
        map: googleMap,
      });

      // Store the DirectionsRenderer instance
      directionsRenderers.value.push(directionsRenderer);

      // Call Directions API
      directionsService.route(request, (result, status) => {
        if (status === window.google.maps.DirectionsStatus.OK) {
          directionsRenderer.setDirections(result);
        } else {
          console.error('Directions request failed due to ' + status);
        }
      });
    });
  } catch (error) {
    console.error('Error fetching histories:', error);
  }
};

onMounted(() => {
  initializeMap();
});

// Function to generate random colors
const getRandomColor = () => {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};
</script>

<style scoped>
.map-container {
  height: 500px;
  width: 100%;
}
</style>
