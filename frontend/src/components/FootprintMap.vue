<template>
  <div class="map-container">
    <l-map
      ref="map"
      v-model:zoom="zoom"
      :center="center"
      :use-global-leaflet="false"
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
} from "@vue-leaflet/vue-leaflet";
import { ref } from "vue";
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

const zoom = ref(4);
const center = ref([31.30, 120.62]); // Default center, e.g., Suzhou

// --- Demo Data ---
const currentLocation = ref({
  name: "Suzhou, China",
  coords: [31.30, 120.62],
  avatarUrl: "/yxh.jpg", // Using the same avatar from HomePage
});

const locations = ref([
  { id: 1, name: "Shanghai", coords: [31.23, 121.47] },
  { id: 2, name: "Beijing", coords: [39.90, 116.40] },
  { id: 3, name: "Tokyo", coords: [35.68, 139.69] },
  { id: 4, name: "Seoul", coords: [37.56, 126.97] },
  { id: 5, name: "Bangkok", coords: [13.75, 100.50] },
  { id: 6, name: "Hong Kong", coords: [22.31, 114.16] },
]);
// --- End Demo Data ---
</script>

<style scoped>
.map-container {
  height: 100%;
  width: 100%;
  min-height: 380px; /* Match combined height of 2 rows + gap (180px + 180px + 20px) */
  border-radius: 8px;
  overflow: hidden;
}

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

/* Fix for transparent square behind custom markers */
:deep(.leaflet-div-icon) {
  background: transparent;
  border: none;
}
</style> 