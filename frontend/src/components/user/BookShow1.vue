<template>
  <div>
    <div style="text-align: center">
      <h1 style="background-color: rgb(234, 111, 131) !important">
        {{ show.name }}
      </h1>
    </div>
    <div style="text-align: center">
      <h2>Cast</h2>
    </div>
    <div class="cele1">
      <div
        v-for="celebrity in show.cast"
        :key="celebrity.id"
        class="card main_card"
        style="width: 18rem; margin-top: 0px"
      >
        <div class="card-body">
          <div v-if="celebrity.photo">
            <img
              class="card-img-top"
              :src="celebrity.photo"
              alt="Card image"
              style="
                background-color: white;
                height: 90px;
                width: 90px;
                border-radius: 45px;
              "
            />
          </div>
          <div v-else>
            <svg
              class="card-img-top"
              xmlns="http://www.w3.org/2000/svg"
              width="80"
              height="80"
              fill="currentColor"
              viewBox="0 0 16 16"
            >
              <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
              <path
                fill-rule="evenodd"
                d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"
              />
            </svg>
          </div>
          <h3 class="card-title">{{ celebrity.name }}</h3>
        </div>
      </div>
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
            <router-link id="day0" :to="'/show/book/' + show.id + '/1'">{{
              day[0]
            }}</router-link>
          </li>
          <li>
            <router-link id="day1" :to="'/show/book/' + show.id + '/2'">{{
              day[1]
            }}</router-link>
          </li>
          <li>
            <router-link id="day2" :to="'/show/book/' + show.id + '/3'">{{
              day[2]
            }}</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <div style="text-align: center">
      <h4>{{ date }}</h4>
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

    <div class="venues1" style="flex-direction: column">
      <div v-if="venues.length > 0" style="margin-left: 37.5%">
        <div
          v-for="venue in venues"
          :key="venue.id"
          class="card main_card"
          style="width: 18rem"
        >
          <div class="card-body">
            <h3 class="card-title">{{ venue.venue_name }}</h3>
            <address style="font-size: 25px">{{ venue.venue_address }}</address>
            <div v-for="screen in venue.screens" :key="screen.id">
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
            No Venues
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
      show: {},
      today: "",
      day: [],
      date: "",
      venues: [],
      showId: "",
      url_date: "",
    };
  },
  created() {
    this.fetchData();
  },

  methods: {
    async fetchData() {
      this.showId = this.$route.params.show_id;
      this.url_date = this.$route.params.date;
      const token = localStorage.getItem("access_token");
      try {
        // Fetch show details
        if (token) {
          const showResponse = await api.get(`/api/show/${this.showId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.show = showResponse.data;

          // Get today's date and create days list
          const today = new Date();
          this.today = today.toLocaleDateString("en-US", {
            day: "numeric",
            month: "long",
            year: "numeric",
          });
          for (let i = 0; i < 3; i++) {
            const day = new Date(today);
            day.setDate(day.getDate() + i);
            if (i == this.url_date - 1) {
              this.date = day.toLocaleDateString("en-US", {
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

          const filteredScreens = screens.filter(
            (screen) =>
              screen.show_id == this.showId &&
              this.isDate1OnDate2(screen.timing, this.date)
          );

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
          console.log(responses);
          this.venues = [];
          const venues = {};
          for (let i = 0; i < responses.length; i++) {
            const screen = filteredScreens[i];
            if (screen.venue_id in venues) {
              continue;
            }
            venues[screen.venue_id] = {
              id: screen.venue_id,
              venue_name: screen.venue_name,
              venue_address: screen.venue_address,
              screens: [],
            };
          }
          for (let i = 0; i < responses.length; i++) {
            const screen = filteredScreens[i];
            const availableSeats = responses[i].data.available_seats;

            venues[screen.venue_id].screens.push({
              id: screen.id,
              time: this.formatDateTime(screen.timing),
              date: this.formatDate(screen.timing),
              available_seats: availableSeats,
            });
          }
          for (let x in venues) {
            this.venues.push(venues[x]);
          }
          // Sort screens within each venue by time
          this.venues.forEach((venue) => {
            venue.screens.sort((a, b) => new Date(a.time) - new Date(b.time));
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
        this.date = this.day[this.url_date - 1];
        this.fetchData();
      }
    },
  },
};
</script>

<style>
/* Add your CSS styles here */
</style>
