<template>
  <div class="snapshots">
    <h1>This are snapshots for user with id: {{user_id}}</h1>
    <b-list-group v-bind:key="snapshot._id" v-for="snapshot in snapshots">
      <b-list-group-item
        v-bind:href="'#/snapshots/'+ user_id + '/' + snapshot._id"
      >{{snapshot.datetime}}</b-list-group-item>
    </b-list-group>
  </div>
</template>


<script>
export default {
  name: "Snapshots",
  data() {
    return {
      snapshots: [
        { _id: "1234_1456886666", user_id: "1234", datetime: 1456886666 },
        { _id: "1234_1456886665", user_id: "1234", datetime: 1456886665 },
        { _id: "1234_1456886667", user_id: "1234", datetime: 1456886667 },
        { _id: "1234_1456886668", user_id: "1234", datetime: 1456886668 },
        { _id: "1234_1456886669", user_id: "1234", datetime: 1456886669 },
        { _id: "1234_1456886670", user_id: "1234", datetime: 1456886670 },
        { _id: "1234_1456886671", user_id: "1234", datetime: 1456886671 },
        { _id: "1234_1456886672", user_id: "1234", datetime: 1456886672 },
        { _id: "1234_1456886673", user_id: "1234", datetime: 1456886673 }
      ]
    };
  },
  props: ["user_id"],
  created() {
    function compare(a, b) {
      if (a.datetime < b.datetime) {
        return -1;
      }
      if (a.datetime > b.datetime) {
        return 1;
      }
      return 0;
    }
    this.snapshots.sort(compare);
  }
};
</script>
