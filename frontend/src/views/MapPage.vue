<script setup>
import { onMounted, ref } from 'vue';
import "leaflet/dist/leaflet.css";
import L from 'leaflet';
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import axios from 'axios';

const map = ref(null);
const locations = ref([]);
const backendUrl = 'http://127.0.0.1:8000';

const customIcon = (imageUrl) => {
  return L.icon({
    iconUrl: imageUrl,
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40]
  });
};

const fetchLocations = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/footprints/');
    locations.value = response.data.map(location => {
      const imageUrl = location.image.startsWith('http') ? location.image : `${backendUrl}${location.image}`;
      return {
        ...location,
        image: imageUrl,
      };
    });
  } catch (error) {
    console.error('获取足迹数据失败:', error);
  }
};

</script>

<template>
  <div class="map-container">
    <l-map 
      ref="map" 
      :zoom="2" 
      :center="[20, 0]" 
      style="height: 100%; width: 100%;"
      @ready="fetchLocations"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&amp;copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
      />
      <l-marker 
        v-for="location in locations" 
        :key="location.id" 
        :lat-lng="[location.latitude, location.longitude]"
        :icon="customIcon(location.image)"
      >
        <l-popup>
          <div class="popup-content">
            <h3>{{ location.name }}</h3>
            <p>{{ location.description }}</p>
            <p>日期: {{ location.date }}</p>
            <img :src="location.image" alt="Location Image" class="popup-image"/>
          </div>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh; /* 使地图容器占满整个视口高度 */
}

.popup-content {
  max-width: 200px;
}

.popup-image {
  width: 100%;
  height: auto;
  border-radius: 5px;
  margin-top: 10px;
}
</style> 