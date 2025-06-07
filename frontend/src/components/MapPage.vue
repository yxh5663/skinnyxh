<template>
  <div class="map-page-container">
    <l-map
      v-if="mapReady"
      ref="map"
      v-model:zoom="zoom"
      :center="center"
      :use-global-leaflet="false"
      class="full-page-map"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>

      <!-- Visited places markers -->
      <l-marker
        v-for="location in locations"
        :key="location.id"
        :lat-lng="location.coords"
      >
        <l-icon :icon-anchor="[20, 20]">
          <div class="location-marker"></div>
        </l-icon>
        <l-popup>
          <div class="location-popup">
            <img v-if="location.imageUrl" :src="location.imageUrl" alt="Location Image" class="popup-image"/>
            <h3>{{ location.name }}</h3>
            <p>{{ location.description }}</p>
          </div>
        </l-popup>
      </l-marker>

      <!-- Current location marker with avatar -->
      <l-marker :lat-lng="currentLocation.coords">
        <l-icon :icon-anchor="[30, 30]">
          <div class="avatar-marker">
            <img :src="currentLocation.avatarUrl" alt="Avatar" />
          </div>
        </l-icon>
      </l-marker>
      
      <!-- Current location label -->
      <l-control position="bottomleft" class="location-label-control">
          <div class="location-label">{{ currentLocation.name }}</div>
      </l-control>

    </l-map>
    <div v-else class="loading-placeholder">
      Loading Map...
    </div>
  </div>
</template>

<script setup>
import "leaflet/dist/leaflet.css";
import {
  LMap,
  LTileLayer,
  LMarker,
  LIcon,
  LControl,
  LPopup,
} from "@vue-leaflet/vue-leaflet";
import { ref, onMounted } from "vue";
import L from 'leaflet';

// --- Fix for broken Leaflet icons in Webpack ---
// eslint-disable-next-line
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});
// --- End of fix ---

const mapReady = ref(false);

onMounted(() => {
  // Delay map rendering until the component is fully mounted
  mapReady.value = true;
});

const zoom = ref(5); // Zoom out a bit for a larger map view
const center = ref([31.30, 120.62]); // Default center, e.g., Suzhou

// --- Demo Data (same as FootprintMap) ---
const currentLocation = ref({
  name: "Suzhou, China",
  coords: [31.30, 120.62],
  avatarUrl: "/yxh.jpg",
});

const locations = ref([
  { id: 1, name: "Shanghai", coords: [31.23, 121.47], description: "A vibrant metropolis, known for its stunning skyline and rich cultural heritage.", imageUrl: "https://picsum.photos/seed/shanghai/200/150" },
  { id: 2, name: "Beijing", coords: [39.90, 116.40], description: "The heart of China, with a history stretching back millennia. Home to the Forbidden City and the Great Wall.", imageUrl: "https://picsum.photos/seed/beijing/200/150" },
  { id: 3, name: "Tokyo", coords: [35.68, 139.69], description: "A dazzling blend of ultramodern and traditional, from neon-lit skyscrapers to historic temples.", imageUrl: "https://picsum.photos/seed/tokyo/200/150" },
  { id: 4, name: "Seoul", coords: [37.56, 126.97], description: "A city of palaces, pop culture, and incredible food. The capital of South Korea is a must-visit.", imageUrl: "https://picsum.photos/seed/seoul/200/150" },
  { id: 5, name: "Bangkok", coords: [13.75, 100.50], description: "The bustling capital of Thailand, known for its ornate shrines and vibrant street life.", imageUrl: "https://picsum.photos/seed/bangkok/200/150" },
  { id: 6, name: "Hong Kong", coords: [22.31, 114.16], description: "A major port and global financial hub with a skyscraper-studded skyline.", imageUrl: "https://picsum.photos/seed/hongkong/200/150" },
]);
// --- End Demo Data ---
</script>

<style scoped>
.map-page-container {
  height: calc(100vh - 60px); /* Adjust based on your nav bar height */
  width: 100%;
}

.full-page-map {
  height: 100%;
  width: 100%;
}

.loading-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 1.5em;
  color: #888;
}

.location-popup {
  width: 200px;
  text-align: left;
}

.popup-image {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}

.location-popup h3 {
  margin: 0 0 5px 0;
  font-size: 1.1em;
}

.location-popup p {
  margin: 0;
  font-size: 0.9em;
  color: #555;
}

/* Fix for transparent square behind custom markers */
:deep(.leaflet-div-icon) {
  background: transparent;
  border: none;
}

/* Reusing marker styles from FootprintMap.vue for consistency */
.location-marker {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(128, 0, 128, 0.8) 0%, /* Center color (purple) */
    rgba(128, 0, 128, 0.5) 40%,
    rgba(75, 0, 130, 0.2) 70%, /* Outer glow (indigo) */
    rgba(75, 0, 130, 0) 100%
  );
  box-shadow: 0 0 10px 2px rgba(128, 0, 128, 0.5);
}

.avatar-marker {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: white;
  padding: 5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-marker img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.location-label-control {
    margin-left: 10px !important;
    margin-bottom: 10px !important;
}

.location-label {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 500;
  color: #333;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  font-size: 14px;
}
</style> 