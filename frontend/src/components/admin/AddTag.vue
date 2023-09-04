<template>
  <div class="container addTag" style="margin-top: 150px; margin-left: 550px">
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="addTag"
      >
        <div class="shadow">
          <form
            @submit.prevent="addTag"
            autocomplete="off"
            enctype="multipart/form-data"
          >
            <h3 class="page-header text-primary" style="text-align: center">
              Add Tag
            </h3>
            <h3 class="page-header text-primary" style="text-align: center">
              Show: {{ show.name }}
            </h3>
            <div class="form-group">
              <label style="font-size: 20px">Tags</label>
              <select
                v-model="selectedTag.id"
                class="form-control"
                style="
                  background-color: lightyellow;
                  width: 80%;
                  margin: auto !important;
                  text-align: center;
                "
              >
                <option value="" disabled selected>Select tag</option>
                <option v-for="tag in tags" :value="tag.id" :key="tag.id">
                  {{ tag.name }}
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
                to="/show"
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
export default {
  data() {
    return {
      selectedTag: {
        id: "",
      }, // To store the selected tag IDs
      tags: [], // To store the fetched tag data
      chosentags: [],
      show: {},
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          // Fetch the list of tags from your API endpoint
          // and store it in the 'tags' data property
          // Example: this.tags = await fetchTags();
          const response = await api.get("/api/tag/all", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const showId = this.$route.params.show_id;
          const response1 = await api.get(`/api/show/${showId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log(response.data);
          console.log(response1.data);
          this.chosentags = response1.data.tags;
          this.tags = response.data.filter(
            (tag) => !response1.data.tags.some((c) => c.id == tag.id)
          );
          this.show = response1.data;
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async addTag() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const showId = this.$route.params.show_id;
          const tag = this.tags.filter((tag) => tag.id == this.selectedTag.id);
          const tags = [...tag, ...this.chosentags];
          await api.put(
            `/api/show/${showId}`,
            {
              tags: tags,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          this.$router.push("/show");
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style>
/* Add your CSS styles here */
</style>
