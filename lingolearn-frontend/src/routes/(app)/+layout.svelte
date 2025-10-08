<!-- src/routes/+layout.svelte -->
<script>
	import {SidebarMenu} from '$lib/components/layout';
    let { children } = $props();
    import Topbar from "$lib/components/layout/Topbar/Topbar.svelte";
    import Sidebar from "$lib/components/layout/Sidebar/SidebarMenu.svelte";
	import { page } from "$app/state";
      let sidebarOpen = $state(true);
</script>

<div class="layout">
    <!-- Topbar -->
    <header class="topbar">
        <Topbar onToggleSidebar={() => (sidebarOpen = !sidebarOpen)} />
    </header>

    <div class="body">
        <!-- Sidebar -->
        <aside class="sidebar">
            <Sidebar />
        </aside>

        <!-- Conteúdo principal -->
        <main class="main">
            {@render children()}
        </main>
    </div>
</div>

<style>
.layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

.topbar {
    height: 56px;
    flex-shrink: 0;
    background: #fff;
    border-bottom: 1px solid #ddd;
}

.body {
    flex: 1;
    display: flex;
    overflow: hidden;
}

.sidebar {
    width: 240px;
    background: #fafafa;
    border-right: 1px solid #ddd;
    overflow-y: auto;
}

.main {
    flex: 1;
    padding: 1rem;
    background: #f9f9f9;
    overflow-y: auto;
}
</style>
