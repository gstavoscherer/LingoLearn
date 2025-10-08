<script lang="ts">
	import { Search } from "$lib/components/ui";
	import Button from "$lib/components/ui/Button.svelte";
	import Logo from "$lib/components/ui/Logo.svelte";
	import { Menu, Moon, Sun } from "@lucide/svelte";
	import Icon from "../Icon/Icon.svelte";


  export let darkMode: boolean = false;
  export let onToggleSidebar: () => void = () => {}
  const toggleDarkMode = () => {
    darkMode = !darkMode;
  };
</script>

<header class="topbar {darkMode ? 'dark' : ''}">
  <div class="topbar-inner">
    <!-- Esquerda -->
    <div class="topbar-left">
      <div class="menu">
        <Menu onclick={onToggleSidebar}  aria-label="Abrir/fechar sidebar"/>
      </div>
      <a class="logo" href="/home">
        <Logo />
      </a>
    </div>

   <div class="topbar-center">
    <Search />
   </div>

    <!-- Direita -->
    <div class="topbar-right">
      <Button onclick={toggleDarkMode} variant="ghost" aria-label="Alternar tema" style="color:black">
  {#if darkMode}
    <Sun />
  {:else}
    <Moon />
  {/if}
      </Button>
     <Button variant="ghost" style="color:black" >
       <Icon />
     </Button>
    </div>
  </div>
</header>

<style>
.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  height: 56px;
  border-bottom: 1px solid #e5e7eb; 
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  color: #1f2937;
}
.menu{
  cursor:pointer;
}

.topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 1.5rem; /* px-6 */
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.logo{
  cursor:pointer;
}
.topbar-center {
  flex: 1;
  max-width: 400px;
  margin: 0 2rem;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
