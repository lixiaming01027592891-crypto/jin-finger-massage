import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import react from '@astrojs/react';

export default defineConfig({
  site: 'https://goldenfingermassage.com',
  output: 'static',
  integrations: [tailwind(), sitemap({
    lastmod: new Date(),
    changefreq: 'weekly',
    priority: 0.7,
    serialize(item) {
      if (item.url.at(-1) === '/') {
        item.url = item.url.slice(0, -1);
      }
      return item;
    },
  }), react()],
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
      config: {
        limitInputPixels: false,
      },
    },
  },
});
