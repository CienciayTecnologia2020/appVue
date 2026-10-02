import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'vuetify/styles';
import 'leaflet';
import 'leaflet/dist/leaflet.css';
import Tres from '@tresjs/core'
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

// Configura Vuetify
const vuetify = createVuetify({
  components,
  directives,
});

// Crea la aplicación Vue y úsala para agregar Vuetify
const app = createApp(App);
app.use(vuetify); // Agrega Vuetify
app.use(router);
app.use(Tres);
app.mount('#app');
