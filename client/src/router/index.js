import { createRouter, createWebHistory } from 'vue-router';
import ClientsView from '../views/ClientsView.vue';
import ProjectsView from '../views/ProjectsView.vue';
import EmployeesView from '../views/EmployeesView.vue';
import ReviewsView from '../views/ReviewsView.vue';
import FavoursView from '../views/FavoursView.vue';
import ProjectServicesView from '../views/ProjectServicesView.vue';
import UsersView from '../views/UsersView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "ClientsView",
      component: ClientsView
    },

    {
    path: '/projects',
    name: 'ProjectsView',
    component: ProjectsView
    },

    {
    path: '/employees',
    name: 'EmployeesView',
    component: EmployeesView
    },

    {
    path: '/reviews',
    name: 'ReviewsView',
    component: ReviewsView
    },

    {
    path: '/favours',
    name: 'FavoursView',
    component: FavoursView
    },

    {
    path: '/project-services',
    name: 'ProjectServicesView',
    component: ProjectServicesView
    },
    {
    path: '/users',
    name: 'users',
    component: UsersView
    },
  ]
});

export default router;

