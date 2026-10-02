import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/HomePage.vue';
import AboutPage from './views/AboutPage.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/about',
    name: 'AboutPage',
    component: AboutPage,
    props: route => ({ selectedLab: route.query.selectedLab, selectedProblem: route.query.selectedProblem })
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;


