import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Vitrox AI Similarity Search',
			// social: {
			// 	github: 'https://github.com/withastro/starlight',
			// },
			sidebar: [
				{
					label: 'Getting Started',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Installation', link: '/getting_started/installation/' },
						// { label: 'Configuration', link: '/getting_started/configuration/' },
					],
				},
				{
					label: 'Dataset',
					autogenerate: { directory: 'dataset' },

				},
				{
					label: 'Tutorial',
					autogenerate: { directory: 'tutorial' },

				},
				{
					label: 'Implementation',
					autogenerate: { directory: 'implementation' },

				},
				// {
				// 	label: 'Guides',
				// 	items: [
				// 		// Each item here is one entry in the navigation menu.
				// 		{ label: 'Example Guide', link: '/guides/example/' },
				// 		{ label: 'Initilisation', link: '/guides/initilisation/' },
				// 	],
				// },
				{
					label: 'Reference',
					autogenerate: { directory: 'reference' },
				},
			],
		}),
	],
});
