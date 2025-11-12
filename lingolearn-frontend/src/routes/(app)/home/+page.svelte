<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { Button } from '$lib/components/ui';
	import type { DashboardData, PaginatedList, TextType } from '$lib/types.js';
	import { formatStudyTime } from '$lib/utils.js';
	import { ALargeSmall, Brain, Clock, TrendingUp } from '@lucide/svelte';

	let { data } = $props();

	function capitalizeFirstLetter(str: string) {
		if (typeof str !== 'string' || str.length === 0) {
			return str;
		}
		return str.charAt(0).toUpperCase() + str.slice(1);
	}

	let texts: PaginatedList<TextType> = $derived(data.texts);
	let username = $derived(capitalizeFirstLetter(page.data.user.username));
	let dashboardData: DashboardData = $derived(data.dashboardData);
</script>

<main>
	<header>
		<h3>Bem vindo de volta, {username}!</h3>
		<p>Continue sua jornada de aprendizado</p>
	</header>
	<section class="header">
		<div class="card">
			<div class="icon">
				<ALargeSmall size={28} />
			</div>
			<div class="card-label">Palavras aprendidas</div>
			<div class="card-data">{dashboardData.userKnownWords}</div>
			<div class="card-progress">+{dashboardData.userKnownWordsLastWeek} essa semana</div>
		</div>
		<div class="card">
			<div class="icon">
				<TrendingUp size={28} />
			</div>
			<div class="card-label">Sequência atual</div>
			<div class="card-data">{dashboardData.streak} {dashboardData.streak == 1 ? 'Dia' : 'Dias'}</div>
			
		</div>
		<div class="card">
			<div class="icon">
				<Clock size={28} />
			</div>
			<div class="card-label">Tempo de estudo</div>
			<div class="card-data">{formatStudyTime(dashboardData.studyTimeToday)}</div>
			<div class="card-progress" style="color: var(--text-secondary);">hoje</div>
		</div>
	</section>
	<section class="body">
		<div class="book-section card">
			<p>Continue lendo</p>
			<div class="book-list">
				{#each texts.items as text (text.id)}
					<div class="book-card">
						<img class="book-image" src={text.imagePath} alt="" />
						<div>
							<p class="title">{text.title}</p>
							<p class="author">{text.author}</p>
						</div>
						<div class="tag">
							{text.language.name}
						</div>
						<div>
							<Button
								variant="primary"
								size="fullWidth"
								onclick={() =>
									goto(`/texts/${text.id}/pages/${text.lastVisitedPage ?? 1}`)}
							>
								Continuar
							</Button>
						</div>
					</div>
				{/each}
			</div>
		</div>
		<div class="card">
			<div class="quiz-card">
				<div class="quiz-icon">
					<Brain size={32} />
				</div>
				<p class="quiz-card-title">Quiz de revisão</p>
				<p class="quiz-card-primary-review">32</p>
				<p class="quiz-card-secondary">Palavras para revisar</p>
				<div class="button">
                    <Button
                                        class="button"
                        variant="primary"
                        size="fullWidth"
                    >
                        Começar Quiz
                    </Button>
                </div>
			</div>
		</div>
	</section>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		height: 100%;
        padding: 0 1rem;
	}

	header {
		margin-left: 4rem;
		margin-bottom: 1rem;
	}

	header h3 {
		font-size: 28px;
	}

	header p {
		font-size: 20px;
		color: var(--text-secondary);
	}

	section.header {
		width: 100%;
		display: flex;
		justify-content: space-between;
	}

	.card {
		background-color: var(--background-white);
		padding: 1rem;
		border-radius: 8px;
		border: 1px solid var(--border);
		color: var(--text-primary);
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		min-width: 300px;
		min-height: 200px;
	}

	.icon {
		display: flex;
		justify-content: center;
		align-items: center;
		width: fit-content;
		border-radius: 8px;
		color: var(--primary-blue);
		background-color: var(--primary-blue-light);
		aspect-ratio: 1 / 1;
		height: 36px;
		margin-bottom: 1rem;
	}

	.quiz-icon {
		display: flex;
		justify-content: center;
		align-items: center;
		width: fit-content;
		border-radius: 100%;
		color: var(--background-white);
		background-color: var(--primary-blue);
		aspect-ratio: 1 / 1;
		height: 64px;
		margin-bottom: 1rem;
	}

	.card-label {
		color: var(--text-secondary);
	}

	.card-data {
		font-size: 20px;
		font-weight: 800;
	}

	.card-progress {
		color: var(--success-green);
		font-weight: 600;
	}

	.body {
		display: flex;
		justify-content: space-between;
		flex-grow: 1;
	}

	.book-section {
		font-size: 16px;
		font-weight: 600;
		min-width: 1000px !important;
	}

	.book-section > p {
		font-size: 20px;
	}

	.book-list {
		height: 100%;
		display: flex;
		gap: 2rem;
		flex-direction: row;
	}

	.book-card {
		background-color: var(--background-white);
		padding: 1rem;
		border-radius: 8px;
		border: 1px solid var(--border);
		color: var(--text-primary);
		display: flex;
		flex-direction: column;
		gap: 1rem;
		min-width: 300px;
		min-height: 200px;
	}

	.book-image {
		height: 185px;
		width: 140px;
		align-self: center;
		margin-bottom: 0.5rem;
		border: 1px solid var(--border);
		border-radius: 6px;
	}

	.title {
		font-size: 18px;
		line-height: 1rem;
	}

	.author {
		font-size: 14px;
		color: var(--text-secondary);
	}

	.tag {
		width: fit-content;
		display: inline-block;
		background: var(--primary-blue-light);
		color: var(--primary-blue);
		padding: 0.15rem 0.75rem;
		border-radius: 16px;
		font-size: 0.75rem;
		font-weight: 500;
		border: 1px solid var(--primary-blue);
	}

	.card:has(.quiz-card) {
		background-color: var(--primary-blue-lightest);
		border: 1px solid var(--primary-blue-light);
	}

	.quiz-card {
		width: 100%;
		height: 100%;
		display: flex;
		padding: 1rem 0rem;
		align-items: center;
		flex-direction: column;
		gap: 1.5rem;
	}

	.quiz-card-title {
		font-size: 20px;
		font-weight: 600;
	}

	.quiz-card-primary-review {
		font-size: 42px;
		font-weight: 700;
		line-height: 1.2rem;
	}

	.quiz-card-secondary {
		font-size: 16px;
		color: var(--text-secondary);
	}

    .quiz-card .button {
        width: 100%;
        margin-top: auto;
    }
</style>
