// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: [
        {
          type: 'doc',
          id: 'intro/intro',
        },
      ],
    },
    {
      type: 'category',
      label: 'Spec-Driven Development',
      items: [
        {
          type: 'doc',
          id: 'spec-cycle/spec-cycle',
        },
      ],
    },
    {
      type: 'category',
      label: 'AI Collaboration',
      items: [
        {
          type: 'doc',
          id: 'ai-collaboration/ai-collaboration',
        },
      ],
    },
    {
      type: 'category',
      label: 'Deployment & Automation',
      items: [
        {
          type: 'doc',
          id: 'deploy-automate/deploy-automate',
        },
      ],
    },
    {
      type: 'category',
      label: 'Governance & Maintenance',
      items: [
        {
          type: 'doc',
          id: 'governance/governance',
                },
      ],
    },
  ],
};

export default sidebars;