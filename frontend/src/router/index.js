import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "../components/LandingPage.vue";
import SignUp from "../components/user/SignUp.vue";
import UserLogin from "../components/user/UserLogin.vue";
import AdminLogin from "../components/admin/AdminLogin.vue";
import ShowPage from "../components/user/ShowPage.vue";
import PageWithUserNavBar from "../components/user/PageWithUserNavBar.vue";
import PageWithAdminNavBar from "../components/admin/PageWithAdminNavBar.vue";
import PageWithoutNavBar from "../components/PageWithoutNavBar.vue";
import BookShow1 from "../components/user/BookShow1.vue";
import BookShow2 from "../components/user/BookShow2.vue";
import BookTicket from "../components/user/BookTicket.vue";
import BookingPage from "../components/user/BookingPage.vue";
import VenuePage from "../components/user/VenuePage.vue";
import LogoutPage from "../components/user/LogoutPage.vue";
import VenueAdmin from "../components/admin/VenuePage.vue";
import AddVenue from "../components/admin/AddVenue.vue";
import AddScreen from "../components/admin/AddScreen.vue";
import UpdateScreen from "../components/admin/UpdateScreen.vue";
import UpdateVenue from "../components/admin/UpdateVenue.vue";
import CelebritiesPage from "../components/admin/CelebritiesPage.vue";
import AddCelebrity from "../components/admin/AddCelebrity.vue";
import ShowAdmin from "../components/admin/ShowPage.vue";
import AddCast from "../components/admin/AddCast.vue";
import AddShow from "../components/admin/AddShow.vue";
import AddTag from "../components/admin/AddTag.vue";
import UpdateShow from "../components/admin/UpdateShow.vue";
import StatisticsPage from "../components/admin/StatisticsPage.vue";
const routes = [
  {
    path: "/",
    name: "landingPage",
    component: PageWithoutNavBar,
    children: [
      {
        path: "",
        component: LandingPage,
      },
    ],
  },
  {
    path: "/user/signup",
    name: "signUp",
    component: PageWithoutNavBar,
    children: [
      {
        path: "",
        component: SignUp,
      },
    ],
  },
  {
    path: "/user",
    name: "userLogin",
    component: PageWithoutNavBar,
    children: [
      {
        path: "",
        component: UserLogin,
      },
    ],
  },
  {
    path: "/admin",
    name: "adminLogin",
    component: PageWithoutNavBar,
    children: [
      {
        path: "",
        component: AdminLogin,
      },
    ],
  },
  {
    path: "/user/show",
    name: "showPage",
    component: PageWithUserNavBar,
    children: [
      {
        path: "",
        component: ShowPage,
      },
    ],
  },
  {
    path: "/show/book/:show_id/:date",
    name: "bookShow1",
    component: PageWithUserNavBar,
    children: [
      {
        path: "",
        component: BookShow1,
      },
    ],
  },
  {
    path: "/buy/ticket/:screen_id",
    name: "bookTicket",
    component: PageWithUserNavBar,
    children: [
      {
        path: "",
        component: BookTicket,
      },
    ],
  },
  {
    path: "/user/bookings",
    name: "bookingPage",
    component: PageWithUserNavBar,
    children: [
      {
        path: "",
        component: BookingPage,
      },
    ],
  },
  {
    path: "/user/venue",
    name: "venuePage",
    component: PageWithUserNavBar,
    children: [
      {
        path: "",
        component: VenuePage,
      },
    ],
  },
  {
    path: "/venue/book/:venue_id/:date",
    name: "bookShow2",
    component: PageWithUserNavBar,
    children: [
      {
        path: "",
        component: BookShow2,
      },
    ],
  },
  {
    path: "/logout",
    name: "logoutPage",
    component: PageWithoutNavBar,
    children: [
      {
        path: "",
        component: LogoutPage,
      },
    ],
  },
  {
    path: "/venue",
    name: "venueAdmin",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: VenueAdmin,
      },
    ],
  },
  {
    path: "/venue/add",
    name: "addVenue",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: AddVenue,
      },
    ],
  },
  {
    path: "/screen/add/:venue_id",
    name: "addScreen",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: AddScreen,
      },
    ],
  },
  {
    path: "/screen/update/:screen_id",
    name: "updateScreen",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: UpdateScreen,
      },
    ],
  },
  {
    path: "/venue/update/:venue_id",
    name: "updateVenue",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: UpdateVenue,
      },
    ],
  },
  {
    path: "/celebrity",
    name: "celebritiesPage",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: CelebritiesPage,
      },
    ],
  },
  {
    path: "/celebrity/add",
    name: "addCelebrity",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: AddCelebrity,
      },
    ],
  },
  {
    path: "/show",
    name: "showAdmin",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: ShowAdmin,
      },
    ],
  },
  {
    path: "/cast/add/:show_id",
    name: "addCast",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: AddCast,
      },
    ],
  },
  {
    path: "/show/add",
    name: "addShow",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: AddShow,
      },
    ],
  },
  {
    path: "/tag/add/:show_id",
    name: "addTag",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: AddTag,
      },
    ],
  },
  {
    path: "/show/update/:show_id",
    name: "updateShow",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: UpdateShow,
      },
    ],
  },
  {
    path: "/statistics",
    name: "statisticsPage",
    component: PageWithAdminNavBar,
    children: [
      {
        path: "",
        component: StatisticsPage,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
