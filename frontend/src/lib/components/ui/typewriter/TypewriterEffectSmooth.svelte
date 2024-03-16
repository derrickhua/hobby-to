<script lang="ts">
    import { onMount } from 'svelte';
    import { cn } from '$lib/utils';

    let Motion;
    onMount(async () => {
        const module = await import('svelte-motion');
        Motion = module.Motion;
    });

    export let words: {
        text: string;
        className?: string;
    }[];
    export let className: string | undefined = undefined;
    export let cursorClassName: string | undefined = undefined;

    let wordsArray = words.map((word) => ({
        ...word,
        text: word.text.split('')
    }));
</script>

{#if Motion}
    <div class={cn('my-6 flex space-x-1', className)}>
        <svelte:component this={Motion}
            style={{ width: 'fit-content' }}
            initial={{ width: '0%' }}
            transition={{
                duration: 2,
                ease: 'linear',
                delay: 1
            }}
        >
            <div class="overflow-hidden">
                <div
                    class="text-xs font-bold sm:text-base md:text-xl lg:text-3xl xl:text-5xl"
                    style="white-space: nowrap;"
                >
                    {#each wordsArray as word, idx}
                        <div class="inline-block">
                            {#each word.text as char, index}
                                <span class={cn('text-black dark:text-white', word.className)}>
                                    {char}
                                </span>
                            {/each}
                        </div>
                    {/each}
                </div>
            </div>
        </svelte:component>
        <svelte:component this={Motion}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{
                duration: 0.8,
                repeat: Infinity,
                repeatType: 'reverse'
            }}
        >
            <span
                class={cn('block h-4 w-4 rounded-sm bg-blue-500 sm:h-6 xl:h-12', cursorClassName)}
            ></span>
        </svelte:component>
    </div>
{/if}
