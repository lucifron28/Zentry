import adapter from '@sveltejs/adapter-vercel';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// Use Vercel adapter for optimal deployment
		adapter: adapter({
			// Optional: Configure edge functions
			runtime: 'nodejs18.x'
		})
	}
};

export default config;
