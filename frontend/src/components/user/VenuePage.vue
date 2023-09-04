<template>
  <div>
    <div class="search-dropdown" style="margin-top: 12px">
      <select id="search-options" v-model="searchOption">
        <option value="venue">Search by Venue</option>
        <option value="location">Search by Location</option>
      </select>
    </div>
    <input
      v-model="searchInput"
      type="text"
      id="venue_input"
      @input="searchVenue"
      :placeholder="
        searchOption === 'location'
          ? 'Search for location..'
          : 'Search for venue name..'
      "
      style="width: 30% !important; margin-left: 20px !important"
    />

    <div class="venues" style="flex-direction: column; align-items: center">
      <div
        v-for="venue in filteredVenues"
        :key="venue.id"
        class="card main_card"
        style="width: 18rem; margin-bottom: 20px"
      >
        <div class="card-body">
          <h3 class="card-title venue-name">{{ venue.name }}</h3>
          <address style="font-size: 25px" class="venue-address">
            {{ venue.address }}
          </address>
        </div>
        <div class="card-footer" style="padding: 0px; border-color: #ffc20e">
          <router-link :to="'/venue/book/' + venue.id + '/1'" class="book"
            >Book</router-link
          >
        </div>
      </div>
    </div>
    <div v-if="filteredVenues.length === 0" style="text-align: center">
      <h3 class="card-text" style="font-size: 25px; font-weight: bold">
        No venues found.
      </h3>
    </div>
  </div>
</template>

<script>
import api from "../../api.js";
export default {
  data() {
    return {
      searchOption: "venue",
      searchInput: "",
      venues: [], // Initialize venues as an empty array to be populated later
    };
  },
  computed: {
    filteredVenues() {
      const filter = this.searchInput.toUpperCase();
      return this.venues.filter((venue) => {
        if (this.searchOption === "location") {
          return venue.address.toUpperCase().includes(filter);
        } else {
          return venue.name.toUpperCase().includes(filter);
        }
      });
    },
  },
  methods: {
    async fetchVenues() {
      const token = localStorage.getItem("access_token");
      if (token) {
        // Fetch venues data from the API using axios or any other HTTP client
        try {
          const response = await api.get("/api/venue/all", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }); // Replace with the actual API endpoint to fetch venues
          this.venues = response.data.venues; // Assign the fetched venues data to the 'venues' data property
        } catch (error) {
          console.error(error);
        }
      } else {
        this.$router.push("/");
      }
    },
  },
  mounted() {
    this.fetchVenues();
  },
};
</script>

<style></style>
