<script lang="ts">
    import { page } from '$app/state';
	import { CircleUserRound } from '@lucide/svelte';


    let user = {
        id: page.data.user.id,
        name: page.data.user.username,
        email: page.data.user.email,
        avatar: ''
    };
</script>

<div class="div">
    <CircleUserRound size={24}/>
</div>

<style>
    .div{
        display:flex;
        justify-content: center;
        align-items: center;
    }
</style>