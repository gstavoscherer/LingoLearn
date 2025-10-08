<script lang="ts">
	import { page } from "$app/state";
	import SidebarDetail from "$lib/components/layout/Sidebar/SidebarDetail.svelte";
	import TextModal from "$lib/components/modals/TextModal.svelte";
	import TextList from "$lib/components/text/TextList.svelte";
	import Button from "$lib/components/ui/Button.svelte";
	import Search from "$lib/components/ui/Search.svelte";
    import type { TextType } from "$lib/types";
    import { Upload, List, Grid3x3 } from "@lucide/svelte";
	import { onMount } from "svelte";
    
    type View = 'grid' | 'list';
    let bookView: View = $state('list');
    let isShowBookModal: boolean = $state(false);
    let texts: TextType[] = $state([]);
    onMount( async () => {
        let userId = page.data.user.id
        let query = `user_id=${userId}`
        const res = await fetch(`${import.meta.env.VITE_API_URL}/texts?${query}`);
        const data = await res.json();

        for (const text of data.texts) {
            const formattedText: TextType = {
                id: text.id,
                author: text.author,
                title: text.tile,
                language: text.language,
                totalWords: text.total_words,
                totalKnowWords: text.total_know_words,
				imagePath: text.image_path,
                lastPage: text.last_page,
                totalPages: text.total_pages
                
            }
            texts.push(formattedText);
        }
     
    });
</script>

<main>
    <section>
        <header>
            <div class="header-title">
                <h1>Minha Biblioteca</h1>
                <p>12 livros &bull; 12 em progresso</p>
            </div>
            <Button
                size='small'
                onclick={() => isShowBookModal=true}
            >
                <Upload size={20}/>
                Adicionar livro
            </Button>
        </header>

        
        <div class="options">
            <Search
                placeholder="Buscar por título, autor ou gênero..."
                size="full-width"
            />

            <select>
                <option>Todos os idiomas</option>
                <option>Português</option>
                <option>Inglês</option>
                <option>Espanhol</option>
            </select>

            <select>
                <option>Recente</option>
                <option>Mais antigos</option>
                <option>A-Z</option>
                <option>Z-A</option>
            </select>

            <div class="view">
                <button 
                class="button-left"
                class:active={ bookView === 'grid'}
                onclick={() => bookView = 'grid'}
                >
                    <Grid3x3 size={20}/>
                </button>

                <button
                    class="button-right"
                    class:active={ bookView === 'list'}
                    onclick={() => bookView = 'list'}
                >
                    <List size={20}/>
                </button>
            </div>
        </div>

        <div class="text-body">
            {#if bookView == 'grid'}
                <h1>Grid</h1>
            {:else}
                <TextList {texts}/>
            {/if}
        </div>
    </section>

    <TextModal
        isOpen={isShowBookModal}
        onClose={() => isShowBookModal=false}
    />
</main>
    
   
<style>
    main {
        display: flex;
    }

    section {
        width: 100%;
        padding: 4rem;
    }

    header {
        width: 100%;
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    .options {
        display: flex;
        gap: 1rem;
    }

    .view {
        display: flex;
        border-collapse: collapse;
    }

    .view button {
        padding: 0.5rem 0.5rem;
        background-color: var(--background-light);
        border-radius: 8px;
        border: 1px solid var(--border);
    }

    .view button.button-left {
        border-top-right-radius: 0 ;
        border-bottom-right-radius: 0;
    }

    .view button.button-right {
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
    }

    .view button.active {
        background: var(--primary-blue);
        color: var(--background-white)
    }

    .text-body {
        margin-top: 1rem;
    }
</style>