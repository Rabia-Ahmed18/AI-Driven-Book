import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Spec-Driven Development',
    description: (
      <p>
        Learn how to apply Spec-Driven Development principles to create well-structured, 
        maintainable documentation projects with clear requirements and traceability.
      </p>
    ),
  },
  {
    title: 'AI Collaboration',
    description: (
      <p>
        Discover how to effectively integrate AI tools like Claude Code as collaborative 
        agents while maintaining human oversight and quality control.
      </p>
    ),
  },
  {
    title: 'Production Ready',
    description: (
      <p>
        Build and deploy production-grade technical books using Docusaurus v3, 
        with CI/CD pipelines and quality gates for consistent, high-quality releases.
      </p>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}