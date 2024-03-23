<script lang="ts">
    import { concurrent } from 'svelte-typewriter';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import LeafletMap from '$lib/components/ui/map/map.svelte';
    import { searchHobbies } from '$lib/util/hobbies';
    let query = '';
    let selectedCategory = '';
    let selectedCosts = writable(["$", "$$", "$$$"]); // All costs are selected by default
    let locations = writable([]);

    async function fetchHobbies() {
        try {
            const result = await searchHobbies({ query, cost: $selectedCosts, category: selectedCategory });
            // console.log(result);
            locations.set(result);
        } catch (error) {
            console.error(error);
        }
    }

    onMount(fetchHobbies);

    function handleSearch() {
        fetchHobbies();
    }

    function toggleCategory(category) {
        selectedCategory = selectedCategory === category ? '' : category;
        fetchHobbies();
    }

    function toggleCost(cost) {
        selectedCosts.update(currentCosts => {
            if (currentCosts.includes(cost)) {
                return currentCosts.filter(c => c !== cost);
            } else {
                return [...currentCosts, cost];
            }
        });
        fetchHobbies();
    }
</script>

<div class="h-full w-full flex flex-col py-16" style="max-width: 1500px;">
    <div class="h-[10%] flex justify-center items-center">
        <p use:concurrent={{ interval: 60 }} class="typewriter font-bold">
            FIND YOUR NEXT PASSION
        </p>
    </div>

    <div class="h-[17%] p-5 flex flex-row items-center justify-center">
        <div class="flex w-1/3 categories">
            <button class="category-btns" on:click={() => toggleCategory('Arts')} class:selected={selectedCategory === 'Arts'}>
                <img src="/paint-brush.png" alt="paintbrush illustration" style="width: 35px; height: 35px;">
                <p>ARTS</p>
            </button>
            <button class="category-btns" on:click={() => toggleCategory('Sports')} class:selected={selectedCategory === 'Sports'}>
                <img src="/sports.png" alt="circle illustration" style="width: 35px; height: 35px;">
                <p>SPORTS</p>
            </button>
            <button class="category-btns" on:click={() => toggleCategory('Other')} class:selected={selectedCategory === 'Other'}>
                <img src="/other.png" alt="square illustration" style="width: 35px; height: 35px;">
                <p>OTHER</p>
            </button>
        </div>

        <div class="flex-1 mx-2 search">
            <input type="text" placeholder="Search..." class="w-full px-4 py-2 border rounded searchbar" bind:value={query} on:keypress={e => e.key === 'Enter' && handleSearch()} />
        </div>

        <div class="flex w-1/3 costs">
            {#each ["$", "$$", "$$$"] as cost}
                <button class="cost-btns" on:click={() => toggleCost(cost)} class:selected={$selectedCosts.includes(cost)}>{cost}</button>
            {/each}
        </div>
    </div>

    <div class="flex-1">
        <LeafletMap locations={$locations} />
    </div>
</div>