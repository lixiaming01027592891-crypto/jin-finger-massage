import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    keywords: z.string(),
    date: z.string(),
    category: z.string().default('按摩服務'),
    ogImage: z.string().optional(),
    readTime: z.string().default('7 分鐘'),
    author: z.string().default('金手指按摩'),
    canonical: z.string().optional(),
  }),
});

export const collections = {
  blog: blogCollection,
};
