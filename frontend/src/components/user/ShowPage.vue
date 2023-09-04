<template>
  <div>
    <div class="search-dropdown" style="margin-top: 12px">
      <select v-model="selectedSearchType" @change="resetSearch">
        <option value="name">Search by Name</option>
        <option value="tag">Search by Tag</option>
        <option value="rating">Search by Rating</option>
      </select>
    </div>
    <input
      type="text"
      v-model="searchInput"
      @keyup="searchByShow"
      id="venue_input"
      :placeholder="getPlaceholderText(selectedSearchType)"
      class="search-input"
    />
    <div class="shows" id="shows">
      <div
        v-for="show in filteredShows"
        :key="show.id"
        class="card main_card show"
        style="width: 18rem"
      >
        <img
          :src="show.poster ? show.poster : '/images/no_image.png'"
          class="card-img-top"
          :style="
            show.poster
              ? 'background-color: white; height: 300px;'
              : 'background-color: white; height: 300px;'
          "
        />
        <div class="card-body">
          <h3 class="card-title" :id="'show-name-' + show.id">
            <div class="show-name">{{ show.name }}</div>
            <div class="tag-buttons">
              <button
                v-for="tag in show.tags"
                :key="tag.id"
                class="tag-button"
                @click="handleTagClick(tag)"
              >
                {{ tag.name }}
              </button>
            </div>
            <br />
            <template v-if="show.rating">
              {{ roundRating(show.rating) }}/10
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="25"
                height="25"
                fill="gold"
                class="bi bi-star-fill"
                viewBox="0 0 25 25"
              >
                <path
                  d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
                />
              </svg>
            </template>
            <template v-else> (no rating available) </template>
          </h3>
          <div v-if="!show.rating_exists">
            <div class="rate-button" @click="showRatingVisible[show.id] = true">
              Rate
            </div>
            <div v-if="showRatingVisible[show.id]">
              <input
                type="range"
                min="1"
                max="10"
                v-model="showRatings[show.id]"
              />
              <div>Rating: {{ showRatings[show.id] || 6 }}/10</div>
              <div
                class="btn btn-success small-button"
                @click="submitRating(show.id)"
              >
                Submit
              </div>
              <div
                class="btn btn-danger small-button"
                @click="cancelRating(show.id)"
              >
                Cancel
              </div>
            </div>
          </div>
        </div>
        <a :href="'/show/book/' + show.id + '/1'" class="book">Book</a>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api.js";
import { mapState } from "vuex";
import jwtDecode from "jwt-decode";
export default {
  data() {
    return {
      searchInput: "",
      shows: [],
      filteredShows: [],
      showRatings: {},
      selectedSearchType: "name",
      showRatingVisible: {},
      user_id: "",
    };
  },
  methods: {
    roundRating(rating) {
      return Math.round(rating * 100) / 100;
    },
    async submitRating(showId) {
      // Perform any actions you want when the "Submit" button is clicked
      this.showRatings[showId] = this.showRatings[showId] || 6;
      const token = localStorage.getItem("access_token");
      if (token) {
        const apiUrl = "/api/rating/add";
        const data = {
          rating: this.showRatings[showId],
          show_id: showId,
          user_id: this.user_id,
        };
        try {
          await api.post(apiUrl, data, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.getShows();
        } catch (e) {
          console.log(e);
        }
      } else {
        this.$router.push("/");
      }
    },
    cancelRating(showId) {
      this.showRatingVisible[showId] = false; // Hide the rating slider after canceling
    },
    searchByShow() {
      // Based on the selected search type, apply different filtering logic
      switch (this.selectedSearchType) {
        case "name":
          this.filterShowsByName();
          break;
        case "tag":
          this.filterShowsByTag();
          break;
        case "rating":
          this.filterShowsByRating();
          break;
        default:
          console.log(this.shows);
      }
    },
    filterShowsByName() {
      // Filter movies by name based on searchInput
      const input = this.searchInput.trim().toUpperCase();
      this.filteredShows = this.shows.filter((show) =>
        show.name.toUpperCase().includes(input)
      );
    },
    filterShowsByTag() {
      // Filter movies by tag based on searchInput
      const input = this.searchInput.trim().toLowerCase();
      this.filteredShows = this.shows.filter((show) =>
        show.tags.some((tag) => tag.name.toLowerCase().includes(input))
      );
    },
    filterShowsByRating() {
      // Filter movies by rating based on searchInput
      if (this.searchInput.trim().length === 0) {
        this.filteredShows = this.shows;
        return;
      }
      const rating = parseFloat(this.searchInput.trim());
      this.filteredShows = this.shows.filter((show) => show.rating >= rating);
    },
    getPlaceholderText(selectedSearchType) {
      switch (selectedSearchType) {
        case "name":
          return "Search for movie name..";
        case "tag":
          return "Search by tag..";
        case "rating":
          return "Search by rating..";
        default:
          console.log(this.shows);
          return "🔍 Search..";
      }
    },
    resetSearch() {
      this.searchInput = ""; // Clear the search input when changing search type
      this.searchByShow();
    },
    handleTagClick(tag) {
      this.selectedSearchType = "tag"; // Set the search type to "tag"
      this.searchInput = tag.name; // Set the searchInput to the clicked tag's name
      this.searchByShow(); // Perform the search
    },
    async getShows() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const decodedToken = jwtDecode(token);
        this.user_id = decodedToken.sub.user_id;
        const apiUrl = "/api/show/all";
        try {
          const response = await api.get(apiUrl, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.shows = response.data.shows;
          this.filteredShows = response.data.shows;
        } catch (e) {
          console.log(e);
        }
      } else {
        this.$router.push("/");
      }
    },
  },
  async created() {
    const token = localStorage.getItem("access_token");
    if (token) {
      const decodedToken = jwtDecode(token);
      this.user_id = decodedToken.sub.user_id;
      const apiUrl = "/api/show/all";
      try {
        const response = await api.get(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.shows = response.data.shows;
        this.filteredShows = response.data.shows;
      } catch (e) {
        console.log(e);
      }
    } else {
      this.$router.push("/");
    }
  },
  computed: {
    ...mapState(["token"]),
  },
};
</script>
<style>
.small-button {
  display: inline-block;
  margin-right: 10px;
  padding: 5px 10px;
  height: 40px;
  width: 80px;
  font-size: 12px;
  cursor: pointer;
}
.tag-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-button {
  background-color: lightblue;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.tag-button:hover {
  background-color: lightyellow;
}
.card {
  margin-bottom: 1rem;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.card-text {
  font-size: 1rem;
  text-align: center;
}

.main_card {
  margin-top: 2rem;
  /* background-color: aquamarine; */
  margin-left: 3rem;
  background-color: aquamarine !important;
}

.main_card .card {
  background-color: blanchedalmond !important;
  margin: 0 auto;
  margin-bottom: 10px;
}

.main_card .card-body {
  text-align: center;
}

#myInput {
  margin-top: 10px;
  margin-left: 220px;
  background-position: 10px 12px;
  width: 60%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-bottom: 20px;
  display: flex;
  text-align: center;
}

ul {
  list-style-type: none;
}

.shadow {
  box-shadow: 3px 3px 10px black;
  padding: 30px;
}

.venues,
.shows,
.cele {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-items: center;
}

.add {
  margin: 10px auto;
  /* background-color: red;
  height: 40px;
  width: 40px;
  border-radius: 50%;
  text-align: center;
  font-weight: bold;
  font-size: 25px; */
}

.add a {
  /* font-size: 25px; */
  text-decoration: none;
  font-weight: bold;
  color: black;
}

.add_block {
  width: 252.2px;
  height: 252.2px;
}

.error {
  color: red;
}

.book {
  width: 100%;
  font-size: 40px;
  background-color: #ffc20e !important;
  text-decoration: none;
  color: #ffffff !important;
  display: block;
}

.days {
  width: 85%;
}

.navbar-links ul {
  display: flex;
  justify-content: space-between;
  width: 100%;
  list-style: none;
  padding: 0;
  margin: 0;
}

.cele1,
.venues1 {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.rate-button {
  background-color: rgb(231, 66, 66);
  color: white;
  border-radius: 20px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.rate-button:hover {
  background-color: red;
}

#show_input {
  background-image: url("../../../public/images/search.png");
  background-position: 10px 12px;
  background-repeat: no-repeat;
  background-size: 25px;
  width: 35%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-top: 12px;
  margin-left: 37%;
}

#venue_input {
  background-image: url("../../../public/images/search.png");
  background-position: 10px 12px;
  background-repeat: no-repeat;
  background-size: 25px;
  width: 35%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-top: 12px;
}

.search-dropdown {
  display: inline-block;
  background-color: #ffffff;
  border: 1px solid #cccccc;
  border-radius: 3px;
  padding: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}

.search-dropdown:hover {
  background-color: #f5f5f5;
}

.search-dropdown select {
  background-color: transparent;
  border: none;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-right: 8px;
}

.top-movies {
  width: 80%;
  margin: 0 auto;
}

.bar-container {
  display: flex;
  flex-direction: column;
}

.bar {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 30px;
  background-color: #ff69b4;
  margin-bottom: 10px;
  position: relative;
}

.bar::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 4px;
  background-color: #ff0040;
}

.movie-name {
  padding-left: 10px;
  font-size: 16px;
  font-weight: bold;
  color: whitesmoke;
}

.movie-rating {
  position: absolute;
  right: 10px;
  font-size: 14px;
  font-weight: bold;
  color: #fff;
}
.search-input {
  margin-left: 20px !important;
  width: 30% !important;
}
</style>
