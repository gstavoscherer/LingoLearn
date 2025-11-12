<script lang="ts">
	import { Eye, BookOpen, TrendingUp } from '@lucide/svelte';
	import { Button, Progress, StatCard } from '../ui';
	import { goto } from '$app/navigation';
	import type { TextType } from '$lib/types';

	interface TextCardProps {
		text: TextType;
		onDetail: (text: TextType) => void;
	}

	let { text, onDetail }: TextCardProps = $props();
	let percentage = $derived.by(() => {
		return text.totalWords > 0 ? Math.round((text.totalKnownWords / text.totalWords) * 100) : 0;
	});
</script>

<div class="card">
	<div class="img">
		<div>
			<img src={text.imagePath} alt="" />
		</div>
	</div>
	<div class="content">
		<div class="top">
			<h2>{text.title}</h2>
			<p>{text.author}</p>
			<!-- Tag de linguagem -->
			<span class="language-tag">{text.language.name}</span>
		</div>
		<div class="middle">
			<Progress current={text.lastVisitedPage} total={text.totalPages} />

			<StatCard
				statCard={{
					icon: BookOpen,
					primary: String(text.totalKnownWords),
					secondary: `de ${text.totalWords} palavras`
				}}
				variant="secondary"
			/>

			<StatCard
				statCard={{
					icon: TrendingUp,
					primary: `${percentage}%`,
					secondary: 'vocabulário'
				}}
				variant="secondary"
			/>
		</div>
		<div class="buttons">
			<Button
				size="small"
				onclick={() => goto(`/texts/${text.id}/pages/${text.lastVisitedPage}`)}
			>
				<BookOpen />
				Continuar leitura
			</Button>
			<Button size="small" variant="outline" onclick={() => onDetail(text)}>
				<Eye />
				Detalhes
			</Button>
		</div>
	</div>
</div>

<style>
	.card {
		padding: 1rem 2rem;
		background: var(--background-white);
		border: 1px solid var(--border);
		border-radius: 8px;
		display: flex;
		gap: 1rem;
	}

	.content {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		flex: 1;
	}

	.middle {
		display: flex;
		justify-content: space-between;
	}

	img {
		height: 150px;
		width: 120px;
		object-fit: cover;
		border-radius: 8px;
	}

	.buttons {
		display: flex;
		gap: 1rem;
	}

	/* Estilo da tag de linguagem */
	.language-tag {
		display: inline-block;
		background: var(--primary-blue-light);
		color: var(--primary-blue);
		padding: 0.15rem 0.75rem;
		border-radius: 16px;
		font-size: 0.75rem;
		font-weight: 500;
		border: 1px solid var(--primary-blue);
		margin-top: 1rem;
	}
</style>
