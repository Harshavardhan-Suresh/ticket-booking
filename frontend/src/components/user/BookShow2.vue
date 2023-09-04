<template>
  <div>
    <div style="text-align: center">
      <h1 style="background-color: rgb(234, 111, 131) !important">
        {{ venue.name }}
      </h1>
    </div>
    <nav
      class="navbar"
      style="
        background-color: lightgoldenrodyellow !important;
        width: 40%;
        margin-left: 30%;
        height: 50px;
        justify-content: space-around;
      "
    >
      <div class="navbar-links days">
        <ul>
          <li>
            <router-link :to="'/venue/book/' + venue.id + '/1'">{{
              day[0]
            }}</router-link>
          </li>
          <li>
            <router-link :to="'/venue/book/' + venue.id + '/2'">{{
              day[1]
            }}</router-link>
          </li>
          <li>
            <router-link :to="'/venue/book/' + venue.id + '/3'">{{
              day[2]
            }}</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <div style="text-align: center">
      <h4>{{ today }}</h4>
    </div>
    <div style="display: flex; justify-content: center">
      <div style="display: flex; align-items: center">
        <svg width="40" height="40">
          <circle cx="20" cy="20" r="16" fill="green" />
        </svg>
        <span style="margin-left: 8px; font-size: 20px">Available</span>
      </div>
      <div style="display: flex; align-items: center; margin-left: 20px">
        <svg width="40" height="40">
          <circle cx="20" cy="20" r="16" fill="red" />
        </svg>
        <span style="margin-left: 8px; font-size: 20px">Houseful</span>
      </div>
    </div>

    <div
      class="venues1"
      style="flex-direction: column"
      :style="
        this.shows.length > 0 ? 'margin-left : 37.5%' : 'margin-left : 0%'
      "
    >
      <div v-if="shows.length > 0">
        <div
          v-for="show in shows"
          :key="show.id"
          class="card main_card"
          style="width: 18rem"
        >
          <div class="card-body">
            <h3 class="card-title">{{ show.show_name }}</h3>
            <div v-for="screen in show.screens" :key="screen.id">
              <a
                v-if="screen.available_seats"
                :href="'/buy/ticket/' + screen.id"
                style="text-decoration: none"
              >
                <div class="card" style="width: 12rem">
                  <div class="card-body">
                    <h3 class="card-title" style="color: green">
                      {{ screen.time }}
                    </h3>
                  </div>
                </div>
              </a>
              <div v-else>
                <div class="card" style="width: 12rem">
                  <div class="card-body">
                    <h3 class="card-title" style="color: red">
                      {{ screen.time }}
                    </h3>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div style="text-align: center">
          <h3 class="card-text" style="font-size: 25px; font-weight: bold">
            No Shows
          </h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api.js";
import axios from "axios";
export default {
  data() {
    return {
      venue: {},
      today: "",
      day: [],
      shows: [],
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      const venueId = this.$route.params.venue_id;
      const token = localStorage.getItem("access_token");
      try {
        // Fetch venue details
        if (token) {
          const venueResponse = await api.get(`/api/venue/${venueId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.venue = venueResponse.data;
          // Get today's date and create days list
          const today = new Date();

          for (let i = 0; i < 3; i++) {
            const day = new Date(today);
            day.setDate(day.getDate() + i);
            if (i == this.$route.params.date - 1) {
              this.today = day.toLocaleDateString("en-US", {
                day: "numeric",
                month: "long",
                year: "numeric",
              });
            }
            this.day.push(
              day.toLocaleDateString("en-US", {
                day: "numeric",
                month: "long",
                year: "numeric",
              })
            );
          }

          // Fetch all screens
          const screensResponse = await api.get("/api/screen/all", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const screens = screensResponse.data.screens;

          // Filter screens for the selected show and date
          console.log(screens);
          const filteredScreens = screens.filter(
            (screen) =>
              screen.venue_id == venueId &&
              this.isDate1OnDate2(screen.timing, this.today)
          );
          console.log(filteredScreens);
          // Fetch available seats for each screen
          const requests = filteredScreens.map((screen) => {
            return axios.get(
              `http://localhost:5000/api/seat/available?screen_id=${screen.id}`,
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );
          });

          // Wait for all requests to complete
          const responses = await axios.all(requests);
          this.shows = [];
          const shows = {};
          for (let i = 0; i < responses.length; i++) {
            const screen = filteredScreens[i];
            if (screen.show_id in shows) {
              continue;
            }
            shows[screen.show_id] = {
              id: screen.show_id,
              show_name: screen.show,
              screens: [],
            };
          }
          for (let i = 0; i < responses.length; i++) {
            const screen = filteredScreens[i];
            const availableSeats = responses[i].data.available_seats;

            shows[screen.show_id].screens.push({
              id: screen.id,
              time: this.formatDateTime(screen.timing),
              date: this.formatDate(screen.timing),
              available_seats: availableSeats,
            });
          }
          for (let x in shows) {
            this.shows.push(shows[x]);
          }
          // Sort screens within each show by time
          this.shows.forEach((show) => {
            show.screens.sort((a, b) => new Date(a.time) - new Date(b.time));
          });
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error(error);
      }
    },
    formatDateTime(dateTimeStr) {
      return new Date(dateTimeStr).toLocaleString("en-US", {
        hour: "numeric",
        minute: "numeric",
        hour12: true,
      });
    },
    isDate1OnDate2(date1, date2) {
      // Convert date strings to Date objects
      const date1Obj = new Date(date1);
      const date2Obj = new Date(date2);

      // Convert Date objects to date strings in the format "month day, year"
      const dateString1 = date1Obj.toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
      });
      const dateString2 = date2Obj.toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
      });

      // Compare the date strings to check if Date 1 lies on Date 2
      return dateString1 === dateString2;
    },
    formatDate(dateTimeStr) {
      return new Date(dateTimeStr).toLocaleDateString("en-US", {
        day: "numeric",
        month: "long",
        year: "numeric",
      });
    },
  },
  watch: {
    // Watch for changes in the route and update 'date'
    $route(to) {
      const date = to.params.date;
      if (date && date >= 1 && date <= 3) {
        this.today = this.day[this.url_date - 1];
        this.fetchData();
      }
    },
  },
};
</script>

<style>
/* Add your CSS styles here */
</style>
