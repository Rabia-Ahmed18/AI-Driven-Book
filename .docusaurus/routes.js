import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'ead'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'f45'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '2d9'),
            routes: [
              {
                path: '/docs/ai-collaboration/ai-collaboration',
                component: ComponentCreator('/docs/ai-collaboration/ai-collaboration', 'd13'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/deploy-automate/deploy-automate',
                component: ComponentCreator('/docs/deploy-automate/deploy-automate', '4ef'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/getting-started',
                component: ComponentCreator('/docs/getting-started', '54c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/governance/governance',
                component: ComponentCreator('/docs/governance/governance', '18c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro/intro',
                component: ComponentCreator('/docs/intro/intro', '2c5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/spec-cycle/spec-cycle',
                component: ComponentCreator('/docs/spec-cycle/spec-cycle', 'd77'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
