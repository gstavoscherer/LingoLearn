<script lang="ts">
    import type { PaginatedList } from "$lib/types";

    interface PaginationProps {
        list: PaginatedList<unknown>
        onPageChange: (page: number) => void
    }

    let {list, onPageChange}: PaginationProps = $props();

    // Mostrar 3 páginas antes da atual
    let startPage = $derived(Math.max(1, list.currentPage - 3));
    // Mostrar 4 páginas depois da atual
    let endPage = $derived(Math.min(list.totalPages, list.currentPage + 4));
    
    // Ajustar o início se estivermos perto do final
    let adjustedStartPage = $derived(Math.max(1, Math.min(startPage, list.totalPages - 7)));
    // Ajustar o final se estivermos perto do início
    let adjustedEndPage = $derived(Math.min(list.totalPages, Math.max(endPage, 8)));
    
    let pages = $derived(Array.from(
        { length: adjustedEndPage - adjustedStartPage + 1 }, 
        (_, i) => adjustedStartPage + i
    ));

    function goToPage(page: number) {
        if (page >= 1 && page <= list.totalPages) {
            onPageChange(page);
        }
    }
</script>

<div class="pagination">
    <button
        class="pagination-btn"
        class:disabled={list.currentPage === 1}
        onclick={() => goToPage(list.currentPage - 1)}
    >
        ‹
    </button>

    {#if adjustedStartPage > 1}
        <button class="pagination-btn" onclick={() => goToPage(1)}>1</button>
        {#if adjustedStartPage > 2}
            <span class="pagination-ellipsis">...</span>
        {/if}
    {/if}

    {#each pages as page (page)}
        <button
            class="pagination-btn"
            class:active={page === list.currentPage}
            onclick={() => goToPage(page)}
        >
            {page}
        </button>
    {/each}

    {#if adjustedEndPage < list.totalPages}
        {#if adjustedEndPage < list.totalPages - 1}
            <span class="pagination-ellipsis">...</span>
        {/if}
        <button class="pagination-btn" onclick={() => goToPage(list.totalPages)}>
            {list.totalPages}
        </button>
    {/if}

    <button
        class="pagination-btn"
        class:disabled={list.currentPage === list.totalPages}
        onclick={() => goToPage(list.currentPage + 1)}
    >
        ›
    </button>
</div>

<style>
    .pagination {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
    }

    .pagination-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 2.5rem;
        height: 2.5rem;
        padding: 0 0.5rem;
        border: 1px solid var(--border);
        background: var(--background-white);
        color: var(--text-primary);
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .pagination-btn:hover:not(.disabled, .active) {
        background: var(--background-light);
        border-color: var(--primary-blue);
    }

    .pagination-btn.active {
        background: var(--primary-blue);
        color: var(--background-white);
        border-color: var(--primary-blue);
    }

    .pagination-btn.disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .pagination-ellipsis {
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 2.5rem;
        height: 2.5rem;
        color: var(--text-secondary);
    }
</style>