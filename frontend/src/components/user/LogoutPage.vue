<template>
  <div>
    <p style="margin-top: 20%; font-size: xx-large">
      Logging out
      <img src="/30.gif" alt="Loading..." />
    </p>
  </div>
</template>

<script>
export default {
  created() {
    this.logout();
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/");
    },
  },
};
</script>
