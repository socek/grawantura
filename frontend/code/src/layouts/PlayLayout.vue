<template>
  <div class="play-screen">
    <RouterView />
  </div>
</template>

<style scoped>
  .play-screen {
    position: fixed;
    inset: 0;
    overflow: auto;
    color: #f8fafc;
    /* Unitless, so large text gets a proportionally tall line. */
    line-height: 1.2;
    background:
      radial-gradient(circle at 15% 20%, rgba(236, 72, 153, 0.35), transparent 45%),
      radial-gradient(circle at 85% 80%, rgba(59, 130, 246, 0.35), transparent 45%),
      linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #0f172a 100%);
    font-family: 'Inter', Avenir, Helvetica, Arial, sans-serif;
  }
</style>
