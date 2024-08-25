<script setup>
</script>

<template>
  <div class="container" style="padding: 50px 0 100px 0">
    <nav>
      <div><RouterLink to="/">Home</RouterLink></div>
      <div><RouterLink to="/editor">Panel Edytora</RouterLink></div>
    </nav>
    <main>
      <RouterView />
    </main>

  </div>
</template>

<style>
nav div {
  float: left;
  padding-left: 5px;
  padding-right: 5px;
}
</style>
