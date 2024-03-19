<script lang="ts">
    import { onMount } from 'svelte';
    import 'leaflet/dist/leaflet.css'; // CSS can be imported outside because it doesn’t reference `window`

    export let locations: Location[];

    interface Location {
        location_id: number;
        name: string;
        address: string;
        latitude: number;
        longitude: number;
        cost: string;
        popularity: number;
        booking_url: string;
    }

    let map: L.Map;

    onMount(async () => {
        const L = await import('leaflet');
        map = L.map('map').setView([43.65107, -79.347015], 12); // Example center and zoom

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Add markers for each location
        locations.forEach(loc => {
            L.marker([loc.latitude, loc.longitude])
                .addTo(map)
                .bindPopup(`${loc.name}<br>${loc.address}`);
        });
    });
</script>

<div id="map" class="h-full w-full"></div>

<style>
    #map {
        height: 100%;
        width: 100%;
        filter: grayscale(100%);
        border-radius: 15px;
    }
</style>