<script lang="ts">
	import { page } from '$app/state';
	import { Page, PageHeader } from '$lib/components/page';

	const { data } = page.data;

    function onWordClick() {
        console.log('click')
    }
</script>

<div class="main">
	<div class="sidebar">
	</div>
	<div class="page">
		<PageHeader text={data.text} />
		<div class="page-content">
			<Page content={data.content} language={data.text.language} {onWordClick} />
		</div>
	</div>
</div>

<style>
	.main {
		display: flex;
		height: 100vh; /* ocupa a tela toda */
		width: 100vw;
	}

	/* Sidebar já tem largura definida no seu componente */
	.sidebar {
		flex-shrink: 0; /* impede de encolher */
	}

	.page-content {
        display: flex;
        justify-content: center;
		flex: 1; /* ocupa todo espaço disponível */
		padding: 1.5rem;
		overflow-y: auto; /* rola só o conteúdo */
	}

</style>
