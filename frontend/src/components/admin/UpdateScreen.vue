<template>
  <div class="container updateScreen">
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="updateScreen"
      >
        <div class="shadow">
          <h3 class="page-header text-primary" style="text-align: center">
            Update Screen
          </h3>
          <h3 class="page-header text-primary" style="text-align: center">
            Venue: {{ venue.name }}
          </h3>
          <form
            @submit.prevent="submitForm"
            autocomplete="off"
            enctype="multipart/form-data"
          >
            <div class="form-group">
              <label style="font-size: 20px">Updated Timing</label>
              <input
                v-model="screen.timing"
                type="datetime-local"
                class="form-control"
                required
              />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Updated Price</label>
              <input
                v-model="screen.price"
                type="number"
                class="form-control"
                required
              />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Updated Show id</label>
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
                style="width: 150px; height: 50px; font-size: 25px"
              >
                Submit
              </button>
              <a
                class="btn btn-danger small-btn"
                style="width: 150px; height: 50px; font-size: 25px"
                href="/venue"
                >Cancel</a
              >
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
        price: null,
        show_id: null,
        venue_id: null,
      },
      venue: {
        name: "",
      },
      existingShows: [],
    };
  },
  methods: {
    async submitForm() {
      try {
        const token = localStorage.getItem("access_token");
        const screenId = this.$route.params.screen_id;
        if (token) {
          const screen = this.screen;
          const inputDateString = screen.timing;
          const parsedDate = parseISO(inputDateString);
          screen.timing = format(parsedDate, "yyyy-MM-dd HH:mm:ss");

          // Log the updated screen object for debugging
          console.log(screen);

          // Perform the API request to update the screen
          await api.put(`/api/screen/${screenId}`, screen, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          // Redirect to the venue page after successful update
          this.$router.push("/venue");
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        // Handle errors here if needed
        console.error(error);
      }
    },
    async fetchData() {
      try {
        const token = localStorage.getItem("access_token");
        const screenId = this.$route.params.screen_id;
        if (token) {
          const response = await api.get(`/api/screen/${screenId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.venue.name = response.data.venue_name;
          this.screen.timing = response.data.timing;
          this.screen.price = response.data.price;
          this.screen.venue_id = response.data.venue_id;
          this.screen.show_id = response.data.show_id;
          const response1 = await api.get("/api/show/all", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.existingShows = response1.data.shows;
          console.log(this.screen);
          console.log(response.data);
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        // Handle errors here if needed
        console.error(error);
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
