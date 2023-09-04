<template>
  <div>
    <h1 style="font-size: 100px; text-align: center; color: rgb(255, 102, 0)">
      Login as
    </h1>
    <div style="display: flex; justify-content: space-around">
      <a
        href="/user"
        style="
          width: fit-content;
          height: fit-content;
          background-color: rgb(171, 222, 245);
          color: black;
          text-decoration: none;
        "
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="300px"
          height="300px"
          fill="currentColor"
          class="bi bi-person"
          viewBox="0 0 16 16"
        >
          <path
            d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"
          />
        </svg>
        <h1 style="font-size: 60px; text-align: center">User</h1>
      </a>
      <a
        href="/admin"
        style="
          width: fit-content;
          height: fit-content;
          background-color: rgb(171, 222, 245);
          color: black;
          text-decoration: none;
        "
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="300px"
          height="300px"
          fill="currentColor"
          class="bi bi-person"
          viewBox="0 0 16 16"
        >
          <path
            d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"
          />
        </svg>
        <h1 style="font-size: 60px; text-align: center">Admin</h1>
      </a>
    </div>
  </div>
</template>

<style>
body {
  background-color: pink !important;
  font-family: sans-serif !important;
}
</style>
