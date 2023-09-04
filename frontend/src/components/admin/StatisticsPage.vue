<template>
  <div>
    <div
      class="top-movies"
      style="margin-top: 10px; text-align: left !important"
    >
      <h2>Top 5 Movies by rating</h2>
      <div class="bar-container">
        <div
          v-for="show in topshows"
          :key="show.id"
          class="bar"
          :style="{ width: `${show.rating * 10}%` }"
        >
          <span class="movie-name">{{ show.name }}</span>
          <span class="movie-rating">{{ show.rating.toFixed(2) }}</span>
        </div>
      </div>
    </div>
    <div
      class="top-movies"
      style="margin-top: 10px; text-align: left !important"
    >
      <h2>Top 5 Movies by collection</h2>
      <div class="bar-container">
        <div
          v-for="show in topcollection"
          :key="show.id"
          class="bar"
          :style="{ width: `${(show.total_revenue / max_collection) * 100}%` }"
        >
          <span class="movie-name">{{ show.name }}</span>
          <span class="movie-rating">{{ show.total_revenue.toFixed(2) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api.js";
export default {
  data() {
    return {
      topshows: [], // Populate this array with your top shows data from the backend or API
      topcollection: [], // Populate this array with your top collection data from the backend or API
      max_collection: 0, // Set this value to the maximum collection value from your backend or API
    };
  },
  methods: {
    async fetchData() {
      const token = localStorage.getItem("access_token");
      try {
        if (token) {
          const response = await api.get("/api/show/all", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const shows = response.data.shows;
          const topshows = shows.filter((show) => show.rating !== null);
          this.topshows = topshows
            .slice() // Create a copy of the array before sorting
            .sort((a, b) => b.rating - a.rating) // Sort by rating in descending order
            .slice(0, 5); // Take the top 5 shows
          const topcollection = shows.filter(
            (show) => show.total_revenue !== null
          );
          this.topcollection = topcollection
            .slice() // Create a copy of the array before sorting
            .sort((a, b) => b.total_revenue - a.total_revenue) // Sort by rating in descending order
            .slice(0, 5); // Take the top 5 shows
          this.max_collection = this.topcollection[0].total_revenue;
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
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
