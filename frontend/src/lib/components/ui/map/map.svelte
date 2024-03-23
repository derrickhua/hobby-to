<script lang="ts">
    import { onMount } from 'svelte';
    import 'leaflet/dist/leaflet.css';
    import { faLocationPin, faLink, faStar } from '@fortawesome/free-solid-svg-icons';
    import { icon } from '@fortawesome/fontawesome-svg-core';

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

    let map;

    onMount(async () => {
        const L = await import('leaflet');
        map = L.map('map').setView([43.65107, -79.347015], 12);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        }).addTo(map);
    });

    $: if (map && locations) {
        map.eachLayer(layer => {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        locations.forEach(loc => {
            const markerIcon = icon(faLocationPin);
            const coloredIcon = markerIcon.html[0].replace('<svg', '<svg style="color: #F6995C; font-size: 20px;"');

            const customIcon = L.divIcon({
                html: coloredIcon,
                iconSize: L.point(20, 20),
                className: ''
            });
            const linkIcon = icon(faLink).html[0].replace('<svg', '<svg id="link-svg" style="color: #F6995C; font-size: 25px;"');
            const starIcon = icon(faStar).html[0].replace('<svg', '<svg id="star-svg" style="color: #F6995C; font-size: 25px;"');

            L.marker([loc.latitude, loc.longitude], { icon: customIcon })
                .addTo(map)
                .bindPopup(`
                    <div class="pop-up"style="padding: 5px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; background-color: #fff; border-radius: 5px;"> 
                            <h2 class="pop-up-title" >${loc.name}</h2>
                            <div class='pop-up-icons'>
                                <div class='pop-up-icons'>
                                    <span class="pop-up-cost">${loc.cost}</span>
                                    <a href="${loc.booking_url}" 
                                        class="pop-up-link" 
                                        onmouseover="document.getElementById('link-svg').style.color = '#ACE2E1';" onmouseout="document.getElementById('link-svg').style.color = '#F6995C';"
                                    >
                                        ${linkIcon}
                                    </a>                
                                    <div 
                                        class="pop-up-link" 
                                        onmouseover="document.getElementById('star-svg').style.color = '#ACE2E1';" onmouseout="document.getElementById('star-svg').style.color = '#F6995C';"
                                    >
                                        ${starIcon}
                                    </div>                          
                                </div>
                            </div>
                        </div>
                    </div>
                `);     
                });
    }
</script>

<div id="map" class="h-full w-full"></div>

<style>
    #map {
        height: 100%;
        width: 100%;
        border-radius: 15px;
    }



</style>