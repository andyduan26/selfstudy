<template>
  <div class="admin-page-header">
    <div>
      <p class="section-kicker">{{ eyebrow }}</p>
      <h1>{{ title }}</h1>
      <p v-if="desc">{{ desc }}</p>
    </div>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  eyebrow: { type: String, default: 'Admin' },
  title: { type: String, required: true },
  desc: { type: String, default: '' },
})
</script>
