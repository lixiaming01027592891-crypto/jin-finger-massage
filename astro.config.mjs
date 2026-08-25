import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import react from '@astrojs/react';

export default defineConfig({
  site: 'https://goldenfingermassage.com',
  output: 'static',
  // 不要加 serialize 去砍尾斜線：靜態輸出是 <route>/index.html，
  // Cloudflare Pages 對應的正式路徑就是帶斜線的 /route/。砍掉之後
  // sitemap 每一筆都會變成 308 的轉址來源，而轉址終點宣告的 canonical
  // 又指回會轉址的網址，訊號自相矛盾。Astro 預設輸出帶斜線，維持預設即可。
  integrations: [tailwind(), sitemap({
    lastmod: new Date(),
    changefreq: 'weekly',
    priority: 0.7,
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
