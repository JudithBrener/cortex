<template>
  <div class="snapshot">
    <h2>Snapshot details:</h2>
    <h5>ID: {{snapshot_id}}</h5>
    <h5>Datetime: {{snapshot.datetime}}</h5>
    <b-list-group v-bind:key="result_name" v-for="result_name in snapshot.result_names">
      <b-list-group-item
        v-bind:href="'#/snapshots/'+ user_id + '/' + snapshot._id + '/' + result_name"
      >{{result_name}}</b-list-group-item>
    </b-list-group>
  </div>
</template>


<script>
export default {
  name: "Snapshot",
  data() {
    return {
        snapshot: { _id: "1234_1575446887339", result_names: ["pose", "feelings", "color_image"], datetime: 1575446887339 },
    };
  },
  props: ["user_id", "snapshot_id"],
  created() {}
};
</script>

<style scoped>
 .list-group-item {
     margin-top: 2em
 }
</style>
