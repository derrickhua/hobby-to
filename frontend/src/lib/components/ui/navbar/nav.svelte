<script lang="ts">
    import { cn } from "$lib/utils.js";
    import * as Avatar from "$lib/components/ui/avatar";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    let className: string | undefined | null = undefined;
    export { className as class };
</script>

<nav class={cn("flex items-center justify-between w-full h-[120px]", className)}>
    <div class="flex items-center space-x-4 ">
        <div class="flex justify-center items-center h-full w-full">
            <a href="/" class="text-lg logo w-full text-center">HOBBY.TO</a>
        </div>
        <a href="/link1" class="text-sm font-medium transition-colors nav-links">ROADMAPS</a>
        <a href="/link2" class="text-sm font-medium transition-colors nav-links">RECOMMEND</a>
    </div>

    <DropdownMenu.Root>
        <DropdownMenu.Trigger >
            <Avatar.Root class="w-[50px] h-[50px]">
                <Avatar.Image src="/avatar.webp" alt="User avatar" />
            </Avatar.Root>
        </DropdownMenu.Trigger>
        <DropdownMenu.Content>
          <DropdownMenu.Group>
            <DropdownMenu.Label>My Account</DropdownMenu.Label>
            <DropdownMenu.Separator />
            <DropdownMenu.Item>Profile</DropdownMenu.Item>
            <DropdownMenu.Item>Billing</DropdownMenu.Item>
            <DropdownMenu.Item>Team</DropdownMenu.Item>
            <DropdownMenu.Item>Subscription</DropdownMenu.Item>
          </DropdownMenu.Group>
        </DropdownMenu.Content>
    </DropdownMenu.Root>
</nav>
