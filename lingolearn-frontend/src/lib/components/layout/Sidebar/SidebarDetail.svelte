<script lang="ts">
    import type { Snippet } from "svelte";

    type SidebarDirection = 'left' | 'right';

    interface SidebarDetailProps {
        direction?: SidebarDirection
        isOpen?: boolean
        children: Snippet
    }

    let { children, direction = 'right', isOpen = false }: SidebarDetailProps = $props();
</script>

<div class="overlay">
    <div 
        class="sidebar"
        class:sidebar-right={direction === 'right'}
        class:sidebar-left={direction === 'left'}
        hidden={!isOpen}
    >
        {@render children()}
    </div>
</div>

<style>
    /* Overlay escurecendo o fundo */
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.4); /* fundo escurecido */
        display: flex;
        justify-content: flex-end; /* padrão: direita */
        z-index: 1000;
    }

    /* Sidebar padrão */
    .sidebar {
        background-color: #fff;
        width: 300px;
        height: 100%;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }

    /* Direção direita */
    .sidebar-right {
        transform: translateX(0);
    }

    /* Direção esquerda */
    .sidebar-left {
        transform: translateX(0);
        margin-right: auto;
    }
</style>
