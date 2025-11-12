<script lang="ts">
	import Logo from '../ui/Logo.svelte';
</script>

<footer class="footer">
	<div class="footerContainer">
		<div class="footerContent">
			<div class="footerSection">
				<div class="footerLogo">
					<Logo size="small" />
				</div>
				<p class="footerDescription">
					A forma mais inteligente de aprender idiomas através de textos reais.
				</p>
			</div>
			<div class="footerSection">
				<h4 class="footerSectionTitle">Produto</h4>
				<ul class="footerLinks">
					<li>
						<a href="/" class="footerLink"> Recursos </a>
					</li>
					<li>
						<a href="/" class="footerLink"> Preços </a>
					</li>
					<li>
						<a href="#faq" class="footerLink"> FAQ </a>
					</li>
				</ul>
			</div>
			<div class="footerSection">
				<h4 class="footerSectionTitle">Suporte</h4>
				<ul class="footerLinks">
					<li>
						<a href="/" class="footerLink"> Central de Ajuda </a>
					</li>
					<li>
						<a href="/" class="footerLink"> Contato </a>
					</li>
					<li>
						<a href="/" class="footerLink"> Status </a>
					</li>
				</ul>
			</div>
			<div class="footerSection">
				<h4 class="footerSectionTitle">Legal</h4>
				<ul class="footerLinks">
					<li>
						<a href="/" class="footerLink"> Privacidade </a>
					</li>
					<li>
						<a href="/" class="footerLink"> Termos </a>
					</li>
					<li>
						<a href="/" class="footerLink"> Cookies </a>
					</li>
				</ul>
			</div>
		</div>
		<div class="footerBottom">
			<p>&copy; 2025 LingoLearn. Todos os direitos reservados.</p>
		</div>
	</div>
</footer>

<style>
	.footer {
		background: var(--text-primary);
		color: white;
		padding: 3rem 2rem 1rem;
	}

	.footerContainer {
		max-width: 1200px;

		margin: 0 auto;
	}
	.footerContent {
		display: grid;
		grid-template-columns: 2fr 1fr 1fr 1fr;
		gap: 2rem;
		margin-bottom: 2rem;
	}

	.footerSection {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.footerLogo {
		margin-bottom: 0.5rem;
	}

	.footerDescription {
		color: rgba(255, 255, 255, 0.8);
		line-height: 1.6;
	}

	.footerSectionTitle {
		font-weight: 600;
		margin-bottom: 0.5rem;
	}

	.footerLinks {
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.footerLink {
		color: rgba(255, 255, 255, 0.8);
		transition: color 0.2s ease;
	}

	.footerLink:hover {
		color: var(--primary-blue);
	}

	.footerBottom {
		padding-top: 2rem;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		text-align: center;
		color: rgba(255, 255, 255, 0.6);
	}
</style>
