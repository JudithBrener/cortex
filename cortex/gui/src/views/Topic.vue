<template>
  <div class="topic">
    <h2>Topic details:</h2>
    <h5>Snapshot ID: {{snapshot_id}}</h5>
    <h5>Topic: {{topic}}</h5>
    <vue-json-pretty :data="topic_details" :showDoubleQuotes="false"></vue-json-pretty>
  </div>
</template>


<script>
import VueJsonPretty from "vue-json-pretty";

export default {
  name: "Snapshot",
  components: {
    VueJsonPretty
  },
  data() {
    return {
      topic_details: {
        translation: {
          x: 0.4873843491077423,
          y: 0.007090016733855009,
          z: -1.1306129693984985
        },
        rotation: {
          x: -0.10888676356214629,
          y: -0.26755994585035286,
          z: -0.021271118915446748,
          w: 0.9571326384559261
        }
      }
    };
  },
  props: ["user_id", "snapshot_id", "topic"]
};
</script>

<style scoped>
.vjs-tree {
  text-align: justify;
  margin-top: 3em;
  margin-left: 2em;
}
</style>
