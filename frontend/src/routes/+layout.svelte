<script lang="ts">
    import "../app.pcss";
    import Nav from '../lib/components/ui/navbar/nav.svelte';
    </script>
    
    <div class="h-screen w-full grid grid-rows-[auto,1fr] px-[80px]">
        <Nav />
        <div class="overflow-auto flex justify-center" style="">
            <slot></slot> 
        </div>
    </div>