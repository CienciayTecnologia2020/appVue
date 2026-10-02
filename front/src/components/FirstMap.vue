<template>
  <div>
    <div id="map" style="height: 550px;"></div>
    <!-- Modal for city description -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-actions>
          <v-btn color="primary" text @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
const apiUrl = process.env.VUE_APP_API_URL;
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

export default {
  props: ['selectedLab'],
  data() {
    return {
      map: null,
      selectedCity: { name: '', description: '' },
      dialog: false,
      cityData: null
    };
  },
  mounted() {
    this.initMap();
    this.fetchLocationData(this.selectedLab);
  },
  watch: {
    selectedLab(newVal) {
      this.fetchLocationData(newVal);
    }
  },
  methods: {
    initMap() {
      // Centrar el mapa en Europa (coordenadas aproximadas para una vista de Europa)
      this.map = L.map('map').setView([54.5260, 15.2551], 4);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
    },
    fetchLocationData(locationId) {
      axios.get(`${apiUrl}/map/${locationId}`)
        .then(response => {
          if (response.data.length > 0) {
            const location = response.data[0];
            this.cityData = {
              lat: location.latitude,
              lng: location.longitude
            };
            this.addCircleMarker(this.cityData);
          } else {
            console.error('Location not found');
            // Si no se encuentra la ubicación, centrar el mapa en Europa
            this.map.setView([54.5260, 15.2551], 4);
          }
        })
        .catch(error => {
          console.error('Error fetching location data:', error);
          // Si hay un error al obtener los datos, centrar el mapa en Europa
          this.map.setView([54.5260, 15.2551], 4);
        });
    },
    addCircleMarker(location) {
      // Limpiar capas existentes
      this.map.eachLayer(layer => {
        if (layer instanceof L.Circle) {
          this.map.removeLayer(layer);
        }
      });

      L.circle([location.lat, location.lng], {
        color: 'red',
        fillColor: 'red',
        fillOpacity: 0.5,
        radius: 5000 // Radio del círculo en metros
      }).addTo(this.map);

      // Centrar el mapa en la ubicación
      this.map.setView([location.lat, location.lng], 10);
    }
  }
};
</script>

<style scoped>
#map {
  width: 450px;
}
</style>
