<template>
  <div class="container addScreen">
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="addScreen"
      >
        <div class="shadow">
          <form
            @submit.prevent="addScreen"
            autocomplete="off"
            enctype="multipart/form-data"
          >
            <h3 class="page-header text-primary" style="text-align: center">
              Add Screen
            </h3>
            <h3 class="page-header text-primary" style="text-align: center">
              Venue: {{ venue.name }}
            </h3>
            <div class="form-group">
              <label style="font-size: 20px">Timing</label>
              <input
                v-model="screen.timing"
                type="datetime-local"
                class="form-control"
                required
              />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Price</label>
              <input
                v-model="screen.price"
                type="number"
                class="form-control"
                required
              />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Show</label>
              <select
                v-model="screen.show_id"
                class="form-control"
                style="
                  background-color: lightyellow;
                  width: 80%;
                  margin: auto !important;
                  text-align: center;
                "
                required
              >
                <option value="" disabled selected>Select a show</option>
                <option
                  v-for="show in existingShows"
                  :value="show.id"
                  :key="show.id"
                >
                  {{ show.name }}
                </option>
              </select>
            </div>
            <div
              class="form-group"
              style="margin-top: 5px; justify-content: center"
            >
              <button
                type="submit"
                class="btn btn-primary small-btn"
                style="
                  width: 150px;
                  height: 50px;
                  align-text: center;
                  font-size: 25px;
                "
              >
                Submit
              </button>
              <router-link
                to="/venue"
                class="btn btn-danger small-btn"
                style="
                  width: 150px;
                  height: 50px;
                  align-text: center;
                  font-size: 25px;
                "
              >
                Cancel
              </router-link>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api.js";
import { parseISO, format } from "date-fns";
export default {
  data() {
    return {
      screen: {
        timing: "",
        price: "",
        show_id: "",
        venue_id: "",
      },
      venue: {
        name: "",
      },
      existingShows: [],
    };
  },
  methods: {
    async addScreen() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const apiUrl = "/api/screen/add";
          const screen = this.screen;
          const inputDateString = screen.timing;
          const parsedDate = parseISO(inputDateString);
          screen.timing = format(parsedDate, "yyyy/MM/dd HH:mm:ss");
          await api.post(apiUrl, screen, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.$router.push("/venue");
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async fetchData() {
      this.screen.venue_id = this.$route.params.venue_id;

      const token = localStorage.getItem("access_token");
      if (token) {
        const response = await api.get(`/api/venue/${this.screen.venue_id}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.venue.name = response.data.name;
        const response1 = await api.get("/api/show/all", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.existingShows = response1.data.shows;
      } else {
        this.$router.push("/");
      }
    },
  },
  created() {
    this.fetchData();
  },
};
</script>

<style>
/* Add your CSS styles here */
</style>
