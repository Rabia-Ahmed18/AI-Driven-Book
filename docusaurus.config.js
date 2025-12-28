// @ts-check



/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI-Spec-Driven Book Creation',
  tagline: 'A practical guide to building and deploying technical documentation using Spec-Driven Development and AI-assisted authoring',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  
  url: 'https://ai-driven-book-nine.vercel.app/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<org-name>/<repo-name>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  organizationName: 'Rabia-Ahmed18', // Usually your GitHub org/user name.
  projectName: 'ai-spec-driven-book', // Usually your repo name.

  onBrokenLinks: 'warn',
  markdown: {
    format: 'mdx',
    mermaid: false,
    // Updated to use the new location for onBrokenMarkdownLinks
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
 },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
        
        },
        blog: false, // Disable blog functionality
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/logo~.jpg',
      navbar: {
        title: 'AI/Spec-Driven Book',
        // logo: {
        //   alt: 'AI/Spec-Driven Book Logo',
        //   src: '/Agentic-Ai-Projects/HACKATHON/HACKATHON-1/static/img',
        //   href: '/ ',
        // },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            href: 'https://github.com/Rabia-Ahmed18/ai-spec-driven-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro/intro',  // Updated to point to the correct doc
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Rabia-Ahmed18/ai-spec-driven-book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AI/Spec-Driven Book Creation. Built by RABIA.`,
      },
      prism: {
        defaultLanguage: 'javascript',
      },
    }),
};

export default config;