const modules = import.meta.glob("./**/*.svelte", { eager: true });

export const components = Object.fromEntries(
	Object.entries(modules).map(([path, module]) => {
		const name = path.split("/").pop()?.replace(".svelte", "")!;
		return [name, (module as any).default];
	})
);