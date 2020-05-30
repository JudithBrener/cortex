<template>
  <div class="topic">
    <h2>Topic details:</h2>
    <h5>Snapshot ID: {{snapshot_id}}</h5>
    <h5>Topic: {{topic}}</h5>
    <vue-json-pretty :data="topic_details" :showDoubleQuotes="false"></vue-json-pretty>
    <b-img :v-if="has_image" :src="image_url" fluid></b-img>
  </div>
</template>


<script>
import VueJsonPretty from "vue-json-pretty";
import axios from "axios";

export default {
  name: "Topic",
  components: {
    VueJsonPretty
  },
  data() {
    return {
      topic_details: {},
      has_image: false,
      image_url: ""
    };
  },
  props: ["user_id", "snapshot_id", "topic"],
  created() {
    this.has_image = this.topic.includes("image");
    axios
      .get(
        this.hostUrl +"/users/" +
          this.user_id +
          "/snapshots/" +
          this.snapshot_id +
          "/" +
          this.topic
      )
      .then(res => {
        this.topic_details = res.data;
        if (this.has_image) {
          this.image_url = this.topic_details.url_to_view_data;
        }
      })
      .catch(err => console.log(err));
  }
};
</script>

<style scoped>
.vjs-tree {
  text-align: justify;
  margin-top: 3em;
  margin-left: 2em;
}
</style>
