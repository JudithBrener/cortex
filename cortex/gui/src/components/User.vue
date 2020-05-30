<template>
  <div class="user">
    <b-container fluid>
      <b-card :title="user.username" class="mb-4">
        <b-card-text>{{user}}</b-card-text>
        <b-button v-bind:href="'#/snapshots/' + user.user_id" variant="primary">    <b-icon icon="camera"></b-icon>
 Go to Snapshots</b-button>
      </b-card>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "User",
  props: ["user"],
};
</script>

<style scoped>
</style>