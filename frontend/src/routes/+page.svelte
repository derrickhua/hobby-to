<script lang="ts">
    import { concurrent } from 'svelte-typewriter';
    
</script>
<div class="h-full w-full flex flex-col py-16" style="max-width: 1500px;">
    <!-- Title Area -->
    <div class="h-[15%] flex justify-center items-center">
        <p use:concurrent={{ interval: 60 }} class="typewriter font-bold">
            FIND YOUR NEXT PASSION
        </p>
    </div>

    <div class="h-[15%] p-5 flex flex-row items-center justify-center">
        <div class="flex w-1/3 categories">
            <button class="category-btns">
                <img src="/paint-brush.png" alt="paintbrush illustration" style="width: 35px; height: 35px;">
                <p>ARTS</p>
            </button>
            <button class="category-btns">
                <img src="/sports.png" alt='circle illustration' style="width: 35px; height: 35px;"/>
                <p>SPORTS</p>
            </button>
            <button class="category-btns">
                <img src="/other.png" alt='square illustration' style="width: 35px; height: 35px;"/>
                <p>OTHER</p>
            </button>
        </div>

        <!-- Search bar in the center -->
        <div class="flex-1 mx-2 search">
            <input type="text" placeholder="Search..." class="w-full px-4 py-2 border rounded searchbar" />
        </div>

        <!-- Optional right side element -->
        <div class="flex w-1/3 costs"> 
            <button class="cost-btns">$</button>
            <button class="cost-btns">$$</button>
            <button class="cost-btns">$$$</button>
        </div>
    </div>

    <!-- Map Area -->
    <div class="flex-1">
        <!-- Leaflet map container -->
        <div id="map" class="h-full w-full">
            <!-- Map will be initialized here -->
        </div>
    </div>
</div>
