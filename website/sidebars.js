// website/sidebars.js

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: "doc",
      id: "intro",
      label: "Introduction",
    },
    {
      type: "doc",
      id: "course-overview",
      label: "Course Overview",
    },
    {
      type: "doc",
      id: "learning-outcomes",
      label: "Learning Outcomes",
    },
    {
      type: "doc",
      id: "course-structure",
      label: "Course Structure",
    },
    {
      type: "category",
      label: "Course Modules",
      items: [
        "module-1-robotic-nervous-system",
        "module-2-digital-twin",
        "module-3-ai-robot-brain",
        "module-4-vision-language-action",
      ],
    },
  ],
};

module.exports = sidebars;
