<script lang="ts">
    import TypewriterEffectSmooth from '$lib/components/ui/typewriter/TypewriterEffectSmooth.svelte';
    const words = [
		{
			text: 'Build'
		},
		{
			text: 'awesome'
		},
		{
			text: 'apps'
		},
		{
			text: 'with'
		},
		{
			text: 'Aceternity.',
			className: 'text-blue-500 dark:text-blue-500'
		}
	];
    
</script>
<div class="h-full w-full flex flex-col py-16">
    <!-- Title Area -->
    <div class="h-[15%] ">
        <TypewriterEffectSmooth {words} />
    </div>

    <!-- Navigation Area -->
    <div class="h-[15%] p-5">
        <!-- Dropdowns on the left -->
        <div class="flex space-x-2">
            <button class="px-4 py-2 border rounded">Dropdown 1</button>
            <button class="px-4 py-2 border rounded">Dropdown 2</button>
            <button class="px-4 py-2 border rounded">Dropdown 3</button>
        </div>

        <!-- Search bar in the center -->
        <div class="flex-1 mx-2">
            <input type="text" placeholder="Search..." class="w-full px-4 py-2 border rounded" />
        </div>

        <!-- Optional right side element -->
        <div> 
            <!-- Elements like additional dropdowns or buttons can go here -->
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
